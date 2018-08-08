# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo import http
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.http_routing.models.ir_http import slug
import base64

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class WebsiteSaleCustom(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        if request.session.uid is None:
            return request.redirect('/web/login')
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category:
                raise NotFound()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        order=post.get('order'))

        compute_currency, pricelist_context, pricelist = self._get_compute_currency_and_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        partner = request.env.user.partner_id
        res_cat_flex = request.env['res.partner.flexible.cat']
        Display_Products = res_cat_flex.search([('csr_review', '=', False), ('partner_id', '=', partner.id)])
        categ_ids = []
        for categ_id in Display_Products:
            categ_ids.append(categ_id.product_category.id)

        categs = request.env['product.public.category'].search([('parent_id', '=', False), ('id', 'not in', categ_ids)])
        Product = request.env['product.template']

        parent_category_ids = []
        if category and category.id not in categ_ids:
            url = "/shop/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        domain += [('public_categ_ids.id', 'not in', categ_ids)]

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)


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
        product_category = request.env['product.public.category']
        res_cat_flex = request.env['res.partner.flexible.cat']

        error = {'error_message': []}

        if 'submitted' in kw:
            if 'license_number_cig' in kw and kw['license_number_cig'] and kw[
                'expiration_date_cig'] == '' and 'no_expiration_date_cig' not in kw:
                error['error_message'].append(
                    '* Please enter Expiration date or select No Expiration Date in Cigarettes.')
            if 'license_number_tc' in kw and kw['license_number_tc']:
                if kw['expiration_date_tc'] == '' and 'no_expiration_date_tc' not in kw:
                    error['error_message'].append(
                        '* Please enter Expiration date or select No Expiration Date in Tobacco.')
            if 'license_number_sale' in kw and kw['license_number_sale'] and not kw[
                'expiration_date_sale'] and 'no_expiration_date_sale' not in kw:
                error['error_message'].append(
                    '* Please enter Expiration date or select No Expiration Date in Sales Tax.')

        cig = product_category.search([('name', 'ilike', 'Cigarette')], limit=1)
        tc = product_category.search([('name', 'ilike', 'Tobacco')], limit=1)

        vals_cig = {
            'partner_id': partner.id,
            'license_number': kw['license_number_cig'],
            'start_date': kw['start_date_cig'],
            'expiration_date': kw['expiration_date_cig'],
            'no_expiration_date': True if 'no_expiration_date_cig' in kw else False,

        }

        vals_tc = {
            'partner_id': partner.id,
            'license_number': kw['license_number_tc'],
            'start_date': kw['start_date_tc'],
            'expiration_date': kw['expiration_date_tc'],
            'no_expiration_date': True if 'no_expiration_date_tc' in kw else False,
        }

        vals_sale = {
            'partner_id': partner.id,
            'license_number': kw['license_number_sale'],
            'start_date': kw['start_date_sale'],
            'expiration_date': kw['expiration_date_sale'],
            'no_expiration_date': True if 'no_expiration_date_sale' in kw else False,
        }

        if cig:
            vals_cig.update({'product_category': cig.id})
        if tc:
            vals_tc.update({'product_category': tc.id})

        if kw.get('license_file_cig'):
            license_file_cig = kw.get('license_file_cig').read()
            if license_file_cig:
                attachment_value = {
                    'name': kw.get('license_file_cig').filename,
                    'res_name': kw.get('license_file_cig').filename,
                    'res_model': 'res.partner.flexible.cat',
                    'res_id': partner.id,
                    'datas': base64.b64encode(license_file_cig),
                    'datas_fname': kw.get('license_file_cig').filename,
                }
                new_attachment = request.env['ir.attachment'].create(attachment_value)

                vals_cig.update({'license_file': kw.get('license_file_cig').filename,
                                 'license_file_attachment': new_attachment.id,
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

                    vals_tc.update({'license_filename': kw.get('license_file_tc').filename,
                                    'license_file_attachment': new_attachment.id,
                                    })
        #
        # if kw.get('license_file_sale'):
        #     license_file_cig = kw.get('license_file_sale').read()
        #     if license_file_cig:
        #         attachment_value = {
        #             'name': kw.get('license_file_sale').filename,
        #             'res_name': kw.get('license_file_sale').filename,
        #             'res_model': 'res.partner',
        #             'res_id': partner.id,
        #             'datas': base64.b64encode(license_file_cig),
        #             'datas_fname': kw.get('license_file_sale').filename,
        #         }
        #         new_attachment = request.env['ir.attachment'].create(attachment_value)
        #
        #         vals.update({'license_filename_sale': kw.get('license_file_sale').filename,
        #                      'license_file_attachment_sale': new_attachment.id,
        #                      })

        partner_cig = res_cat_flex.search([('product_category', '=', cig.id), ('partner_id', '=', partner.id)], limit=1)

        partner_tc = res_cat_flex.search([('product_category', '=', tc.id), ('partner_id', '=', partner.id)], limit=1)

        partner_sale = res_cat_flex.search([('product_category', '=', False), ('partner_id', '=', partner.id)], limit=1)

        if len(partner_cig) == 0:
            partner.sudo().write({'licenses_ids': [(0, 0, vals_cig)]})
        else:
            partner.sudo().write({'licenses_ids': [(1, partner_cig.id, vals_cig)]})

        if len(partner_tc) == 0:
            partner.sudo().write({'licenses_ids': [(0, 0, vals_tc)]})
        else:
            partner.sudo().write({'licenses_ids': [(1, partner_tc.id, vals_tc)]})

        if len(partner_sale) == 0:
            partner.sudo().write({'licenses_ids': [(0, 0, vals_sale)]})
        else:
            partner.sudo().write({'licenses_ids': [(1, partner_sale.id, vals_sale)]})

        if len(error['error_message']):
            values = {
                'partner_cig': partner_cig or False,
                'partner_tc': partner_tc or False,
                'partner_sale': partner_sale or False,
                'partner': partner,
                'submitted': 0,
                'error': error
            }
            return request.render("mclane_customization.license_permits_temp", values)
        else:
            return request.redirect('/license-permits')

    @route(['/license-permits'], type='http', auth="user", website=True)
    def home(self):
        res_cat_flex = request.env['res.partner.flexible.cat']
        partner = request.env.user.partner_id
        partner_cig = res_cat_flex.search(
            [('product_category.name', 'ilike', 'Cigarettes'), ('partner_id', '=', partner.id)], limit=1)

        partner_tc = res_cat_flex.search(
            [('product_category.name', 'ilike', 'Tobacco'), ('partner_id', '=', partner.id)], limit=1)

        partner_sale = res_cat_flex.search(
            [('product_category', '=', False), ('partner_id', '=', partner.id)], limit=1)

        error = {'error_message': []}

        values = {
            'partner': partner,
            'partner_cig': partner_cig or False,
            'partner_tc': partner_tc or False,
            'partner_sale': partner_sale or False,
            'submitted': 0,
            'error': error
        }
        return request.render("mclane_customization.license_permits_temp", values)

