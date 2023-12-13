from odoo import models,fields,api


class ProductManagement(models.Model):
    _name = 'product.management'
    _description = 'Cloth Management'

    name = fields.Char(string="Product Name")
    rent_per_day = fields.Integer(string="Rent Per Day")
    size = fields.Selection([('s',"S"),('l',"L"),('m',"M"),('xl','XL'),('xxl','XXL'),('x','X')],string="size")
    category = fields.Selection([('men',"Men"),('women',"Women"),('children',"Children")],string="Product")
    product_image = fields.Binary(string="Image")
