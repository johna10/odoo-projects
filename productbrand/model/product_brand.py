from odoo import models, fields

class ProductBrand(models.Model):
    """Class used for create brand for the products."""

    _name = 'product.brand'
    _description = 'Create Brands for products'

    name = fields.Char(string='Brand Name')