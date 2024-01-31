from odoo import models, fields, api


class ProductManagement(models.Model):
    _name = 'product.management'
    _description = 'Cloth Management'
    _rec_name = 'prod_id'

    name = fields.Char(string="Product Name")
    prod_id = fields.Char(string='Product ID')
    company_name = fields.Selection([('raymond', 'Raymond'),
                                     ('h_and_m', 'H & M '),
                                     ('mafatlal', 'Mafatlal')], string="Brand Name")
    rent_per_day = fields.Integer(string="Rent Per Day", tracking=True)
    size = fields.Selection([('s', "S"),
                             ('l', "L"),
                             ('m', "M"),
                             ('xl', 'XL'),
                             ('xxl', 'XXL'),
                             ('x', 'X')],
                            string="size")
    category = fields.Selection([('t_shirt', "T-Sirt"),
                                 ('shirt', "Shirt"),
                                 ('pent', "Pent"),
                                 ('pathani', "Pathani"),
                                 ('trouser', "Trousers"),
                                 ('blazer', "Blazer")],
                                string="Category")
    product_image = fields.Binary(string="Image")
    sum_one = fields.Integer(string=" ", compute="_compute_subtotal")
    # quantity = fields.Integer(string="Quantity")

    @api.model
    def create(self, vals):
        vals['prod_id'] = self.env['ir.sequence'].next_by_code('product.management.code')
        return super(ProductManagement, self).create(vals)

    def _compute_subtotal(self):
        total = 0
        for order in self:
            total = total + order.rent_per_day
            self.sum_one = total
