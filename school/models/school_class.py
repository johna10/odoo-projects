# -*- coding: utf-8 -*-
from odoo import fields, models


class SchoolClass(models.Model):
    """This model is used to create class in school."""
    _name = 'school.class'
    _inherit = 'mail.thread'
    _description = 'Class'

    name = fields.Char(string='Name')
    department_id = fields.Many2one('school.department', string='Department')
    head_of_department_id = fields.Many2one(related='department_id.head_of_dpt_id',string='Head of the Department')
    student_ids = fields.One2many('student.registration',
                                  'class_id', domain=[('state','=','registration')])
    class_teacher_id = fields.Many2one('res.partner',
                                    domain=[('partner','=','teacher')], string="Class Teacher")
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)

