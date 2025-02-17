from odoo import models, fields, api

class HospitalConsultation(models.Model):
    _name = 'hospital.consultation'
    _description = "consult"
    _rec_name = 'consult_serial_no'


    consult_serial_no = fields.Char(string='Serial No')
    op_ticket = fields.Many2one("op.ticket")
    patient = fields.Many2one(related='op_ticket.patient_name')
    doctor = fields.Many2one(related='op_ticket.doctor_name')
    gender = fields.Selection(related='op_ticket.patient_gender')
    age = fields.Integer(related='op_ticket.age')
    prescription_id = fields.One2many('hospital.diagnosis','prescription')

    @api.model
    def create(self, vals):
        vals['consult_serial_no'] = self.env['ir.sequence'].next_by_code('my_sequence_code_consultation')
        return super(HospitalConsultation, self).create(vals)