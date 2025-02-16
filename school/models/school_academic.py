# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolAcademic(models.Model):
    """This model is used to create the Academic year."""
    _name = 'school.academic'
    _description = 'Academic Year'

    name = fields.Char(string='Name of Academic Year')
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)
