from odoo import models, fields


class Screen(models.Model):
    _name = 'delegation.screen'
    _description = 'Screen'
    _rec_name = 'size'
    _table = 'delegation_screen'

    size = fields.Float(string='Screen Size in inches')

class Keyboard(models.Model):
    _name = 'delegation.keyboard'
    _description = 'Keyboard'
    _rec_name = 'layout'
    _table = 'delegation_keyboard'

    layout = fields.Char(string='Layout')

class Laptop(models.Model):
    _name = 'delegation.laptop'
    _description = 'Laptop'
    _table = 'delegation_laptop'


    _inherits = {
        'delegation.screen': 'screen_id',
        'delegation.keyboard': 'keyboard_id',
    }

    name = fields.Char(string='Name')
    maker = fields.Char(string='Maker')

    # a Laptop has a screen
    screen_id = fields.Many2one('delegation.screen', required=True, ondelete="cascade")
    # a Laptop has a keyboard
    keyboard_id = fields.Many2one('delegation.keyboard', required=True, ondelete="cascade")
    # select a product
    product_id = fields.Many2one('product.template', string='Product')
