# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _compute_margin_msrp(self):
        for order_line in self:
            order_line.update({
                'margin_msrp': order_line.product_id.product_tmpl_id.margin_msrp
            })

    margin_msrp = fields.Float('Margin', compute='_compute_margin_msrp', default=0.0)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.product_uom_qty')
    def _compute_margin_msrp_total(self):
        for order in self:
            amount_untaxed = 0.0
            for line in order.order_line:
                amount_untaxed += (line.product_id.product_tmpl_id.margin_msrp * line.product_uom_qty)
            order.update({
                'margin_msrp_total': amount_untaxed,
            })

    margin_msrp_total = fields.Float(compute='_compute_margin_msrp_total', string='Expected Margin MSRP')


