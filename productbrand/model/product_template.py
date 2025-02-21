from odoo import fields, models


class ProductTemplate(models.Model):
    """Class used for inherit the product model"""
    _name = 'product.template'
    _inherit = 'product.template'

    brand = fields.Many2one('product.brand',string="Brand")