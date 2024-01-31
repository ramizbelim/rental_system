from odoo import models, fields



class ErrorMessageAssigned(models.TransientModel):
    _name = 'assigned.product'


    name = fields.Selection([('yes', 'Yes'),('no', 'No')])
    customer = fields.Many2one('rent.customers', string="Customer")
    mobile = fields.Char(related="customer.mobile", string="Mobile", readonly=False)
    address = fields.Char(related="customer.address", string="Address", readonly=False)

    def force_assigned(self):
        if self.name == 'yes':
            select_id = self.env.context.get("active_ids")
            self.env["rent.customers"].search([("name", '=', self.name.name)]).update({
                'cloth_order': [(fields.Command.set([recs for recs in select_id]))]
            })
            self.env['cloth.orders'].create({
                'name': self.name.id,
                'my_product_ids': [(fields.Command.set([recs for recs in select_id]))]
            })
    def default_get(self):
        x = self.enc.context
        print("3333333333333333333333333333333",x)


