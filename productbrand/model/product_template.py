from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Many2one('product.brand', string="Brand")