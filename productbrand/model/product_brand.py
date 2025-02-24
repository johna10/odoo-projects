from odoo import models, fields,api

class ProductBrand(models.Model):
    """Class used for create brand for the products, and load to the POS."""

    _name = 'product.brand'
    _description = 'Create Brands for products'
    _rec_name = 'brand'
    _inherit = ['pos.load.mixin']

    brand = fields.Char(string='Brand Name')

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        result.append('brand')
        return result