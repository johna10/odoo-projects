import datetime
from email.policy import default
from operator import index
from types import LambdaType

from odoo import models, fields, api
from odoo.api import readonly


class OpTicket(models.Model):
    _name = 'op.ticket'
    _description = 'OP Ticket'
    _rec_name = 'serial_no'

    serial_no = fields.Char(string="Serial No")
    patient_name = fields.Many2one("res.partner")
    age = fields.Integer(related='patient_name.age')
    patient_gender = fields.Selection(related='patient_name.gender')
    doctor_name = fields.Many2one('hr.employee', required=True)
    date_and_time =fields.Datetime(default=datetime.datetime.now())
    token_id = fields.Integer(string="Token ID")

    company_id = fields.Many2one('res.company', store=True, copy=False, string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id', default=lambda self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(related='doctor_name.hourly_cost',string="Fee")

    @api.model
    def create(self, vals):
        vals['serial_no'] = self.env['ir.sequence'].next_by_code('my_sequence_code_opticket')
        return super(OpTicket, self).create(vals)



    _sql_constraints = [
        ('token_id', 'UNIQUE(token_id)', 'Enter the UNIQUE Token NO.'),
    ]