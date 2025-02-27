# -*- coding: utf-8 -*-
from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    """The model is used to add a discount limit feature within the pos settings."""
    _inherit = 'res.config.settings'

    pos_is_discount_limit = fields.Boolean(string='Discount limit KKi',
                                        related='pos_config_id.is_discount_limit', readonly=False,
                                        help='Check this field for enabling discount limit')
    pos_discount_type = fields.Selection([('fixed','Fixed'), ('percentage','Percentage')],
                                        related='pos_config_id.discount_type', readonly=False)
    pos_discount_fixed_limit = fields.Float(string='Limit amount',
                                        related='pos_config_id.discount_fixed_limit', readonly=False,
                                        help='The discount limit in amount')
    pos_discount_percentage_limit = fields.Float(string='Limit Percentage %',
                                        related='pos_config_id.discount_percentage_limit', readonly=False,
                                        help='The discount limit in percentage')

    # pos_config_id

    # @api.model
    # def get_values(self):
    #     """Method used to get values from res.config.settings"""
    #
    #     print('Inside the get values')
    #     res = super(ResConfigSettings, self).get_values()
    #     if self.pos_discount_type == 'fixed':
    #         self.pos_discount_percentage_limit = 0.0
    #     else:
    #         self.pos_discount_fixed_limit = 0.0
    #     res['pos_discount_type'] = self.env['ir.config_parameter'].sudo().get_param("base.pos_discount_type", default="")
    #     return res
    #
    # @api.model
    # def set_values(self):
    #     """Method used for setting the values to the configuration settings fields"""
    #
    #     print('Set values inside ')
    #     self.env['ir.config_parameter'].set_param("base.pos_discount_type", self.pos_discount_type or '')
    #     super(ResConfigSettings, self).set_values()


