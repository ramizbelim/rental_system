from datetime import datetime

from odoo import models, fields, api


class ClothWashing(models.Model):
    _name = "cloth.washing"
    _description = "Cloth Washing Details"

    name = fields.Char(string="Washer Name")
    date = fields.Date(string="Date", default=datetime.now())
    washing_qty = fields.Integer(string="Quantity")
    rate = fields.Integer(string="Washing Rate")
    final_price = fields.Integer(string="Final Price")
    @api.onchange('washing_qty', 'rate')
    def _onchange(self):
        for rec in self:
            if rec.washing_qty:
                rec.final_price = rec.washing_qty * rec.rate
