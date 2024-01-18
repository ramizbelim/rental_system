from odoo import models, fields, api
from datetime import datetime

class Invoice(models.Model):
    _name = "customers.invoice"

    name = fields.Many2one("rent.customers", string="Customers", required=True)
    address = fields.Char(string="Address", related="name.address", store=True)
    mobile = fields.Char(string="Mobile", related="name.mobile", store=True)
    invoice_number = fields.Char()
    invoice_date = fields.Date(string="Date",default=datetime.today())
    payment_terms = fields.Char(string="Payment terms")
    currency = fields.Selection([('usd', "USD"),
                                 ('inr', "INR"),
                                 ("aus", "AUS")],
                                string="Currency", default='inr')
    email = fields.Char("Email")
    @api.model
    def create(self, vals):
        vals['invoice_number'] = self.env['ir.sequence'].next_by_code('customers.invoice.code')
        return super(Invoice, self).create(vals)

    # def _button_check_orm(self):
    #     # customer = self.env['customers.invoice'].search([])
    #     # print("+++++++++++++++++++++++++++++++++++",customer)
    #     for rec in self:
    #         rec.address="ramizlala 12345"
    #         print("+++++++++++++++++++++++", rec.address)

    #Send Email invoice
    def send_by_email(self):
        mail_template = self.env.ref('rental_system.cloth_order_mail_template')
        for rec in self:
            mail_template.send_mail(rec.id, force_send=True)

