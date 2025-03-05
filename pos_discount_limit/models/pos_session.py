from odoo import models,api,fields


class PosSession(models.Model):
    """Inherit pos.session to load product.brand data."""
    _inherit = 'pos.session'

    session_discount_balance = fields.Float(string='Limit amount', default=0.0, help='The discount limit in amount')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Method used to load the additonal field to the pos.session."""
        result = super()._load_pos_data_fields(config_id)
        result.append('session_discount_balance')
        return result

    @api.model
    def sample(self, session_id, value):
        """Method used to store update the session discount."""
        session = self.env['pos.session'].browse(session_id)
        if session:
            session.write({'session_discount_balance': value})

