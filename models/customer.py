from odoo import models, fields, api


class Customer(models.Model):
    _name = "rent.customers"
    _description = "Customer Details"
    # _rec_name = "prod_num"

    name = fields.Char("Customer Name", required=True)
    prod_num = fields.Char(string="Prod Num", readonly=True)
    mobile = fields.Integer(string="Mobile", required=True)
    address = fields.Char(string="Address")
    identity = fields.Selection([('pan', "Pan Card"),
                                 ("voter_id", "Voter ID"),
                                 ("driving_id", "Driving Licence")],
                                string="Identity")
    identity_proof = fields.Binary("Identity Proof")
    email_id = fields.Char("Email ID")

    @api.model
    def create(self, vals):
        vals['prod_num'] = self.env['ir.sequence'].next_by_code('rent.customers.code')
        return super(Customer, self).create(vals)
