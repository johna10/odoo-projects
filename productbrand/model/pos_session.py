from odoo import models,api,fields


class PosSession(models.Model):
    """Inherit pos.session to load product.brand data."""
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        """Load the data into pos.config.models"""
        data = super()._load_pos_data_models(config_id)
        data += ['product.brand']
        return data

