from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


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
    order_details = fields.Many2many("product.management",string="Order Details")
    @api.model
    def create(self, vals):
        vals['invoice_number'] = self.env['ir.sequence'].next_by_code('customers.invoice.code')
        invoice_search = self.env["customers.invoice"].search([('name','=',vals["name"])])
        store = []
        for i in invoice_search:
            store.append(i)
        if store == []:
            return super(Invoice, self).create(vals)
        else:
            raise ValidationError("Invoice already generated!!")


        # return super(Invoice, self).create(vals)

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

    # @api.model
    # def default_get(self, fields_list):
    #     record = self.env["cloth.orders"].search([('name','=',self.name.name)])
    #     res = super().default_get(fields_list)
    #     res["order_details"] = record.name.name
    #     print("9999999999",res)
    #     print("9999999999",record)
    @api.onchange('name')
    def onchange_order_details(self):
        order = self.env["cloth.orders"].search([('name','=',self.name.name)])
        if order.ids != []:
            for rec in order:
                self.order_details += rec.my_product_ids
        else:
            raise ValidationError("Any cloth not given to this customer yet!!")


