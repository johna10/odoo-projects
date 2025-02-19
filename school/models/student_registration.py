# -*- coding: utf-8 -*-
from dateutil.utils import today
from odoo import fields, models, api, Command
from odoo.exceptions import UserError


class StudentRegistration(models.Model):
    """This model is used to register new student and take admission."""
    _name = 'student.registration'
    _inherit = 'mail.thread'

    user_id = fields.Many2one('res.users',string='Related User')
    registration_no = fields.Char(string="Registration No", readonly="1")
    name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(compute='_compute_full_name', string="Name of Student")
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    communication_address = fields.Text(string='Communication address')
    same_as_comm_add = fields.Boolean(string='Same communication address')
    permanent_address = fields.Char(string='Permanent Address')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    date_of_birth = fields.Date(string="Date of Birth", default=today())
    age = fields.Integer(string="Age",  compute='_compute_age')
    gender = fields.Selection(string="Gender", selection=[('male','Male'),('female','Female')])
    registration_date = fields.Date(string="Registration Date", default=today())
    photo = fields.Image(string="")
    pre_aca_dpt_id = fields.Many2one('school.department', string="Previous Academic Department")
    pre_class_id = fields.Many2one('school.class', string="Previous Class")
    tc = fields.Many2many('ir.attachment', string='TC')
    aadhaar_number = fields.Char(string='Aadhaar Number')
    state = fields.Selection([('draft','Draft'),('registration','Registration')],
                             string='Status', default='draft')
    current_date = fields.Date(default=fields.Date.context_today)
    admission_no = fields.Char(string='Admission Number')
    hide = fields.Boolean(default=True)
    clubs_ids = fields.Many2many('school.club',string='Clubs', title='IT IS USED TO MENTION THE CLUB FOR THE STUDENT ')
    class_id = fields.Many2one('school.class', string='Class')
    exam_ids = fields.Many2many('school.exam')
    attendance = fields.Selection([('present', 'Present'), ('absent', 'Absent')],
                             string='Attendance', default='present')
    leaves_ids = fields.One2many('school.leave', 'student_id', string='Leaves')
    company_id = fields.Many2one('res.company', copy=False, default=lambda self: self.env.company.id)

    def action_admission_button(self):
        """Change the state of the statusbar and create Admission sequence."""
        self.write({'state': 'registration'})
        self.admission_no = self.env['ir.sequence'].next_by_code('my_sequence_code_student_admission')

    @api.model
    def create(self, vals):
        """Create Registration sequence number to each record."""
        vals['registration_no'] = self.env['ir.sequence'].next_by_code('my_sequence_code_student_registration')
        return super(StudentRegistration, self).create(vals)

    @api.constrains('pre_aca_dpt_id','pre_class_id')
    def _check_department_class_match(self):
        """This method is used to check and validate the class with respect to department."""
        for record in self:
            if record.pre_class_id.department_id != record.pre_aca_dpt_id:
                raise UserError('Class and the previous year is not matching')

    @api.depends("date_of_birth")
    def _compute_age(self):
        """This method is used to auto-update the age field from the given date of birth."""
        for record in self:
            if record.date_of_birth:
                today = record.current_date
                dob = record.date_of_birth
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                print('age calculated')
            else:
                record.age = 0

    @api.depends('name','last_name')
    def _compute_full_name(self):
        """This method is used to combination the firstname and lastname."""
        for record in self:
            record.full_name = f"{record.name} {record.last_name}"

    def action_create_user_for_student(self):
        """This method is used to create user for student."""
        user_ids = self.env['res.users'].search(['|', ('name', '=', self.full_name), ('email', '=', self.email)])
        if self.state == 'registration' and not user_ids:
            user = self.env['res.users'].create([{
                'name': self.full_name,
                'login': self.email,
                'partner_id': self.env['res.partner'].create({
                    'name': self.full_name,
                    'email': self.email,
                    'partner': 'student',
                }).id,
                'groups_id': [
                    Command.link(self.env.ref('base.group_user').id),
                    Command.link(self.env.ref('school.students_group').id)],
            }])
            self.user_id = user.id

    def action_report(self):
        print('Button Click')
        return self.env.ref('school.action_student_report').report_action(self)

    _sql_constraints = [
        ('unique_aadhaar_number', 'unique (aadhaar_number)', 'This aadhaar number already exists!. Enter a unique one'),
        ('unique_email_inherited', 'unique(email)', "A student with same Email already exists!")
    ]


