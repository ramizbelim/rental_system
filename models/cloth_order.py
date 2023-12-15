from odoo import models,fields,api
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

class ClothOrder(models.Model):
    _name = "cloth.orders"
    _description = " Cloth Rental Order"
    # _rec_name = "reciept_num"

    name = fields.Many2one("rent.customers",string="Customer",required=True)
    reciept_num = fields.Char('Order No.', copy=False, readonly=True)
    address = fields.Char(string="Address")
    delivery_address = fields.Char(string="Delivery Address",required=True)
    mobile = fields.Char(string="Mobile No.")
    product = fields.Selection([('men',"Men"),('women',"Women"),('children',"Children")],string="Product")
    order_date = fields.Date(string="Order Date")
    rental_period_start = fields.Date(string="From Date")
    rental_period_end = fields.Date(string="End Date")
    duration = fields.Integer(string = "Duration in Days",readonly=True)
    payment_method = fields.Selection([('upi',"UPI"),('cash',"Cash"),('debit_card',"Debit Card")],string="Payment Method")

    @api.onchange('rental_period_start','rental_period_end')
    def _onchange_duration(self):
        for rec in self:
           rec.duration= relativedelta(rec.rental_period_end, rec.rental_period_start).days

    @api.model
    def create(self, vals):
        vals['reciept_num'] = self.env['ir.sequence'].next_by_code('cloth.order.code')
        return super(ClothOrder,self).create(vals)
    @api.model
    def create(self,vals):
        # self.env["rent.customers"].create({
        #     "name": self.name,
        #     "address": self.address,
        #     "mobile": self.mobile
        # })
        print("--------------------",self)
        return super(ClothOrder, self).create(vals)



