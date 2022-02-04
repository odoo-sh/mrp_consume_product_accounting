# Copyright 2018-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import models, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _cal_price(self, consumed_moves):
        """Do not add the cost of a consumable product to the finished product that is manufacturing."""
        consumed_moves = consumed_moves.filtered(lambda x: x.product_id.type != 'consu')
        return super(MrpProduction, self)._cal_price(consumed_moves)

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_accounting_data_for_valuation(self):
        """if a consumable is produced in a manufacturing order, then move the cost to the expense account of the consumable"""
        self.ensure_one()
        journal_id, acc_src, acc_dest, acc_valuation = super(StockMove, self)._get_accounting_data_for_valuation()
        if self.location_dest_id.usage == 'production' and self.raw_material_production_id and self.raw_material_production_id.product_id.type != 'product':
            accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
            acc_dest = accounts_data['expense'].id
        return journal_id, acc_src, acc_dest, acc_valuation

    def _get_price_unit(self):
        res = super(StockMove, self)._get_price_unit()
        if self._is_in() and self.production_id:
            if all('consu' in val.product_id.type for val in self.production_id.move_raw_ids):
                return self.price_unit
        return res

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        self.ensure_one()
        if self._context.get('force_valuation_amount'):
            valuation_amount = self._context.get('force_valuation_amount')
        else:
            valuation_amount = cost
        debit_value = self.company_id.currency_id.round(valuation_amount)
        if self.company_id.currency_id.is_zero(debit_value) and self._is_in() and self.production_id and all('consu' in val.product_id.type for val in self.production_id.move_raw_ids):
            return []
        return super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id,description)
