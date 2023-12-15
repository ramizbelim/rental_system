from odoo import models, fields, api

class Invoice(models.Model):
    _name = "customers.invoice"

    name = fields.Many2one("rent.customers",string="Customers",required=True)
    address = fields.Char(string="Address")
    invoice_number = fields.Char()
    invoice_date = fields.Date(string="Date")
    payment_terms = fields.Char(string="Payment terms")
    currency = fields.Selection([('usd',"USD"),('inr',"INR"),("aus","AUS")],string="Currency")

    @api.model
    def create(self, vals):
        vals['invoice_number'] = self.env['ir.sequence'].next_by_code('customers.invoice.code')
        return super(Invoice, self).create(vals)
