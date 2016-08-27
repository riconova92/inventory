# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PendingOrder(Document):
	def add_item(self):
		if self.item_code and self.qty and self.warehouse :
			if self.uom == "Yard" or self.uom == "Meter" :
				if self.colour :
					if self.pending_order_roll :
						for i in self.pending_order_roll :
							if i.item_code_roll == self.item_code and i.colour == self.colour and i.warehouse == self.warehouse and i.rate == self.rate and i.group == "" :
								new_total_roll = i.roll_qty
								i.roll_qty = new_total_roll + self.qty
								new_total_rate = i.total_rate
								i.total_rate = new_total_rate + (self.qty * self.rate)

							else :
								pp_so = self.append('pending_order_roll', {})
								pp_so.item_code_roll = self.item_code
								pp_so.item_name_roll = self.item_name
								pp_so.colour = self.colour
								pp_so.roll_qty = self.qty
								pp_so.rate = self.rate
								pp_so.warehouse = self.warehouse
					else :
						pp_so = self.append('pending_order_roll', {})
						pp_so.item_code_roll = self.item_code
						pp_so.item_name_roll = self.item_name
						pp_so.colour = self.colour
						pp_so.roll_qty = self.qty
						pp_so.rate = self.rate
						pp_so.total_rate = self.rate * self.qty
						pp_so.warehouse = self.warehouse
				else :
					frappe.throw("Colour tidak ada isinya")

			elif self.uom == "Pcs" :
				if self.pending_order_pcs :
					for i in self.pending_order_pcs :
						if i.item_code_pcs == self.item_code and i.warehouse == self.warehouse and i.rate == self.rate and i.group == "" :
							new_total_roll = i.pcs_qty
							i.pcs_qty = new_total_roll + self.qty
							new_total_rate = i.total_rate
							i.total_rate = new_total_rate + (self.qty * self.rate)
						else :
							pp_so = self.append('pending_order_pcs', {})
							pp_so.item_code_pcs = self.item_code
							pp_so.item_name_roll = self.item_name
				
							pp_so.pcs_qty = self.qty
							pp_so.rate = self.rate
							pp_so.warehouse = self.warehouse
				else :
					pp_so = self.append('pending_order_pcs', {})
					pp_so.item_code_pcs = self.item_code
					pp_so.item_name_roll = self.item_name
					
					pp_so.pcs_qty = self.qty
					pp_so.rate = self.rate
					pp_so.total_rate = self.rate * self.qty
					pp_so.warehouse = self.warehouse


		else :
			frappe.throw("Item Code / Qty / Warehouse tidak ada isinya")
