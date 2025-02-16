# -*- coding: utf-8 -*-
import typing
from odoo import fields, models, api


class SaleOrder(models.Model):
    """This model is used to add a new state to sales order."""
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[('admitted', 'Admitted'), ('approval', 'Approval'), ('sent', 'Quotation Sent')])


