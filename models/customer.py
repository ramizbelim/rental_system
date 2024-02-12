from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _name = "rent.customers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Customer Details"
    # _rec_name = "prod_num"

    name = fields.Char("Customer Name", required=True)
    prod_num = fields.Char(string="Prod Num", readonly=True)
    mobile = fields.Char(string="Mobile", required=True,
                         compute="_compute_check_number",
                         store=True, readonly=False)
    address = fields.Char(string="Address")
    identity = fields.Selection([('pan', "Pan Card"),
                                 ("voter_id", "Voter ID"),
                                 ("driving_id", "Driving Licence")],
                                string="Identity")
    identity_proof = fields.Binary("Identity Proof")
    email_id = fields.Char("Email ID")
    cloth_order = fields.Many2many('product.management',string="Cloth Order")

    @api.model
    def create(self, vals):
        vals['prod_num'] = self.env['ir.sequence'].next_by_code('rent.customers.code')
        return super(Customer, self).create(vals)

    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     print("======", name)
    #     print(".----------------------->", args)
    #     print(".----------------------->", operator)
    #     print(".----------------------->", limit)
    #     ids = self._name_search(name, args, operator, limit=limit)
    #     print(".----------------------->", name)
    #     print(".----------------------->",ids)
    #     return self.browse(ids).sudo().name_get()
    @api.constrains('mobile')
    def _compute_check_number(self):
        for record in self:
            if record.mobile and (len(record.mobile) == 10 and record.mobile.isdigit()):
                pass
            else:
                raise ValidationError("Mobile number must be a 10-digit !")


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        # print(".---------------------args-->", args)
        # print(".----------------------operator->", operator)
        # print(".---------------------limit-->", limit)
        # print(".----------------------name->", name)
        # print(".----------------------name_get_uid->", name_get_uid)
        if name:
            # Be sure name_search is symetric to name_get
            # name = name.split(' / ')[-1]
            # print(".----------------------name->", name)
            args = ['|', ('name', operator, name), ('prod_num', operator, name)] + args

            # print(".----------------------args->", args)
        # print("after print====", self._search(args, limit=limit, access_rights_uid=name_get_uid))
        # return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super()._name_search(name, args, operator, limit, name_get_uid)
