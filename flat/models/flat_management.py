# -*- coding: utf-8 -*-
from odoo import fields, models


class FlatManagement(models.Model):
    """This model is used to create flat management."""
    _name = 'flat.management'
    _description = 'Flat'

    name = fields.Char(string='Customer')
    address = fields.Char(string='Address')
    flat_ids = fields.One2many('flat','flat_management_id', string='Flats')

