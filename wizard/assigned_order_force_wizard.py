from odoo import models, fields


class AssignedorderForce(models.TransientModel):
    _name = 'assigned.order.force'

    name = fields.Many2one('rent.customers', string="Customer")
    mobile = fields.Char(related="name.mobile", string="Mobile", readonly=False)
    address = fields.Char(related="name.address", string="Address", readonly=False)

    def assigned_button(self):
        select_id = self.env.context.get("active_ids")
        record_id = self.env["rent.customers"].search([])
        store = []
        for rec in record_id:
            product_id = list(record.id for record in rec.cloth_order)
            cloth = list(cloth for cloth in select_id if cloth in product_id)
            store.extend(cloth)
        if store == []:
            self.env["rent.customers"].search([("name", '=', self.name.name)]).update({
                'cloth_order': [(fields.Command.set([recs for recs in select_id]))]
            })
            self.env['cloth.orders'].create({
                'name': self.name.id,
                'my_product_ids': [(fields.Command.set([recs for recs in select_id]))]
            })
        else:
            wizard = self.env['ir.actions.act_window']._for_xml_id("rental_system.action_assigned_product_wizard")
            # return wizard

            return {
                'context': {'active_id': self.ids,
                            'name': 'self.name',
                            'mobile': self.mobile,
                            'address':self.address
            }
            }

    def force_assigned_button(self):
        select_id = self.env.context.get("active_ids")
        self.env["rent.customers"].search([("name", '=', self.name.name)]).update({
            'cloth_order': [(fields.Command.set([recs for recs in select_id]))]
        })
        self.env['cloth.orders'].create({
            'name': self.name.id,
            'my_product_ids': [(fields.Command.set([recs for recs in select_id]))]
        })
