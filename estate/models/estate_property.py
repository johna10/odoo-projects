from email.policy import default

from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property details'

    name = fields.Char('Name', required=True,widget="char")
    description = fields.Text('Description', required=True)
    postcode = fields.Char('Postcode')
    active = fields.Boolean()
    date_availability = fields.Date(copy=False, default=today()+relativedelta(months=3) )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly="1", copy=False, default=0)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Type', selection=[('east','East'),('west','West'),('north','North'),('south','South')])
    state = fields.Selection(string='State', selection=[('new','New'),('offerreceived','Offer Received'),('offeraccepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')], default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    salesperson = fields.Many2one("res.users", string="Salesperson", index=True, tracking=True, default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag",string="")
    offer_id = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Float(compute="_compute_total")
    best_offer = fields.Float(compute='_best_price')

    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_id")
    def _best_price(self, record=None):
        for record in self:
            record.best_offer=max(record.offer_id.mapped("price")) if record.offer_id else 0

    @api.onchange("garden")
    def _onchange_garden_(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_action(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("It is a cancelled property")
            else:
                record.state = "sold"

    def cancel_action(self):
        for record in self:
            if record.state == "sold":
                raise UserError("It is already sold")
            else:
                record.state = "cancelled"

#     CONSTRAINTS

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)','The expected price should be a positive value.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price should be between a positive value.')
    ]

