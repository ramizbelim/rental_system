from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'
