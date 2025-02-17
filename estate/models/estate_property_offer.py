from email.policy import default
from datetime import date

from odoo.exceptions import UserError
from odoo.tools import date_utils

from odoo import fields,models, api
class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property tags'

    price = fields.Float()
    status = fields.Selection(string='Status', selection=[('accepted','Accepted'),('refused','Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    create_date = fields.Date(default=fields.Date.context_today)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_deadline_", inverse="_inverse_deadline_")


    @api.depends("validity","create_date")
    def _deadline_(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_deadline_(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity=(record.date_deadline - record.create_date).days
            else:
                record.validity = 0

    def accepted(self):
        for record in self:
            if "accepted" not in record.property_id.offer_id.mapped('status'):
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
            else:
                raise UserError("Invalid")

    def refused(self):
        for record in self:
            record.status = 'refused'
            record.property_id.selling_price = 0
            record.property_id.buyer = False