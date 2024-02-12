from odoo import models, fields



class ErrorMessageAssigned(models.TransientModel):
    _name = 'assigned.product'


    name = fields.Char(string="Customer")
    choose = fields.Selection([('yes', 'Yes'),('no', 'No')])
    mobile = fields.Char(string="Mobile", readonly=False)
    address = fields.Char(string="Address", readonly=False)

    def force_assigned_product(self):
        if self.choose == 'yes':
            select_id = self.env.context.get("active_ids")
            record_id = self.env["rent.customers"].search([])
            assigned_product_customer = []
            for rec in record_id:
                product_id = list(record.id for record in rec.cloth_order)
                cloth = list(cloth for cloth in select_id if cloth in product_id)
                customer_id = list(rec.id for id in rec.cloth_order if id.id in product_id if id.id in cloth)
                assigned_product_customer.extend(customer_id)
            for id in assigned_product_customer:
                for active_id in select_id:
                    self.env["rent.customers"].browse(id).update({
                                'cloth_order': [(fields.Command.unlink(active_id))]
                            })
            self.env["rent.customers"].search([("name", '=', self.name)]).update({
                'cloth_order': [(fields.Command.set(select_id))]
            })



