# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_order_id = fields.Many2one('sale.order',string='Related Sale Order')

class AccountMove(models.Model):
    """This model is used to add a new state to sales order."""
    _inherit = 'account.move'

    related_sale_order_ids = fields.Many2many('sale.order',
                                              string='Related SO',
                                              domain=[('invoice_status','=','to invoice')]
                                              )
    related_added_sale_order_ids = fields.Many2many('sale.order', string='Related SO',
                                                    relation='account_move_new_sales_order_ids_rel',
                                                    column1='move_id',
                                                    column2='sale_order_id',
                                                    )
    sales_order_count = fields.Integer(compute="_compute_origin_so_counts", string='Sale Order Count', store=True)

    @api.onchange('related_sale_order_ids')
    def _onchange_related_sale_order_ids(self):
        """Method use to add the sales order lines to invoice line."""

        self.related_added_sale_order_ids = [fields.Command.set(self.related_sale_order_ids.ids)]
        self.invoice_line_ids = [fields.Command.clear()]
        new_invoice_lines = []

        for sale_order in self.related_sale_order_ids:
            for order_line in sale_order.order_line:
                invoice_line_vals = {
                    'product_id': order_line.product_id.id,
                    'quantity': order_line.product_uom_qty,
                    'price_unit': order_line.price_unit,
                    'tax_ids': [fields.Command.set(order_line.tax_id.ids)],
                    'price_subtotal': order_line.price_subtotal,
                    'sale_order_id': order_line.order_id.id,
                }
                new_invoice_lines.append(fields.Command.create(invoice_line_vals))
        if new_invoice_lines:
            self.update({'invoice_line_ids': new_invoice_lines})


    @api.depends('related_added_sale_order_ids')
    def _compute_origin_so_counts(self):
        """Compute the number of sales order selected."""
        for move in self:
            count = 0
            for sales_orders in self.related_added_sale_order_ids:
                if sales_orders:
                    count +=1
            move.sales_order_count = count

    def get_sales_orders(self):
        """Get connect the selected sale order using smart button."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'list,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', self.related_added_sale_order_ids.ids)],
            'context': "{'create': False }"
        }

    def action_post(self):
        """Method used for link the current invoice id with the selected sales orders."""
        res = super().action_post()
        for move in self:
            if move.related_sale_order_ids:
                for sale_order in move.related_sale_order_ids:
                    sale_order.order_line.invoice_status = 'invoiced'
        return res
