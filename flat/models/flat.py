# -*- coding: utf-8 -*-
from odoo import fields, models


class Flat(models.Model):
    """This model is used to create flat."""
    _name = 'flat'
    _description = 'Flat'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    amount = fields.Float(string='Amount')
    flat_management_id = fields.Many2one('flat.management')

