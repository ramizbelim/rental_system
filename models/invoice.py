from odoo import models, fields, api


class Invoice(models.Model):
    _name = "customers.invoice"

    name = fields.Many2one("rent.customers", string="Customers", required=True)
    address = fields.Char(string="Address", related="name.address", store=True)
    mobile = fields.Integer(string="Mobile", related="name.mobile", store=True)
    invoice_number = fields.Char()
    invoice_date = fields.Date(string="Date")
    payment_terms = fields.Char(string="Payment terms")
    currency = fields.Selection([('usd', "USD"),
                                 ('inr', "INR"),
                                 ("aus", "AUS")],
                                string="Currency", default='inr')

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
