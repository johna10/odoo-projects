# -*- coding: utf-8 -*-
from odoo import fields,models


class SchoolClubs(models.Model):
    """This model is used to create clubs in school."""
    _name = 'school.club'
    _description = 'Club'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Name of Club')
    students_ids = fields.Many2many('student.registration',
                                       string='All Students', domain=[('state','=','registration')])
    events_count = fields.Integer(compute='_compute_events_count')
    users_id = fields.Many2one('res.partner',string='Leader', domain=[('partner', '=', 'student')])
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)


    def _compute_events_count(self):
        """Count & Show the number of event with respect to the club."""
        for record in self:
            record.events_count = self.env['school.event'].search_count(
                [('club_ids', 'in', self.ids)])

    def get_events(self):
        """Show all events linked to the club in list and form view."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'list,form',
            'res_model': 'school.event',
            'domain': [('club_ids', '=', self.ids)],
            'context': "{'create': False }"
        }
