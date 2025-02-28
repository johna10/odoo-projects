from odoo import fields, models, api


class PosConfig(models.Model):
    """The model is used to add fields for limit discount in res.config model."""
    _inherit = 'pos.config'

    is_discount_limit = fields.Boolean(string='Discount limit')
    discount_type = fields.Selection([('fixed','Fixed'), ('percentage','Percentage')])
    discount_fixed_limit = fields.Float(string='Limit amount', help='The discount limit in amount')
    discount_percentage_limit = fields.Float(string='Limit Percentage %', help='The discount limit in percentage')
