from odoo import models, fields,api

class ProductBrand(models.Model):
    """Class used for creating brands for products and loading them into the POS."""
    _name = 'product.brand'
    _description = 'Create Brands for Products'
    _inherit = ['pos.load.mixin']

    name = fields.Char(string='Brand Name')

