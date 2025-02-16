# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolDepartment(models.Model):
    """This model is used to create departments."""
    _name = 'school.department'
    _inherit = 'mail.thread'
    _description = 'Department'

    name = fields.Char(string='Name')
    head_of_dpt_id = fields.Many2one('res.partner',
                                     string='Head of the Department', domain="[('partner','=','hod')]")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)
    class_ids = fields.One2many('school.class', 'department_id', string='Class')
    clubs_ids = fields.Many2many('school.club', string='Clubs')