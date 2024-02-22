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

    @http.route('/customer-details', type="http", auth='public', website=True)
    def customer_data(self, **kwargs):
        customer_detail = request.env["rent.customers"].search([])
        values = {
            'customer' : customer_detail
        }
        return request.render("rental_system.rental_customer_record_details",values)

    @http.route('/rental-system', type="http", auth='public', website=True)
    def rental_system_view(self, **kwargs):
        product_details = request.env["product.management"].search([])
        company = {}
        for rec in product_details:
            company_name = dict(rec._fields['company_name'].selection)
            company.update(company_name)

        # company_name = product_details._fields['company_name'].selection
            # company.update({'company' : company_name})
        print("cccccccccccccccccccccccccccccc",company)
        values = {
            'product': product_details,
            # 'company': company,
        }
        print("valuessssssssssssssssss", values)
        return request.render("rental_system.rental_system_website_views", values)
    @http.route('/product-data', type="http", auth='public', website=True)
    def products_show_data(self):
        product_details = request.env["product.management"].search([])
        values = {
            'product': product_details
        }
        return request.render("rental_system.rental_system_website_views", values)

    @http.route('/form', type='http', auth='public',  website=True)
    def form_cloth_washing(self, **kwargs):
        return http.request.render("rental_system.form_cloth_washing", {})

    @http.route('/create-cloth', type='http', auth='public',website=True)
    def create_washing_cloth(self, **kwargs):
        print("77777777777777777",kwargs)
        product_val = {
            'name' : kwargs.get('name')
        }
        request.env["cloth.washing"].sudo().create(product_val)
        return request.render("rental_system.thanks_page",{})

    # @http.route('/my_controller', type='json', auth='public', csrf=False)
    # def my_json_controller(self, **kwargs):
    #     product_details = request.env["product.management"].search([])
    #     values = {
    #             'product': product_details
    #         }
    #     return {'result': 'success'}



