# -*- coding: utf-8 -*-
from odoo import fields,models


class SchoolPaper(models.Model):
    """This model is used to create paper."""
    _name = 'school.paper'
    _description = 'Paper'

    subject_id = fields.Many2one('school.subject', string='Subject')
    pass_mark = fields.Integer(string='Pass Mark')
    max_mark = fields.Integer(string='Max Mark')
    exam_id = fields.Many2one('school.exam',string='Exam')
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)



