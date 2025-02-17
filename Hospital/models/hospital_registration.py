from dateutil.utils import today

from odoo import fields, models, api
from odoo import models, fields

class Registration(models.Model):
    _inherit = "res.partner"
    _description = "registration_details"

    age = fields.Integer(string="Age", compute='_autoagecalculator_')
    date_of_birth = fields.Date(string="DOB")
    gender = fields.Selection(string="Gender", selection=[('male','Male'),('female','Female')])
    patient_id = fields.Integer(string='Id')
    current_date = fields.Date(default=fields.Date.context_today)
    blood_group = fields.Selection(string="Blood Group", selection=[('a+','A+'),('a','A'),('b+','B+'),('ab+','AB+'),('ab','AB'),('o','O'),('o+','O+')])

    @api.depends("date_of_birth")
    def _autoagecalculator_(self):
        for record in self:
            if record.date_of_birth:
                today = record.current_date
                dob = record.date_of_birth
                record.age = today.year - dob.year - ((today.month, today.day)<(dob.month,dob.day))
            else:
                record.age = 0

    _sql_constraints = [
        ('patient_id', 'UNIQUE(patient_id)', 'Enter the unique Id for each patient.'),
    ]
