from odoo import models, fields
class Assignedorder(models.TransientModel):
    _name = 'assigned.order'

    name = fields.Selection([('yes', 'Yes'),('no', 'No')])

    def force_assigneded(self):
        print("******************")




