from odoo import models,api,fields


class PosSession(models.Model):
    """Inherit pos.session to load product.brand data."""
    _inherit = 'pos.session'

    session_discount_balance = fields.Float(string='Limit amount',related='config_id.discount_fixed_limit', help='The discount limit in amount')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Method used to load the additonal field to the pos.session."""
        result = super()._load_pos_data_fields(config_id)
        result.append('session_discount_balance')
        return result

    def sample(self):
        return self.session_discount_balance