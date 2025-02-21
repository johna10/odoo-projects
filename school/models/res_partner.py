# -*- coding: utf-8 -*-
from odoo import fields,models,Command


class SchoolTeacher(models.Model):
    """This model is used to create teachers, office-staff, Hod in school."""
    _inherit = 'res.partner'

    email = fields.Char(required=True)
    value = fields.Boolean(default=False)
    partner = fields.Selection([('teacher', 'Teacher'), ('student', 'Student'),
                                ('officestaff', 'Office Staff'), ('hod','Head of Department')],
                               string='Partner Type')
    user_id = fields.Many2one('res.users',string='Related User')
    company_id = fields.Many2one('res.company', copy=False,
                                 default= lambda self:self.env.company.id, readonly=True)

    def action_create_user_for_employee(self):
        """This method is used to create user for employee."""
        # user_ids = self.env['res.users'].search(['|', ('name', '=', self.name), ('email', '=', self.email)])
        # if not  user_ids:
        if self.partner == 'student':
            pass
        elif self.partner == 'teacher':
            user = self.env['res.users'].create([{
                'name': self.complete_name,
                'login': self.email,
                'partner_id': self.id,
                'groups_id': [
                    Command.link(self.env.ref('base.group_user').id),
                    Command.link(self.env.ref('school.teachers_group').id)],
            }])
            self.user_id = user.id
        else:
            user = self.env['res.users'].create([{
                'name': self.complete_name,
                'login': self.email,
                'partner_id': self.id,
                'groups_id': [
                    Command.link(self.env.ref('base.group_user').id),
                    Command.link(self.env.ref('school.staff_group').id)],
            }])
            self.user_id = user.id

    _sql_constraints = [
        ('unique_email_inherited', 'unique(email)', "A partner with same Email already exists!")
    ]

