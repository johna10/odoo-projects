# -*- coding: utf-8 -*-
from odoo import fields,models


class SchoolExam(models.Model):
    """This model is used to create exams in school."""
    _name = 'school.exam'
    _inherit = 'mail.thread'

    name = fields.Char(string='Name')
    class_id = fields.Many2one('school.class',string='Class', required=True)
    papers_ids = fields.One2many('school.paper','exam_id', string='Papers')
    hide = fields.Boolean()
    state = fields.Selection([('draft','Draft'),('announced','Announced'),
                              ('end','End'),('cancelled','Cancelled')], default='draft')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)


    def action_assign_to_student(self):
        """Assign the exams to corresponding students in same class."""
        # same_class_student_records = self.env['student.registration'].search([('class_id','=',self.class_id.id)])
        for record in self.class_id.student_ids:
            record.exam_ids = [(fields.Command.link(self.id))]
        if self.start_date and self.end_date:
            self.state = 'announced'
            self.hide = True

    def action_cancel_exam(self):
        """This method is used to cancel the exam."""
        same_class_student_ids = self.class_id.student_ids
        for record in same_class_student_ids:
            record.exam_ids = [(fields.Command.unlink(self.id))]
        self.state = 'cancelled'

    def validate_exam_end_date(self):
        """This method is used to change the state of the exam to end after the end date."""
        current_day = fields.Date.today()
        records = self.search([])
        for record in records:
            if record.end_date == current_day:
                record.state = 'end'







