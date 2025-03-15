# -*- coding: utf-8 -*-
from odoo import models, fields


class DashboardComment(models.Model):
    """Class used to store and fetch the comments to the photos."""
    _name = 'dashboard.comment'


    name = fields.Char(string="Comment")


