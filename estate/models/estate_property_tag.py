from odoo import fields,models
class EstatePropertyTags(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tags'

    name = fields.Char('Name', required=True)