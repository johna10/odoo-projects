from odoo import fields, models,api


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one('product.brand', string="Brand")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Method used to load the additonal field to the pos.session."""
        result = super()._load_pos_data_fields(config_id)
        result.append('brand_id')
        return result