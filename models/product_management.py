from odoo import models,fields,api


class ProductManagement(models.Model):
    _name = 'product.management'
    _description = 'Cloth Management'
    _rec_name = 'prod_id'

    name = fields.Char(string="Product Name")
    prod_id = fields.Char(string='Product ID')
    rent_per_day = fields.Integer(string="Rent Per Day")
    size = fields.Selection([('s',"S"),('l',"L"),('m',"M"),('xl','XL'),('xxl','XXL'),('x','X')],string="size")
    category = fields.Selection([('men',"Men"),('women',"Women"),('children',"Children")],string="Product")
    product_image = fields.Binary(string="Image")

    @api.model
    def create(self, vals):
        vals['prod_id'] = self.env['ir.sequence'].next_by_code('product.management.code')
        return super(ProductManagement, self).create(vals)