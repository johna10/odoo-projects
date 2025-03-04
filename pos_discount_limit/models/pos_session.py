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
        print('RRRR')
        print(self.session_discount_balance)
        return result

    @api.model
    def sample(self, session_id, value):
        print('Sample', value)
        print('Session Id', session_id)

        # Get the active POS session
        session = self.env['pos.session'].browse(session_id)
        if session:
            print("Before Update:", session.session_discount_balance)
            # Update the session's discount balance
            session.write({'session_discount_balance': value})
            print("Updated Session Limit:", session.session_discount_balance)
        else:
            print("No active POS session found!")

