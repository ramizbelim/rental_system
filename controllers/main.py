from odoo import http
from odoo.http import request

class WebsiteContact(http.Controller):

    @http.route('/contact', type="http", auth='public', website = True)
    def fetch_res_partner_data(self, **kwargs):
        partner_details = request.env["res.partner"].search([])
        values = {
            'partners' : partner_details
        }
        return request.render("rental_system.contact_res_partner_details",values)

    @http.route('/contact/<int:id>', type="http", auth='public', website=True)
    def fetch_res_partner_data_particular(self,id=None ,**kwargs):
        partner_details = request.env["res.partner"].search([]).browse(int(id))
        values = {
            'partners': partner_details
        }
        return request.render("rental_system.contact_res_partner_details_dynamic", values)

    @http.route('/customer', type="http", auth='public', website=True)
    def customer_data(self, **kwargs):
        customer_detail = request.env["rent.customers"].search([])
        values = {
            'customer' : customer_detail
        }
        return request.render("rental_system.rental_customer_record_details",values)

    @http.route('/product', type="http", auth='public', website=True)
    def customer_data(self, **kwargs):
        product_details = request.env["product.management"].search([])
        values = {
            'product': product_details
        }
        return request.render("rental_system.cloth_rental_product_snippet", values)

