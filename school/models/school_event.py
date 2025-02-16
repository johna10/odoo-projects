# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import fields,models,api


class SchoolEvent(models.Model):
    """ This model is used to create events in school."""
    _name = 'school.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name of Event')
    club_ids = fields.Many2many('school.club', string='Club')
    state = fields.Selection(string='Status', selection=[('ready','Ready'),('ongoing','Ongoing'),('end','Ended')])
    start_date = fields.Datetime(string='Start Date', default=today())
    end_date = fields.Datetime(string='End Date', default=today())
    responsible_person_id = fields.Many2one("res.partner", string="Responsible", index=True, tracking=True,
                                         domain=[('partner','=','hod')])
    venue = fields.Char(string='Venue')
    description = fields.Char(string='Description')
    current_day = fields.Datetime.today()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)

    @api.onchange('start_date', 'end_date')
    def _onchange_start_date(self):
        """Change the status of the leave on creation."""
        if self.start_date > self.current_day:
            self.state = 'ready'
        elif self.start_date <= self.current_day <= self.end_date:
            self.state = 'ongoing'
        else:
            self.state = 'end'

    def event_archive(self):
        """This method is for archive the occurred events and sent notification to employees."""
        records = self.search([])
        partner_ids = (self.env['res.partner'].search
                       (['|', ('partner', '=', 'teacher'), ('partner', '=', 'officestaff')]))
        email_list = ','.join(partner_ids.mapped('email'))
        for record in records:
            if record.start_date > record.current_day:
                record.state = 'ready'
            elif record.start_date <= record.current_day <= record.end_date:
                record.state = 'ongoing'
            else:
                record.active = False
                record.state = 'end'

            # sent notification to employees two days before
            if record.start_date <= record.end_date:
                num_of_days = (record.start_date - record.current_day).days
                if num_of_days == 2:
                    mail_template = self.env.ref('school.event_mail_template')
                    mail_template.email_to = email_list
                    mail_template.send_mail(record.id, force_send=True)





