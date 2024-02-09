
from odoo import http
from odoo.http import request


class WebsiteContact(http.Controller):

    @http.route('/contact', type="json", auth='user')
    def fetch_res_partner_data(self, **kwargs):
        partner_details = request.env["res.partner"].search([])
        values = {
            'partners' : partner_details
        }
        return request.render("rental_system.",values)
