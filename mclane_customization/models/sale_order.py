# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_msrp = fields.Float('Margin', default=0.0)

    @api.depends('product_id')
    def _get_price_reduce(self):
        for line in self:
            line.margin_msrp = line.product_id.margin_msrp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin_msrp_total = fields.Integer(compute='_compute_margin_msrp_total', string='Expected Margin MSRP')

    @api.multi
    def _compute_margin_msrp_total(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_margin_msrp = 0.0  # type: float
            for line in order.order_line:
                amount_margin_msrp += line.product_id.margin_msrp

            order.update({
                'margin_msrp_total': order.pricelist_id.currency_id.round(amount_margin_msrp)
            })
