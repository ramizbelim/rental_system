from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from lxml import etree

class ClothOrder(models.Model):
    _name = "cloth.orders"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cloth Rental Order"
    # _rec_name = "reciept_num"

    name = fields.Many2one('rent.customers', string="Customer", required=True)
    reciept_num = fields.Char('Order No.', copy=False, readonly=True)
    address = fields.Char(string="Address", related="name.address", store=True, readonly=False)
    same_as_address = fields.Boolean(string="Same as above?")
    delivery_address = fields.Char(string="Delivery Address")
    mobile = fields.Char(string="Mobile No.", related="name.mobile", store=True,readonly=False)
    email = fields.Char(string="Email")
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
    # state = fields.Selection(selection=[
    #     ('draft', 'Draft'),
    #     ('in_progress', 'In Progress'),
    #     ('cancel', 'Cancelled'),
    #     ('done', 'Done')],
    #     string='Status', required=True, readonly=True, copy=False,
    #     default='draft')
    active = fields.Boolean('Active', default=True)
    image = fields.Binary('Image')

    @api.model
    def default_get(self, fields):
        res = super(ClothOrder, self).default_get(fields)
        date_today = date.today()
        res['rental_period_start'] = date.today()
        res['rental_period_end'] = date.today()
        # res['order_date'] = datetime.now()
        # return {"rental_period_start": date.today(), "rental_period_end": date.today()}
        data = self.search([]).read(['reciept_num'])
        # data = self.env['res.partner'].read_group([], ['phone'],['phone'])
        # data = self.env['rent.customers'].search_read([('identity','=','pan')], ['identity'])
        return res

    @api.onchange('rental_period_start', 'rental_period_end')
    def onchange_duration(self):
        for rec in self:
            rec.duration = relativedelta(rec.rental_period_end, rec.rental_period_start).days

    @api.model
    def create(self, vals):
        vals['reciept_num'] = self.env['ir.sequence'].next_by_code('cloth.order.code')
        return super(ClothOrder, self).create(vals)

    @api.onchange('same_as_address')
    def _onchange_address(self):
        for rec in self:
            if rec.same_as_address:
                rec.delivery_address = rec.address

    def generate_invoice(self):
        invoice_search = self.env["customers.invoice"].search([('name', '=', self.name.id)])
        store = []
        for i in invoice_search:
            store.append(i)
        if store == []:
            self.env["customers.invoice"].create({
                "name": self.name.id,
                "address": self.delivery_address,
                "mobile": self.mobile,
                "invoice_date": self.order_date
            })
        else:
            raise ValidationError("Invoice Already generated!!!!!")

    def click_chatter(self):
        self.message_post(body="Hello, Button Clicked")

    def write(self, vals):
        selection_display_name = dict(self._fields['payment_method'].selection)
        user = self.env.user.name
        old_name = self.payment_method
        if "payment_method" in vals:
            message_body = (
                f"{user} changed the {selection_display_name[old_name]} to {selection_display_name[vals['payment_method']]}")
            self.message_post(body=message_body)

        # for rec in self:
        #     if rec.image:
        #         count = 0
        #         message_write = (f"{count} image uploaded")
        #         self.message_post(body=message_write)
        
        return super(ClothOrder, self).write(vals)

    def send_mail_cloth_orders(self):
        mail_template = self.env.ref('rental_system.cloth_order_mail_template_notification')
        records = self.search([])
        for rec in records:
            if (date.today() == rec.rental_period_end - relativedelta(days=1)) or (
                    date.today() == rec.rental_period_end + relativedelta(
                    days=1)) or date.today() == rec.rental_period_end:
                for record in records:
                    mail_template.send_mail(record.id, force_send=True)

    def order_confirm(self):
        # for rec in self.my_product_ids:
        #     product = self.env["product.management"].search([('prod_id', '=', rec.prod_id)])
        #     if self.my_product_ids:
        #         if rec.quantity==0:
        #             return self.call_wizard()
        #         else:
        #             product.quantity -=1
        # for rec in self.my_product_ids:

        self.write({
                    "name": self.name.id,
                    "address": self.delivery_address,
                    "mobile": self.mobile,
                    "delivery_address": self.delivery_address,
                    "address": self.address,
                    "email": self.email,
                    "category": self.category,
                    "order_date": self.order_date,
                    "rental_period_start": self.rental_period_start,
                    "rental_period_end": self.rental_period_end,
                    "duration": self.duration,
                    "my_product_ids": self.my_product_ids.ids
                })
        self.env["rent.customers"].search([("name", '=', self.name.name)]).update({
            'cloth_order': [(fields.Command.set([rec.id for rec in self.my_product_ids]))]
        })
        for rec in self.my_product_ids:
            print("-----------",rec.id)

            # 'cloth_order': [(4,self.my_product_ids.ids)]


    @api.model
    def default_get(self,fields_list):
        return super(ClothOrder, self).default_get(fields_list)

    # def force_assigned(self):
        # wizard = self.env['ir.actions.act_window']._for_xml_id("rental_system.action_assigned_order_wizard")
        # return {
        #     'name': 'Wizard',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     "view_type": "form",
        #     'res_model': 'assigned.order',
        #     'target': 'new',
        #     'view_id': self.env.ref
        #     ('rental_system.action_assigned_order_wizard').id,
        #     'context': {'active_id': self.id},
        # }
        # print("===========")
        # pass


    def call_wizard(self):
        wizard = self.env['ir.actions.act_window']._for_xml_id("rental_system.action_assigned_order_wizard")
        return wizard

    # @api.model
    # def get_view(self, views, options=None):
    #     # call super to get the original view
    #     result = super().get_view(views, options)
    #     # loop through the views
    #     for view in result.get("fields_views", {}).values():
    #         # check if the view type is form
    #         if view["type"] == "form":
    #             # parse the XML view
    #             doc = etree.XML(view["arch"])
    #             # find the field that you want to modify
    #             field = doc.xpath("//field[@name='rental_period_start']")
    #         if field:
    #             # inject your domain and context
    #             field[0].set("domain", "[('your_domain', '=', True)]")
    #             field[0].set("context", "{'abc': 'value'}")
    #         # update the view arch with the modified XML
    #         view["arch"] = etree.tostring(doc, encoding="unicode")
    #     return result
