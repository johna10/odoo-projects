from odoo import models, fields, api

class HospitalConsultation(models.Model):
    _name = 'hospital.diagnosis'
    _description = "prescription"

    prescription = fields.Many2one('hospital.consultation')
    medicine = fields.Many2one("product.product")
    dose = fields.Char(string='Dose')
    quantity = fields.Integer(string='Qty')