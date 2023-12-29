from odoo import models, fields, api


class ProductManagement(models.Model):
    _name = 'product.management'
    _description = 'Cloth Management'
    _rec_name = 'prod_id'

    name = fields.Char(string="Product Name")
    prod_id = fields.Char(string='Product ID')
    company_name = fields.Char("Company Name")
    rent_per_day = fields.Integer(string="Rent Per Day")
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

    @api.model
    def create(self, vals):
        vals['prod_id'] = self.env['ir.sequence'].next_by_code('product.management.code')
        vals['company_name'] = "H & M"
        return super(ProductManagement, self).create(vals)


    def write(self, vals):
        vals['company_name'] = "Mafatlal"
        return super(ProductManagement, self).write(vals)

