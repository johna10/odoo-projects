# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.utils import today
from odoo import fields,models,api


class SchoolLeaves(models.Model):
    """This model is used to create leave for the students."""
    _name = 'school.leave'
    _inherit = 'mail.thread'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.registration', string='Student',
                                 domain=[('state','=','registration')], ondelete='cascade', required=True)
    student_class_id = fields.Many2one(related='student_id.class_id',string='Class')
    start_date = fields.Datetime(default=today())
    end_date = fields.Datetime(default=today())
    total_days = fields.Float(default=0, string='Total Days', compute='_compute_total_days')
    half_days = fields.Boolean(string='Half Days')
    state = fields.Selection([('fn','FN'),('an','AN')], string='Time of Day')
    reason = fields.Char(string='Reason', required=True)
    status = fields.Selection([('upcoming','Upcoming'),('ongoing','Ongoing'),('end','End')])
    current_day = fields.Datetime.today()
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)

    @api.depends('start_date', 'end_date', 'half_days')
    def _compute_total_days(self):
        """Calculate the total number of weekdays between start_date and end_date, excluding weekends."""
        for record in self:
            if record.half_days:
                record.total_days = 0.5
                start_date_hour = record.start_date.hour
                if 0 < start_date_hour < 13:
                    record.state = 'fn'
                else:
                    record.state = 'an'
            elif record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    record.total_days = 0
                else:
                    current_date = record.start_date
                    total_days = 0
                    while current_date <= record.end_date:
                        if current_date.weekday() not in (5, 6):
                            total_days += 1
                        current_date += timedelta(days=1)
                    record.total_days = total_days

    def leave_status(self):
        """This method is used to change the status of the leave."""
        records = self.search([])
        for record in records:
            if record.start_date > record.current_day:
                record.status = 'upcoming'
            elif record.start_date <= record.current_day <= record.end_date:
                record.status = 'ongoing'
            else:
                record.status = 'end'

    @api.onchange('start_date','end_date')
    def _onchange_start_date(self):
        """Change the status of the leave on creation."""
        if self.start_date > self.current_day:
            self.status = 'upcoming'
        elif self.start_date <= self.current_day <= self.end_date:
            self.status = 'ongoing'
        else:
            self.status = 'end'

    def attendance_marking(self):
        """This method is used to autocheck the student is present or absent """
        records = self.search([])
        for rec in records:
            if rec.status == 'ongoing':
                rec.student_id.attendance ='absent'
            else:
                rec.student_id.attendance ='present'

    _sql_constraints = [
        ('check_total_days', 'CHECK(total_days >= 0.5)', 'Minimum leave at least be 0.5.')
    ]


