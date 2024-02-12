from odoo import http
from odoo.http import request
from .main import WebsiteContact

class WebsiteCustomerDetails(WebsiteContact):

    def customer_data(self, **kwargs):
        res = super().customer_data()
        # var = res.qcontext.get('customer')
        var = res.qcontext
        product_details = request.env["product.management"].search([])
        var['product'] = product_details
        return res

