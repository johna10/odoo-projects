from odoo import fields,models
class EstatePropertyTypes(models.Model):
    _name = 'estate.property.type'
    _description = 'Property types'

    name = fields.Char('Name', required=True)