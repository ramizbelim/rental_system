from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class ClothOrder(models.Model):
    _name = "cloth.orders"
    _description = "Cloth Rental Order"
    # _rec_name = "reciept_num"

    name = fields.Many2one("rent.customers", string="Customer", required=True)
    reciept_num = fields.Char('Order No.', copy=False, readonly=True)
    address = fields.Char(string="Address", related="name.address", store=True)
    same_as_address = fields.Boolean(string="Same as above?")
    delivery_address = fields.Char(string="Delivery Address", required=True)
    mobile = fields.Integer(string="Mobile No.", related="name.mobile", store=True)
    category = fields.Selection([('men',"Men"),
                                 ('women',"Women"),
                                 ('children',"Children")],
                                string="Category")
    order_date = fields.Date(string="Order Date")
    rental_period_start = fields.Date(string="From Date")
    rental_period_end = fields.Date(string="End Date")
    duration = fields.Integer(string = "Duration in Days", store=True)
    payment_method = fields.Selection([('upi',"UPI"),
                                       ('cash',"Cash"),
                                       ('debit_card',"Debit Card")],
                                      string="Payment Method")
    my_product_ids = fields.Many2many("product.management", string="Product")
    price_subtotal = fields.Integer(string="Subtotal")

    @api.onchange('rental_period_start','rental_period_end')
    def _onchange_duration(self):
        for rec in self:
           rec.duration= relativedelta(rec.rental_period_end, rec.rental_period_start).days

    @api.model
    def create(self, vals):
        print("---------------------------",vals)
        vals['reciept_num'] = self.env['ir.sequence'].next_by_code('cloth.order.code')
        return super(ClothOrder,self).create(vals)

    @api.model
    def write(self,vals):
        print("========================",vals)
        return super(ClothOrder,self).write(vals)

    @api.onchange('same_as_address')
    def _onchange_address(self):
        for rec in self:
            if rec.same_as_address:
                rec.delivery_address = rec.address

    # @api.model
    # def create(self,vals):
    #     # self.env["rent.customers"].create({
    #     #     "name": self.name,
    #     #     "address": self.address,
    #     #     "mobile": self.mobile
    #     # })
    #     print("-------------------------------------------",vals)
    #     return super(ClothOrder, self).create(vals)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         if operator in ('=', '!='):
    #             domain = ['|', ('code', '=', name.split(' ')[0]), ('name', operator, name)]
    #         else:
    #             domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
    #     return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)






