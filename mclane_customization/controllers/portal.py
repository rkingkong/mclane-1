# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
import base64


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
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        country_id = False
        if not partner.country_id:
            country_id = request.env['res.country'].sudo().search([('code', '=', 'US')]).id

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
        datas = kw.get('license_file').read()
        attachment = False
        if datas:

            attachment = request.env['ir.attachment'].sudo().create({
                'name': partner.name,
                'type': 'binary',
                'datas': base64.encodestring(datas),
                'res_model': 'res.partner',
                'res_id': partner.id,
                'datas_fname': kw.get('license_file').filename
            }).id

        partner.write({
            'license_number': kw['license_number'],
            'expiration_date': kw['expiration_date'],
            'license_file': attachment })

        return request.redirect("/")

    @route(['/license-permits'], type='http', auth="user", website=True)
    def home(self):
        return request.render("mclane_customization.license_permits_temp")
