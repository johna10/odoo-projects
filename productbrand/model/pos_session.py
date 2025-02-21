from odoo import models, fields

class PosSession(models.Model):
    """Class used for create brand for the products."""

    _inherit = 'pos.session'

    name = fields.Char(string='Brand Name')