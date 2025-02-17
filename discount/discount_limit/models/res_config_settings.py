# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """The model is used to add a discount limit feature within the sales settings."""
    _inherit = 'res.config.settings'

    is_discount_limit = fields.Boolean(string='Discount limit',
                                        config_parameter='sale_discount_limit.is_discount_limit',
                                        help='Check this field for enabling discount limit')
    discount_type = fields.Selection([('fixed','Fixed'), ('percentage','Percentage')])
    discount_fixed_limit = fields.Float(string='Limit amount',
                                        config_parameter='sale_discount_limit.discount_fixed_limit',
                                        help='The discount limit in amount')
    discount_percentage_limit = fields.Float(string='Limit Percentage %',
                                        config_parameter='sale_discount_limit.discount_percentage_limit',
                                        help='The discount limit in percentage')

    @api.model
    def get_values(self):
        """Method used to get values from res.config.settings"""
        res = super(ResConfigSettings, self).get_values()
        if self.discount_type == 'fixed':
            self.discount_percentage_limit = 0.0
        else:
            self.discount_fixed_limit = 0.0
        res['discount_type'] = self.env['ir.config_parameter'].sudo().get_param("base.discount_type", default="")
        return res

    @api.model
    def set_values(self):
        """Method used for setting the values to the configuration settings fields"""
        self.env['ir.config_parameter'].set_param("base.discount_type", self.discount_type or '')
        super(ResConfigSettings, self).set_values()


