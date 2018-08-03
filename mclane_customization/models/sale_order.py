# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty')
    def _compute_margin_msrp(self):

        for order_line in self:
            amount_margin_msrp = 0.0  # type: float
            amount_margin_msrp += (order_line.product_id.product_tmpl_id.margin_msrp * order_line.product_uom_qty)
            order_line.update({
                'margin_msrp': amount_margin_msrp
            })

    margin_msrp = fields.Float('Margin', compute='_compute_margin_msrp', default=0.0)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.margin_msrp')
    def _compute_margin_msrp_total(self):
        for order in self:
            amount_untaxed = 0.0
            for line in order.order_line:
                amount_untaxed += line.margin_msrp
            order.update({
                'margin_msrp_total': amount_untaxed,
            })

    margin_msrp_total = fields.Float(compute='_compute_margin_msrp_total', string='Expected Margin MSRP')

