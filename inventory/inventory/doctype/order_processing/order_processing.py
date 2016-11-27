# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


form_grid_templates = {
	"summary_pending_order_roll": "templates/includes/summary_pending_order.html",
	"summary_pending_order_pcs": "templates/includes/summary_pending_order_pcs.html",

	"summary_roll_table": "templates/includes/alokasi_barang.html",
	
}


class OrderProcessing(Document):

	def summary_pending_order_get(self):
		if self.get("summary_pending_order_roll") :
			for item_summary in self.summary_pending_order_roll :
				count = item_summary.roll_qty
				
				if self.get("roll_table") :
					for item_roll in self.get("roll_table"):
						if item_summary.item_code_roll==item_roll.item_code_roll and item_summary.colour == item_roll.colour and (item_roll.rate == item_summary.rate or item_roll.rate == 0):
							if count == 0 :
								self.remove(item_summary)
							else :
								count = count - 1
								item_roll.rate = item_summary.rate
				
				item = frappe.get_doc("Item",item_summary.item_code_roll)
				for i in range(count) :
					ch = self.append("roll_table")
					#ch.roll_item_code = item_summary.item_code_roll
					#ch.roll_yard_atau_meter = 0
					##ch.roll_colour = item_summary.colour
					#ch.roll_rate = item_summary.rate
					#ch.roll_total_roll = 1
					
					ch.item_code_roll = item_summary.item_code_roll
					ch.item_name_roll = item.item_name
					ch.colour = item_summary.colour
					ch.roll_qty = 1
					ch.inventory_uom = item_summary.inventory_uom
					
					ch.rate = item_summary.rate
					#ch.total_rate = ch.rate * dg.total_roll * dg.yard_atau_meter_per_roll
					ch.warehouse = item.default_warehouse
					
			self.summary_pending_order_roll = []
			
		
		if self.get("summary_pending_order_pcs") :
			for item_summary in self.summary_pending_order_pcs :
				count = item_summary.pcs_qty
				
				if self.get("pcs_table") :
					for item_pcs in self.get("pcs_table"):
						if item_summary.item_code_pcs==item_pcs.item_code_pcs and item_summary.rate == item_pcs.rate :
							if count == 0 :
								self.remove(item_summary)
							else :
								count = count - 1
				item = frappe.get_doc("Item",item_summary.item_code_pcs)
				for i in range(count) :
					ch = self.append("pcs_table")
					ch.item_code_pcs = item_summary.item_code_pcs
					ch.item_name = item.item_name
					ch.pcs_uom = item_summary.pcs_uom
					ch.rate = item_summary.rate
					ch.pcs_qty = 1
					ch.total_rate = ch.rate
					ch.warehouse = item.default_warehouse

			self.summary_pending_order_pcs = []
	
	def get_group(self):
		if self.group_item :
			get_data_group = frappe.db.sql("""
				SELECT
				gi.`group_code`,
				gi.`uom`,

				dg.`item_code_variant`,
				dg.`item_name`,
				dg.`parent_item`,
				dg.`colour`,
				dg.`yard_atau_meter`,
				dg.`warehouse`,
				dg.`inventory_uom`,
				dg.`total_qty_roll`


				FROM `tabGroup Item` gi
				JOIN `tabData Group` dg
				ON gi.`name` = dg.`parent`
				WHERE gi.`group_code` = "{}"
				ORDER BY dg.`idx`

			""".format(self.group_item))


			if get_data_group :
				for dg in get_data_group :
						
					pp_so = self.append('group_helper_table', {})
					pp_so.item_code_variant = dg[2]
					pp_so.colour = dg[5]
					pp_so.total_roll = dg[9]
					pp_so.yard_atau_meter_per_roll = dg[6]
					pp_so.group_code = dg[0]

					qty_pending_order = 0
					qty_terkirim = 0
					qty_dialokasi = 0
					qty_inventory = 0

					get_qty_inventory = frappe.db.sql("""
						SELECT
						SUM(di.`total_roll`)
						FROM `tabData Inventory` di
						WHERE di.`item_code_variant` = "{}"
						AND di.`colour` = "{}"
						AND di.`group` = "{}"

						GROUP BY di.`item_code_variant`
						""".format(dg[2], dg[5], self.group_item))

					get_qty_pending_order = frappe.db.sql("""
						SELECT
						SUM(por.`roll_qty`)

						FROM `tabPending Order` po
						JOIN `tabPending Order Roll` por
						ON po.`name` = por.`parent`
						WHERE po.`docstatus` < 2
						AND por.`docstatus` < 2
						AND por.`item_code_roll` = "{}"
						AND por.`colour` = "{}"
						GROUP BY por.`item_code_roll`
						""".format(dg[2], dg[5]))

					get_qty_dialokasi = frappe.db.sql("""
						SELECT
						SUM(ops.`roll_qty`)

						FROM `tabOrder Processing` op
						JOIN `tabOrder Processing Summary Roll` ops
						ON op.`name` = ops.`parent`
						WHERE op.`docstatus` < 2
						AND ops.`docstatus` < 2
						AND ops.`item_code_roll` = "{}"
						AND ops.`colour` = "{}"
						AND ops.`group` = "{}"
						GROUP BY ops.`item_code_roll`
						""".format(dg[2], dg[5], self.group_item))

					get_qty_terkirim = frappe.db.sql("""
						SELECT
						SUM(por.`roll_qty`)

						FROM `tabPacking List Delivery` po
						JOIN `tabPacking List Delivery Data` por
						ON po.`name` = por.`parent`
						WHERE po.`docstatus` < 2
						AND por.`docstatus` < 2
						AND por.`item_code_roll` = "{}"
						AND por.`colour` = "{}"
						AND por.`group` = "{}"
						GROUP BY por.`item_code_roll`
						""".format(dg[2], dg[5], self.group_item))

					if get_qty_pending_order :
						qty_pending_order = float(get_qty_pending_order[0][0])
					else :
						qty_pending_order = 0
					if get_qty_terkirim :
						qty_terkirim = float(get_qty_terkirim[0][0])
					else :
						qty_terkirim = 0
					if get_qty_dialokasi :
						qty_dialokasi = float(get_qty_dialokasi[0][0])
					else :
						qty_dialokasi = 0
					if get_qty_inventory :
						qty_inventory = float(get_qty_inventory[0][0])
					else :
						qty_inventory = 0


					if qty_pending_order == 0 :
						pp_so.qty_pending_order = 0
					else :
						pp_so.qty_pending_order = qty_pending_order 

					if qty_dialokasi == 0 :
						pp_so.qty_alokasi_barang = 0
					else :
						pp_so.qty_alokasi_barang = qty_dialokasi

					if qty_terkirim == 0 :
						pp_so.qty_terkirim = 0
					else :
						pp_so.qty_terkirim = qty_terkirim

					if qty_inventory == 0 :
						pp_so.qty_inventory = 0
					else :
						pp_so.qty_inventory = qty_inventory - pp_so.qty_alokasi_barang
						
			else :
				frappe.throw("Group Tidak Active / Tidak Memiliki Item")

		else :
			frappe.throw("Group Item belum dipilih")
	
	def get_data_group(self):
		#for item_group in self.get("group_helper_table") :
		#	checker = 0
			
		#	for item_roll in self.get("roll_table") :
		#		if item_roll.roll_item_code == item_group.group_item_code and item_roll.roll_colour == item_group.group_colour and (item_roll.roll_yard_atau_meter == item_group.group_yard_atau_meter or item_roll.roll_yard_atau_meter == 0) :
		#			checker = 1
		#			item_roll.roll_yard_atau_meter = item_group.group_yard_atau_meter
			
		#	if (checker == 0) :
		#		for i in range(item_group.group_total_roll) :
		#			ch = self.append("roll_table")
		#			ch.roll_item_code = item_group.group_item_code
		#			ch.roll_yard_atau_meter = item_group.group_yard_atau_meter
		#			ch.roll_colour = item_group.group_colour
		#			ch.roll_rate = 0
		#			ch.roll_total_roll = 1
		if self.group_helper_table :
			for dg in self.group_helper_table :
				item = frappe.get_doc("Item", dg.item_code_variant)
				
				for i in range(dg.total_roll):
					pp_so = self.append('roll_table', {})
					pp_so.item_code_roll = dg.item_code_variant
					pp_so.item_name_roll = item.item_name
					pp_so.colour = dg.colour
					pp_so.roll_qty = 1
					pp_so.group = dg.group_code
					pp_so.inventory_uom = item.stock_uom
					pp_so.yard_atau_meter = dg.yard_atau_meter_per_roll
					pp_so.total_yard_atau_meter = pp_so.yard_atau_meter
					
					pp_so.rate = dg.rate
					pp_so.total_rate = dg.rate * dg.total_roll * dg.yard_atau_meter_per_roll
					pp_so.warehouse = item.default_warehouse

			self.group_helper_table = []

		else :
			frappe.throw("Data Group tidak ada")
		
	def summarize(self):
		for item in self.get("roll_table") :
			checker = 0
			if self.get("summary_roll_table") :
				for summary in self.get("summary_roll_table") :
					if (item.item_code_roll == summary.item_code_roll and item.yard_atau_meter == summary.yard_atau_meter and 
						item.colour == summary.colour and item.rate == summary.rate) :
						summary.roll_qty = summary.roll_qty + item.roll_qty
						summary.roll_sisa = summary.roll_qty
						
						summary.total_yard_atau_meter = summary.roll_qty * summary.yard_atau_meter
						summary.total_rate = summary.rate * summary.total_yard_atau_meter
						
						checker = 1
						break
			if checker == 0 :
				pp_so = self.append('summary_roll_table', {})
				pp_so.item_code_roll = item.item_code_roll
				pp_so.item_name_roll = item.item_name_roll
				pp_so.colour = item.colour
				pp_so.roll_qty = item.roll_qty
				pp_so.group = item.group
				pp_so.inventory_uom = item.inventory_uom
				pp_so.yard_atau_meter = item.yard_atau_meter
				pp_so.total_yard_atau_meter = pp_so.yard_atau_meter
					
				pp_so.rate = item.rate
				pp_so.total_rate = pp_so.rate * pp_so.total_yard_atau_meter
				pp_so.warehouse = item.warehouse

		self.roll_table = []
		for item in self.get("pcs_table") :
			checker = 0
			if self.get("summary_pcs_table") :
				for summary in self.get("summary_pcs_table") :
					if (item.item_code_pcs == summary.item_code_pcs  and item.rate == summary.rate) :
						summary.pcs_qty = summary.pcs_qty + item.pcs_qty
						summary.qty_sisa = summary.pcs_qty
						summary.total_rate = summary.pcs_qty * summary.rate
						checker = 1
						break
			if checker == 0 :
				ch = self.append("summary_pcs_table")
				
				ch.item_code_pcs = item.item_code_pcs
				ch.item_name_pcs = item.item_name_pcs
				ch.pcs_uom = item.pcs_uom
				ch.rate = item.rate
				ch.pcs_qty = item.pcs_qty
				ch.total_rate = ch.rate * ch.pcs_qty
				ch.warehouse = item.warehouse


		self.pcs_table = []				
	
	def on_submit(self):
		self.reduce_from_pending_order()
		self.update_submit_status_pending_order()
		
	def on_cancel(self):
		self.increase_pending_order()
		self.update_cancel_status_pending_order()

	def validate(self):
		self.recalculate()

	def update_cancel_status_pending_order(self):
		if not self.get("pending_order") :
			return

		pending_order = frappe.get_doc("Pending Order", self.get("pending_order"))

		if pending_order.pending_order_roll :
			count_check = 0
			for i in pending_order.pending_order_roll :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 1 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabPending Order` 
					set 
					status_document= "Open"
					where 
					name="{0}"
				""".format(self.get("pending_order")))


		if pending_order.pending_order_pcs :
			count_check = 0
			for i in pending_order.pending_order_pcs :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 1 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabPending Order` 
					set 
					status_document= "Open"
					where 
					name="{0}"
				""".format(self.get("pending_order")))

		
	def update_submit_status_pending_order(self):
		if not self.get("pending_order") :
			return

		pending_order = frappe.get_doc("Pending Order", self.get("pending_order"))

		if pending_order.pending_order_roll :
			count_check = 0
			for i in pending_order.pending_order_roll :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 0 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabPending Order` 
					set 
					status_document= "Closed"
					where 
					name="{0}"
				""".format(self.get("pending_order")))


		if pending_order.pending_order_pcs :
			count_check = 0
			for i in pending_order.pending_order_pcs :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 0 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabPending Order` 
					set 
					status_document= "Closed"
					where 
					name="{0}"
				""".format(self.get("pending_order")))



	def reduce_from_pending_order(self):
		if not self.get("pending_order") :
			return
		item_list = []
		item_qty = {}
		for item in self.get("summary_roll_table") :
			key = (item.item_code_roll,item.colour,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.roll_qty
		pending_order = frappe.get_doc("Pending Order", self.get("pending_order"))
		value_clause = ""
		for item in pending_order.pending_order_roll :
			key = (item.item_code_roll,item.colour,item.rate)
			if key in item_list :
				sisa = item.qty_sisa
				if sisa < item_qty[key] :
					item_qty[key] = item_qty[key] - sisa
					sisa = 0
				else :
					sisa = sisa - item_qty[key]
					item_qty[key] = 0
				if value_clause == "" :
					value_clause = """("{0}",{1})""".format(item.name,sisa)
				else :
					value_clause = """{0}, ("{1}",{2})""".format(value_clause,item.name,sisa)
		if not value_clause == "" :	
			frappe.db.sql(""" 
				INSERT INTO `tabPending Order Roll` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
		
		item_list = []
		item_qty = {}
		for item in self.get("summary_pcs_table") :
			key = (item.item_code_pcs,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.pcs_qty
			
		value_clause = ""
		for item in pending_order.pending_order_pcs :
			key = (item.item_code_pcs,item.rate)
			if key in item_list :
				sisa = item.qty_sisa
				if sisa < item_qty[key] :
					item_qty[key] = item_qty[key] - sisa
					sisa = 0
				else :
					sisa = sisa - item_qty[key]
					item_qty[key] = 0
				if value_clause == "" :
					value_clause = """("{0}",{1})""".format(item.name,sisa)
				else :
					value_clause = """{0}, ("{1}",{2})""".format(value_clause,item.name,sisa)
		if not value_clause == "" :	
			frappe.db.sql(""" 
				INSERT INTO `tabPending Order Pcs` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
	
	def increase_pending_order(self):
		if not self.get("pending_order") :
			return
		item_list = []
		item_qty = {}
		for item in self.get("summary_roll_table") :
			key = (item.item_code_roll,item.colour,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.roll_qty
		pending_order = frappe.get_doc("Pending Order", self.get("pending_order"))
		value_clause = ""
		for item in pending_order.pending_order_roll :
			key = (item.item_code_roll,item.colour,item.rate)
			if key in item_list :
				sisa = item.qty_sisa
				sisa = sisa + item_qty[key]
				item_qty[key] = 0
				if value_clause == "" :
					value_clause = """("{0}",{1})""".format(item.name,sisa)
				else :
					value_clause = """{0}, ("{1}",{2})""".format(value_clause,item.name,sisa)
		if not value_clause == "" :	
			frappe.db.sql(""" 
				INSERT INTO `tabPending Order Roll` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
		
		item_list = []
		item_qty = {}
		for item in self.get("summary_pcs_table") :
			key = (item.item_code_pcs,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.pcs_qty
			
		value_clause = ""
		for item in pending_order.pending_order_pcs :
			key = (item.item_code_pcs,item.rate)
			if key in item_list :
				sisa = item.qty_sisa
				sisa = sisa + item_qty[key]
				item_qty[key] = 0
				if value_clause == "" :
					value_clause = """("{0}",{1})""".format(item.name,sisa)
				else :
					value_clause = """{0}, ("{1}",{2})""".format(value_clause,item.name,sisa)
		if not value_clause == "" :	
			frappe.db.sql(""" 
				INSERT INTO `tabPending Order Pcs` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
		
	def recalculate(self) :
		for item in self.get("summary_roll_table") :
			item.qty_sisa = item.roll_qty
			item.total_yard_atau_meter = item.yard_atau_meter * item.roll_qty
			item.total_rate = item.rate * item.total_yard_atau_meter
		for item in self.get("summary_pcs_table") :
			item.qty_sisa = item.pcs_qty
			item.total_rate = item.rate * item.pcs_qty
			
	pass


@frappe.whitelist()
def get_data_from_order_processing(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.order_processing = source.name
		target.customer = source.customer
		target.order_processing_roll = []

		target.commission_rate = source.commission_percentage

		for item in source.summary_roll_table :
			if item.qty_sisa > 0 :
				ch = target.append("order_processing_roll")
				ch.item_code_roll = item.item_code_roll
				ch.item_name_roll = item.item_name_roll
				ch.colour = item.colour
				ch.inventory_uom = item.inventory_uom
				ch.group = item.group
				ch.warehouse = item.warehouse
				ch.note = item.note
				ch.rate = item.rate
				ch.total_rate = item.total_rate
				ch.yard_atau_meter = item.yard_atau_meter
				ch.total_yard_atau_meter = item.total_yard_atau_meter
				ch.roll_qty = item.qty_sisa
		target.order_processing_pcs = []
		for item in source.summary_pcs_table :
			if item.qty_sisa > 0 :
				ch = target.append("order_processing_pcs")
				ch.item_code_pcs = item.item_code_pcs
				ch.item_name_pcs = item.item_name_pcs
				ch.pcs_uom = item.pcs_uom
				ch.warehouse = item.warehouse
				ch.note = item.note
				ch.rate = item.pcs_rate
				ch.total_rate = item.total_rate
				ch.pcs_qty = item.qty_sisa
	def update_item_roll(source_doc, target_doc, source_parent):
		pass
		
	def update_item_pcs(source_doc, target_doc, source_parent):
		pass



	target_doc = get_mapped_doc("Order Processing", source_name, {
		"Order Processing": {
			"doctype": "Sales Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		}
		
	}, target_doc, set_missing_values)

	return target_doc