# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.main import Home
import base64
import werkzeug
import werkzeug.utils


class Website(Home):
    @route()
    def index(self, **kw):
        if not request.session.uid:
            return werkzeug.utils.redirect('/web/login')
        return super(Website, self).index(**kw)


class WebsiteSalePortal(CustomerPortal):
    @route()
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key]
                          for key in self.MANDATORY_BILLING_FIELDS}
                values.update(
                    {key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        country_id = False
        if not partner.country_id:
            country_id = request.env['res.country'].sudo().search(
                [('code', '=', 'US')]).id

        values.update({
            'partner': partner,
            'countries': countries,
            'country_id': country_id,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class Portal(Controller):

    @route(['/my/account/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def change_value(self, **kw):
        partner = request.env.user.partner_id
        vals = {
            'license_filename_cig': kw.get('license_file_cig').filename,
            'license_number_cig': kw['license_number_cig'],
            'license_number_sale': kw['license_number_sale'],
            'license_number_tc': kw['license_number_tc'],
            'start_date_cig': kw['start_date_cig'],
            'start_date_tc': kw['start_date_tc'],
            'start_date_sale': kw['start_date_sale'],
            'expiration_date_cig': kw['expiration_date_cig'],
            'expiration_date_sale': kw['expiration_date_sale'],
            'expiration_date_tc': kw['expiration_date_tc'],
        }
        license_file_cig = kw.get('license_file_cig').read()
        if license_file_cig:
            vals.update(
                {'license_file_cig': base64.b64encode(license_file_cig)})
        partner.write(vals)

        return request.redirect("/")

    @route(['/license-permits'], type='http', auth="user", website=True)
    def home(self):
        partner = request.env.user.partner_id
        values = {
            'partner': partner
        }
        return request.render("mclane_customization.license_permits_temp", values)
