from odoo import models, fields

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_ui_models_to_load(self):
        """Extend POS data loading to include custom fields"""
        result = super()._pos_ui_models_to_load()
        result.append('pos.config')  # Ensure pos.config is loaded
        return result

    def _loader_params_pos_config(self):
        """Ensure the fields are sent to the POS frontend"""
        result = super()._loader_params_pos_config()
        result['search_params']['fields'].extend([
            'is_discount_limit',
            'discount_type',
            'discount_fixed_limit',
            'discount_percentage_limit',
        ])
        return result
