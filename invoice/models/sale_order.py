from reportlab.rl_settings import strikeGap

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_ids = fields.Many2many('account.move', string='Invoices', compute='_get_invoiced')
    invoiced_ids = fields.Many2many('account.move', string='Invoiced')

    @api.depends('order_line.invoice_lines','invoiced_ids')
    def _get_invoiced(self):
        """Get the invoice from the invoicing module."""

        for order in self:
            if self.order_line.invoice_lines:
                print('from sales')
                invoices = order.order_line.invoice_lines.move_id.filtered(
                    lambda r: r.move_type in ('out_invoice', 'out_refund'))
                order.invoice_ids = invoices
                order.invoice_count = len(invoices)
            elif self.invoiced_ids:
                print('from invoice')
                invoices = order.invoiced_ids
                order.invoice_ids = invoices
                order.invoice_count = len(invoices)
                print(order.invoice_ids)
            else:
                print('not in two')
                invoices = order.invoiced_ids
                order.invoice_ids = invoices
                order.invoice_count = len(invoices)
                print(order.invoice_ids)



