# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolSubject(models.Model):
    """This model is used to create subject."""
    _name = 'school.subject'
    _description = 'Subject'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    department_ids = fields.Many2many('school.department')
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)
