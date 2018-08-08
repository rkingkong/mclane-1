# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
import base64


class WebsiteSaleCustom(WebsiteSale):
    @http.route('/shop', type="http", auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if request.session.uid is None:
            return request.redirect('/web/login')
        return super(WebsiteSaleCustom, self).shop(page, category, search, ppg, **post)


class WebsiteExtendCustom(Website):
    @http.route('/', type="http", auth="public", website=True)
    def index(self, **kw):
        if request.session.uid is None:
            return request.redirect('/web/login')
        return super(WebsiteExtendCustom, self).index(**kw)


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

    @route(['/my/account/update'], type='http', auth="public", methods=['POST', 'GET'], website=True)
    def change_value(self, **kw):
        global new_attachment
        partner = request.env.user.partner_id
        error = {'error_message': []}

        if 'submitted' in kw:
            if 'license_number_cig' in kw and kw['license_number_cig']:
                if kw['expiration_date_cig'] == '' and 'no_expiration_date_cig' not in kw:
                    error['error_message'].append(
                        '* Please enter Expiration date or select No Expiration Date in Cigarettes.')
            if 'license_number_tc' in kw and kw['license_number_tc']:
                if kw['expiration_date_tc'] == '' and 'no_expiration_date_tc' not in kw:
                    error['error_message'].append(
                        '* Please enter Expiration date or select No Expiration Date in Tobacco.')
            if 'license_number_sale' in kw and kw['license_number_sale']:
                if not kw['expiration_date_sale'] and 'no_expiration_date_sale' not in kw:
                    error['error_message'].append(
                        '* Please enter Expiration date or select No Expiration Date in Sales Tax.')

        vals = {
            'license_number_cig': kw['license_number_cig'],
            'license_number_sale': kw['license_number_sale'],
            'license_number_tc': kw['license_number_tc'],
            'start_date_cig': kw['start_date_cig'],
            'start_date_tc': kw['start_date_tc'],
            'start_date_sale': kw['start_date_sale'],
            'expiration_date_cig': kw['expiration_date_cig'],
            'expiration_date_sale': kw['expiration_date_sale'],
            'expiration_date_tc': kw['expiration_date_tc'],
            'no_expiration_date_tc': True if 'no_expiration_date_tc' in kw else False,
            'no_expiration_date_cig': True if 'no_expiration_date_cig' in kw else False,
            'no_expiration_date_sale': True if 'no_expiration_date_sale' in kw else False,
        }

        if kw.get('license_file_cig'):
            license_file_cig = kw.get('license_file_cig').read()
            if license_file_cig:
                attachment_value = {
                    'name': kw.get('license_file_cig').filename,
                    'res_name': kw.get('license_file_cig').filename,
                    'res_model': 'res.partner',
                    'res_id': partner.id,
                    'datas': base64.b64encode(license_file_cig),
                    'datas_fname': kw.get('license_file_cig').filename,
                }
                new_attachment = request.env['ir.attachment'].create(attachment_value)

                vals.update({'license_filename_cig': kw.get('license_file_cig').filename,
                             'license_file_attachment_cig': new_attachment.id,
                             })

        if kw.get('license_file_tc'):
            license_file_cig = kw.get('license_file_tc').read()
            if license_file_cig:
                if license_file_cig:
                    attachment_value = {
                        'name': kw.get('license_file_tc').filename,
                        'res_name': kw.get('license_file_tc').filename,
                        'res_model': 'res.partner',
                        'res_id': partner.id,
                        'datas': base64.b64encode(license_file_cig),
                        'datas_fname': kw.get('license_file_tc').filename,
                    }
                    new_attachment = request.env['ir.attachment'].create(attachment_value)

                vals.update({'license_filename_tc': kw.get('license_file_tc').filename,
                             'license_file_attachment_tc': new_attachment.id
                             })

        if kw.get('license_file_sale'):
            license_file_cig = kw.get('license_file_sale').read()
            if license_file_cig:
                attachment_value = {
                    'name': kw.get('license_file_sale').filename,
                    'res_name': kw.get('license_file_sale').filename,
                    'res_model': 'res.partner',
                    'res_id': partner.id,
                    'datas': base64.b64encode(license_file_cig),
                    'datas_fname': kw.get('license_file_sale').filename,
                }
                new_attachment = request.env['ir.attachment'].create(attachment_value)

                vals.update({'license_filename_sale': kw.get('license_file_sale').filename,
                             'license_file_attachment_sale': new_attachment.id,
                             })

        partner.sudo().write(vals)
        if len(error['error_message']):
            values = {
                'partner': partner,
                'submitted': 0,
                'error': error
            }
            return request.render("mclane_customization.license_permits_temp", values)
        else:
            return request.redirect('/license-permits')

    @route(['/license-permits'], type='http', auth="user", website=True)
    def home(self):
        partner = request.env.user.partner_id
        error = {'error_message': []}

        values = {
            'partner': partner,
            'submitted': 0,
            'error': error
        }
        return request.render("mclane_customization.license_permits_temp", values)

