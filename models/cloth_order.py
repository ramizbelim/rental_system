from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class ClothOrder(models.Model):
    _name = "cloth.orders"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cloth Rental Order"
    # _rec_name = "reciept_num"

    name = fields.Many2one("rent.customers", string="Customer", required=True)
    reciept_num = fields.Char('Order No.', copy=False, readonly=True)
    address = fields.Char(string="Address", related="name.address", store=True)
    same_as_address = fields.Boolean(string="Same as above?")
    delivery_address = fields.Char(string="Delivery Address", required=True)
    mobile = fields.Char(string="Mobile No.", related="name.mobile", store=True)
    category = fields.Selection([('t_shirt', "T-Sirt"),
                                 ('shirt', "Shirt"),
                                 ('pent', "Pent"),
                                 ('pathani', "Pathani"),
                                 ('trouser', "Trousers"),
                                 ('blazer', "Blazer")],
                                string="Category")
    order_date = fields.Datetime(string="Order Date", default=datetime.now())
    rental_period_start = fields.Date(string="From Date")
    rental_period_end = fields.Date(string="End Date")
    duration = fields.Integer(string="Duration in Days", store=True)
    payment_method = fields.Selection([('upi', "UPI"),
                                       ('cash', "Cash"),
                                       ('debit_card', "Debit Card")],
                                      string="Payment Method",
                                      compute="_compute_track_feilds",
                                      store=True,
                                      readonly=False)
    my_product_ids = fields.Many2many("product.management", string="Product")
    price_subtotal = fields.Integer(string="Total", store=True, related="my_product_ids.sum_one", tracking=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')],
        string='Status', required=True, readonly=True, copy=False,
        default='draft')
    active = fields.Boolean('Active', default=True)

    @api.model
    def default_get(self, fields):
        res = super(ClothOrder, self).default_get(fields)
        date_today = date.today()
        print(date_today)
        res['rental_period_start'] = date.today()
        res['rental_period_end'] = date.today()
        # res['order_date'] = datetime.now()
        print(res)
        # return {"rental_period_start": date.today(), "rental_period_end": date.today()}
        data = self.search([]).read(['reciept_num'])
        # data = self.env['res.partner'].read_group([], ['phone'],['phone'])
        # data = self.env['rent.customers'].search_read([('identity','=','pan')], ['identity'])
        print("++++++++++++++++++++++\n", data)
        return res

    @api.onchange('rental_period_start', 'rental_period_end')
    def onchange_duration(self):
        for rec in self:
            rec.duration = relativedelta(rec.rental_period_end, rec.rental_period_start).days

    @api.model
    def create(self, vals):
        print("---------------------------", vals)
        vals['reciept_num'] = self.env['ir.sequence'].next_by_code('cloth.order.code')
        vals["state"] = "done"
        return super(ClothOrder, self).create(vals)

    def write(self, vals):
        print("========================", vals)
        return super(ClothOrder, self).write(vals)

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
    def click_chatter(self):
        self.message_post(body="Hello, Buuton Clicked")
        
    # def write(self, vals):
    #     if 'upi' in vals:
    #         # new_value = vals['upi']
    #         # old_value = self.payment_method
    #         # if new_value != old_value:
    #         message_body = _("%(user)s changed the Name to %(user_name)s",
    #                              user=self.env.user.name,
    #                              user_name=self.env['cloth.order'].search(domain=[('id', '=', self.payment_method)]).payment_method)
    #         self.message_post(body=message_body, message_type='notification')
    #     res = super().write(vals)
    #     return res


