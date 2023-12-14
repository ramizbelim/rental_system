from odoo import models, fields, api


class Customer(models.Model):
    _name = "rent.customers"

    name = fields.Char("Customer Name",required=True)
    mobile = fields.Integer(string="Mobile",required = True)
    address = fields.Char(string="Address",required=True)
    identity = fields.Selection([('pan',"Pan Card"),("voter_id","Voter ID"),
                                 ("driving_id","Driving Licence")],string="Identity",required=True)
    identity_proof = fields.Binary("Identity Proof")
    email_id = fields.Char("Email ID")


