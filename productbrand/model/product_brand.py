from odoo import models, fields,api

class ProductBrand(models.Model):
    """Class used for creating brands for products and loading them into the POS."""
    _name = 'product.brand'
    _description = 'Create Brands for Products'
    _rec_name = 'brand'
    _inherit = ['pos.load.mixin']

    brand = fields.Char(string='Brand Name')

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'brand']  # Fix: 'brand' instead of 'name'
