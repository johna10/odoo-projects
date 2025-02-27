from odoo import models,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        """Load the data into pos.config.models"""
        data = super()._load_pos_data_models(config_id)
        data += ['pos.config']
        return data
    #
    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     """Method used to load the additonal field to the pos.session."""
    #     result = super()._load_pos_data_fields(config_id)
    #     result.append('is_discount_limit',
    #                   'discount_type',
    #                   'discount_fixed_limit',
    #                   'discount_percentage_limit')
    #     return result
