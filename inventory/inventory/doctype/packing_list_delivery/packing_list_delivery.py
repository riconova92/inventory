# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import msgprint
import frappe.utils
from frappe.utils import cstr, flt, getdate, comma_and, cint
from frappe import _
from frappe.model.mapper import get_mapped_doc
import operator


form_grid_templates = {
	"packing_list_data": "templates/includes/packing_list_delivery.html"
}


class PackingListDelivery(Document):
	
	def on_submit(self):
		self.reduce_order_processing()
		self.update_submit_status_order_processing()
		self.check_return_item()

	def on_cancel(self):
		self.increase_order_processing()
		self.update_cancel_status_order_processing()
	
	def check_return_item(self):
		if not self.is_return :
			return
		return_doc = frappe.get_doc("Packing List Delivery",self.return_against)
		for item in self.packing_list_data :
			checker = 0
			for item_b in return_doc.packing_list_data :
				if item.item_code_roll == item_b.item_code_roll and item.yard_atau_meter_per_roll == item_b.yard_atau_meter_per_roll :
					checker = 1
					break
			if checker == 0 :
				frappe.throw("Ada Item yang tidak ditemukan pada Packing List Delivery")
		
		for item in self.packing_list_data_pcs :
			checker = 0
			for item_b in return_doc.packing_list_data_pcs :
				if item.item_code_pcs == item_b.item_code_pcs :
					checker = 1
					break
			if checker == 0 :
				frappe.throw("Ada Item yang tidak ditemukan pada Packing List Delivery")
		

	def update_submit_status_order_processing(self):
		if not self.get("sales_invoice") :
			return

		sales_invoice = frappe.get_doc("Sales Invoice", self.get("sales_invoice"))

		order_processing = frappe.get_doc("Order Processing", sales_invoice.order_processing)

		if order_processing.summary_roll_table :
			count_check = 0
			for i in order_processing.summary_roll_table :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 0 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabOrder Processing` 
					set 
					status_document= "Closed"
					where 
					name="{0}"
				""".format(sales_invoice.order_processing))


		if order_processing.summary_pcs_table :
			count_check = 0
			for i in order_processing.summary_pcs_table :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 0 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabOrder Processing` 
					set 
					status_document= "Closed"
					where 
					name="{0}"
				""".format(sales_invoice.order_processing))



	def update_cancel_status_order_processing(self):
		if not self.get("sales_invoice") :
			return

		sales_invoice = frappe.get_doc("Sales Invoice", self.get("sales_invoice"))

		order_processing = frappe.get_doc("Order Processing", sales_invoice.order_processing)

		if order_processing.summary_roll_table :
			count_check = 0
			for i in order_processing.summary_roll_table :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 1 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabOrder Processing` 
					set 
					status_document= "Open"
					where 
					name="{0}"
				""".format(sales_invoice.order_processing))


		if order_processing.summary_pcs_table :
			count_check = 0
			for i in order_processing.summary_pcs_table :
				if i.qty_sisa > 0 :
					count_check = 1

			if count_check == 1 :
				# update status pending order
				frappe.db.sql ("""
					update 
					`tabOrder Processing` 
					set 
					status_document= "Open"
					where 
					name="{0}"
				""".format(sales_invoice.order_processing))






	def reduce_order_processing(self):
		if not self.get("sales_invoice") :
			return
		si = frappe.get_doc("Sales Invoice",self.sales_invoice)
		if not si.get("order_processing") :
			return
		
		item_list = []
		item_qty = {}
		for item in self.get("packing_list_data") :
			key = (item.item_code_roll,item.colour,item.yard_atau_meter_per_roll,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.roll_qty
		order_processing = frappe.get_doc("Order Processing", si.get("order_processing"))
		value_clause = ""
		for item in order_processing.summary_roll_table :
			key = (item.item_code_roll,item.colour,item.yard_atau_meter,item.rate)
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
				INSERT INTO `tabOrder Processing Summary Roll` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
		
		item_list = []
		item_qty = {}
		for item in self.get("packing_list_data_pcs") :
			key = (item.item_code_pcs,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.pcs_qty
			
		value_clause = ""
		for item in order_processing.summary_pcs_table :
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
				INSERT INTO `tabOrder Processing Summary Pcs` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
	
	def increase_order_processing(self):
		if not self.get("sales_invoice") :
			return
		si = frappe.get_doc("Sales Invoice",self.sales_invoice)
		if not si.get("order_processing") :
			return
		
		item_list = []
		item_qty = {}
		for item in self.get("packing_list_data") :
			key = (item.item_code_roll,item.colour,item.yard_atau_meter_per_roll,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.total_roll
		order_processing = frappe.get_doc("Order Processing", si.get("order_processing"))
		value_clause = ""
		for item in order_processing.summary_roll_table :
			key = (item.item_code_roll,item.colour,item.yard_atau_meter,item.rate)
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
				INSERT INTO `tabOrder Processing Summary Roll` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
		
		item_list = []
		item_qty = {}
		for item in self.get("packing_list_data_pcs") :
			key = (item.item_code_pcs,item.rate)
			if not key in item_list :
				item_list.append(key)
				item_qty[key] = 0
			item_qty[key] = item_qty[key] + item.pcs_qty
			
		value_clause = ""
		for item in order_processing.summary_pcs_table :
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
				INSERT INTO `tabOrder Processing Summary Pcs` (`name`,`qty_sisa`) VALUES {0} 
				ON DUPLICATE KEY UPDATE `qty_sisa` = VALUES(`qty_sisa`) 
				""".format(value_clause))
	
	def add_item(self):
	 	count = 0
		if not self.qty_roll :
			frappe.throw("Item Code / Colour / Warehouse / Qty / Yard / Meter tidak terisi")
		qty_add = self.qty_roll
		if self.is_return :
			if qty_add > 0 :
				qty_add = 0-qty_add
	 	if self.item_code_variant and self.yard_atau_meter and self.colour and self.warehouse :
	 		parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
	 		item_name = frappe.get_doc("Item", self.item_code_variant).item_name
	 		if self.packing_list_data :
	 			for i in self.packing_list_data :
	 				if i.item_code_roll == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom :
	 					count = 1

	 			if count == 1 :
	 				for i in self.packing_list_data :
	 					if i.item_code_roll == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom :
	 						new_total_roll = i.roll_qty
	 						i.roll_qty = new_total_roll + qty_add
	 						i.total_yard_atau_meter = i.yard_atau_meter_per_roll * i.roll_qty
	 						i.total_rate = i.rate * i.roll_qty
						
	 			else :
	 				pp_so = self.append('packing_list_data', {})
	 				pp_so.item_code_roll = self.item_code_variant
	 				pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
	 				pp_so.roll_qty = qty_add
	 				pp_so.total_yard_atau_meter = self.yard_atau_meter * pp_so.roll_qty
	 				pp_so.parent_item = parent_item
	 				pp_so.item_name = item_name
	 				pp_so.warehouse = self.warehouse
	 				pp_so.colour = self.colour
	 				pp_so.inventory_uom = self.inventory_uom
	 				pp_so.rate = self.rate
					pp_so.total_rate = self.rate * pp_so.roll_qty

	 		else :
	 			pp_so = self.append('packing_list_data', {})
	 			pp_so.item_code_roll = self.item_code_variant
	 			pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
	 			pp_so.roll_qty = qty_add
	 			pp_so.total_yard_atau_meter = self.yard_atau_meter * pp_so.roll_qty
	 			pp_so.parent_item = parent_item
	 			pp_so.item_name = item_name
	 			pp_so.warehouse = self.warehouse
	 			pp_so.colour = self.colour
	 			pp_so.inventory_uom = self.inventory_uom
				pp_so.rate = self.rate
	 			pp_so.total_rate = self.rate * pp_so.roll_qty
			
	 	else :
	 		frappe.throw("Item Code / Colour / Warehouse / Qty / Yard / Meter tidak terisi")

	def add_pcs(self):
	 	count = 0
		if not self.qty_pcs :
			frappe.throw("Item Code / Warehouse / Qty tidak terisi")
		add_qty = self.qty_pcs
		if self.is_return :
			if add_qty > 0 :
				add_qty = 0-add_qty
	 	if self.item_code_pcs and self.warehouse_pcs :
	 		parent_item = frappe.get_value("Item", self.item_code_pcs,"variant_of")
	 		item_name = frappe.get_value("Item", self.item_code_pcs,"item_name")
	 		if self.packing_list_data_pcs :
	 			for i in self.packing_list_data_pcs :
	 				if i.item_code_pcs == self.item_code_pcs and i.warehouse == self.warehouse_pcs :
	 					count = 1

	 			if count == 1 :
	 				for i in self.packing_list_data_pcs :
	 					if i.item_code_pcs == self.item_code_pcs and i.warehouse == self.warehouse_pcs :
	 						i.pcs_qty = i.pcs_qty + add_qty
	 						i.total_rate = i.pcs_qty * i.rate
	 			else :
	 				pp_so = self.append('packing_list_data_pcs', {})
	 				pp_so.item_code_pcs = self.item_code_pcs
	 				pp_so.pcs_qty = add_qty
	 				pp_so.parent_item_pcs = parent_item
	 				pp_so.item_name_pcs = item_name
	 				pp_so.warehouse = self.warehouse_pcs
	 				pp_so.pcs_uom = self.uom_pcs
					pp_so.rate = self.rate_pcs
	 				pp_so.total_rate = pp_so.rate * pp_so.pcs_qty

	 		else :
	 			pp_so = self.append('packing_list_data_pcs', {})
	 			pp_so.item_code_pcs = self.item_code_pcs
	 			pp_so.pcs_qty = add_qty
	 			pp_so.parent_item_pcs = parent_item
	 			pp_so.item_name_pcs = item_name
	 			pp_so.warehouse = self.warehouse_pcs
	 			pp_so.pcs_uom = self.uom_pcs
				pp_so.rate = self.rate_pcs
	 			pp_so.total_rate = pp_so.rate * pp_so.pcs_qty
			
	 	else :
	 		frappe.throw("Item Code / Warehouse / Qty tidak terisi")


	# def get_item(self):
	# 	if self.group_item :
	# 		get_data_group = frappe.db.sql("""
	# 			SELECT
	# 			gi.`group_code`,
	# 			gi.`uom`,

	# 			dg.`item_code_variant`,
	# 			dg.`item_name`,
	# 			dg.`parent_item`,
	# 			dg.`colour`,
	# 			dg.`yard_atau_meter`,
	# 			dg.`warehouse`,
	# 			dg.`inventory_uom`,

	# 			dg.`item_code_pcs`,
	# 			dg.`item_name_pcs`,
	# 			dg.`parent_item_pcs`,
	# 			dg.`warehouse_pcs`,
	# 			dg.`uom_pcs`


	# 			FROM `tabGroup Item` gi
	# 			JOIN `tabData Group` dg
	# 			ON gi.`name` = dg.`parent`
	# 			WHERE gi.`is_active` = 1
	# 			AND gi.`group_code` = "{}"

	# 		""".format(self.group_item))


	# 		if get_data_group :
	# 			for dg in get_data_group :
	# 				if dg[1] == "PCS" :
	# 					count = 0
	# 					if self.packing_list_data_pcs :
	# 						for i in self.packing_list_data_pcs :
	# 							if i.item_code_pcs == dg[9] and i.warehouse_pcs == dg[12] and i.group_pcs == dg[0] :
	# 								count = 1

	# 						if count == 1 :
	# 							for i in self.packing_list_data_pcs :
	# 								if i.item_code_pcs == dg[9] and i.warehouse_pcs == dg[12] and i.group_pcs == dg[0] :
	# 									new_total_pcs = i.total_pcs
	# 									i.total_pcs = new_total_pcs + 1
									
	# 						else :
	# 							pp_so = self.append('packing_list_data_pcs', {})
	# 							pp_so.item_code_pcs = dg[9]
	# 							pp_so.total_pcs = 1
	# 							pp_so.parent_item_pcs = dg[11]
	# 							pp_so.item_name_pcs = dg[10]
	# 							pp_so.warehouse_pcs = dg[12]
	# 							pp_so.uom_pcs = dg[13]
	# 							pp_so.group_pcs = dg[0]	

	# 					else :
	# 						pp_so = self.append('packing_list_data_pcs', {})
	# 						pp_so.item_code_pcs = dg[9]
	# 						pp_so.total_pcs = 1
	# 						pp_so.parent_item_pcs = dg[11]
	# 						pp_so.item_name_pcs = dg[10]
	# 						pp_so.warehouse_pcs = dg[12]
	# 						pp_so.uom_pcs = dg[13]
	# 						pp_so.group_pcs = dg[0]
								

	# 				else :
	# 					count = 0
	# 					if self.packing_list_data :
	# 						for i in self.packing_list_data :
	# 							if i.item_code_variant == dg[2] and i.yard_atau_meter_per_roll == dg[6] and i.warehouse == dg[7] and i.colour == dg[5] and i.group == dg[0] and i.inventory_uom == dg[8] :
	# 								count = 1

	# 						if count == 1 :
	# 							for i in self.packing_list_data :
	# 								if i.item_code_variant == dg[2] and i.yard_atau_meter_per_roll == dg[6] and i.warehouse == dg[7] and i.colour == dg[5] and i.group == dg[0] and i.inventory_uom == dg[8] :
	# 									new_total_yard_atau_meter = i.total_yard_atau_meter
	# 									new_total_roll = i.total_roll
	# 									i.total_roll = new_total_roll + 1
	# 									i.total_yard_atau_meter = new_total_yard_atau_meter + dg[6]
									
	# 						else :
	# 							pp_so = self.append('packing_list_data', {})
	# 							pp_so.item_code_variant = dg[2]
	# 							pp_so.yard_atau_meter_per_roll = dg[6]
	# 							pp_so.total_yard_atau_meter = dg[6]
	# 							pp_so.total_roll = 1
	# 							pp_so.group = dg[0]
	# 							pp_so.parent_item = dg[4]
	# 							pp_so.item_name = dg[3]
	# 							pp_so.warehouse = dg[7]
	# 							pp_so.colour = dg[5]
	# 							pp_so.inventory_uom = dg[8]	

	# 					else :
	# 						pp_so = self.append('packing_list_data', {})
	# 						pp_so.item_code_variant = dg[2]
	# 						pp_so.yard_atau_meter_per_roll = dg[6]
	# 						pp_so.total_yard_atau_meter = dg[6]
	# 						pp_so.total_roll = 1
	# 						pp_so.group = dg[0]
	# 						pp_so.parent_item = dg[4]
	# 						pp_so.item_name = dg[3]
	# 						pp_so.warehouse = dg[7]
	# 						pp_so.colour = dg[5]
	# 						pp_so.inventory_uom = dg[8]	
						
	# 		else :
	# 			frappe.throw("Group Tidak Active / Tidak Memiliki Item")

	# 	else :
	# 		frappe.throw("Group Item belum dipilih")

	# def add_item(self):
	# 	count = 0


	# 	if self.item_code_variant and self.yard_atau_meter :
	# 		parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
	# 		item_name = frappe.get_doc("Item", self.item_code_variant).item_name
	# 		if self.packing_list_data :
	# 			for i in self.packing_list_data :
	# 				if i.item_code_variant == self.item_code_variant and i.yard_per_roll == self.yard_atau_meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour :
	# 					count = 1

	# 			if count == 1 :
	# 				for i in self.packing_list_data :
	# 					if i.item_code_variant == self.item_code_variant and i.yard_per_roll == self.yard_atau_meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour  :
	# 						new_total_yard = i.total_yard
	# 						new_total_roll = i.total_roll
	# 						i.total_roll = new_total_roll + 1
	# 						i.total_yard = new_total_yard + self.yard_atau_meter
				
	# 			else :
	# 				pp_so = self.append('packing_list_data', {})
	# 				pp_so.item_code_variant = self.item_code_variant
	# 				pp_so.yard_per_roll = self.yard_atau_meter
	# 				pp_so.total_yard = self.yard_atau_meter
	# 				pp_so.total_roll = 1
	# 				pp_so.parent_item = parent_item
	# 				pp_so.item_name = item_name
	# 				pp_so.warehouse = self.warehouse
	# 				pp_so.colour = self.colour
					

	# 		else :
	# 			pp_so = self.append('packing_list_data', {})
	# 			pp_so.item_code_variant = self.item_code_variant
	# 			pp_so.yard_per_roll = self.yard_atau_meter
	# 			pp_so.total_yard = self.yard_atau_meter
	# 			pp_so.total_roll = 1
	# 			pp_so.parent_item = parent_item
	# 			pp_so.item_name = item_name
	# 			pp_so.warehouse = self.warehouse
	# 			pp_so.colour = self.colour
				

	# 	elif self.item_code_variant and self.meter :
	# 		parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
	# 		item_name = frappe.get_doc("Item", self.item_code_variant).item_name
	# 		if self.packing_list_data :
	# 			for i in self.packing_list_data :
	# 				if i.item_code_variant == self.item_code_variant and i.meter_per_roll == self.meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour :
	# 					count = 1

	# 			if count == 1 :
	# 				for i in self.packing_list_data :
	# 					if i.item_code_variant == self.item_code_variant and i.meter_per_roll == self.meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour  :
	# 						new_total_meter = i.total_meter
	# 						new_total_roll = i.total_roll
	# 						i.total_roll = new_total_roll + 1
	# 						i.total_meter = new_total_meter + self.meter
	# 			else :
	# 				pp_so = self.append('packing_list_data', {})
	# 				pp_so.item_code_variant = self.item_code_variant
	# 				pp_so.meter_per_roll = self.meter
	# 				pp_so.total_meter = self.meter
	# 				pp_so.total_roll = 1
	# 				pp_so.parent_item = parent_item
	# 				pp_so.item_name = item_name
	# 				pp_so.warehouse = self.warehouse
	# 				pp_so.colour = self.colour
					

	# 		else :
	# 			pp_so = self.append('packing_list_data', {})
	# 			pp_so.item_code_variant = self.item_code_variant
	# 			pp_so.meter_per_roll = self.meter
	# 			pp_so.total_meter = self.meter
	# 			pp_so.total_roll = 1
	# 			pp_so.parent_item = parent_item
	# 			pp_so.item_name = item_name
	# 			pp_so.warehouse = self.warehouse
	# 			pp_so.colour = self.colour
				

	# 	else :
	# 		frappe.throw("Item Code / Yard tidak terisi")




	# def get_item(self):
	# 	if self.group_item :
	# 		get_data_group = frappe.db.sql("""
	# 			SELECT
	# 			gi.`group_code`,
	# 			dg.`item_code_variant`,
	# 			dg.`yard_per_roll`,
	# 			dg.`item_name`,
	# 			dg.`parent_item`,
	# 			dg.`warehouse`,
	# 			dg.`colour`,
	# 			dg.`design`
	# 			FROM `tabGroup Item` gi
	# 			JOIN `tabData Group` dg
	# 			ON gi.`name` = dg.`parent`
	# 			WHERE gi.`is_active` = 1
	# 			AND gi.`group_code` = "{}"
	# 		""".format(self.group_item))

	# 		if get_data_group :
	# 			for dg in get_data_group :
	# 				cek_inventory = frappe.db.sql("""
	# 					SELECT
	# 					di.`parent`,
	# 					di.`item_code_variant`,
	# 					di.`yard_per_roll`,
	# 					di.`warehouse`,
	# 					di.`total_roll`,
	# 					di.`total_yard`
	# 					FROM
	# 					`tabData Inventory` di
	# 					WHERE di.`parent` = "{}"
	# 					AND di.`item_code_variant` = "{}"
	# 					AND di.`warehouse` = "{}"
	# 					AND di.`yard_per_roll` = "{}"
	# 					and di.`colour` = "{}"
	# 					and di.`design` = "{}"
	# 				""".format(dg[4], dg[1], dg[5], dg[2], dg[6], dg[7]))

	# 				if cek_inventory[0][4] <= 0 or cek_inventory[0][5] <= 0 :
	# 					frappe.throw("Group "+self.group_item+" tidak dapat dijual sebagai group karena item "+dg[1]+" tidak memiliki stock (stocknya 0) \n Gunakan Add Item biasa untuk menjual bukan sebagai grup")


	# 		if get_data_group :
	# 			for dg in get_data_group :
	# 				count = 0
	# 				if self.packing_list_data :
	# 					for i in self.packing_list_data :
	# 						if i.item_code_variant == dg[1] and i.yard_per_roll == dg[2] and i.group == dg[0] and i.warehouse == dg[5] and i.colour == dg[6] and i.design == dg[7] :
	# 							count = 1

	# 					if count == 1 :
	# 						for i in self.packing_list_data :
	# 							if i.item_code_variant == dg[1] and i.yard_per_roll == dg[2] and i.group == dg[0] and i.warehouse == dg[5]  and i.colour == dg[6] and i.design == dg[7] :
	# 								new_total_yard = i.total_yard
	# 								new_total_roll = i.total_roll
	# 								i.total_roll = new_total_roll + 1
	# 								i.total_yard = new_total_yard + dg[2]
	# 					else :
	# 						if dg[0] :
	# 							pp_so = self.append('packing_list_data', {})
	# 							pp_so.item_code_variant = dg[1]
	# 							pp_so.yard_per_roll = dg[2]
	# 							pp_so.total_yard = dg[2]
	# 							pp_so.total_roll = 1
	# 							pp_so.group = dg[0]
	# 							pp_so.parent_item = dg[4]
	# 							pp_so.item_name = dg[3]
	# 							pp_so.warehouse = dg[5]
	# 							pp_so.colour = dg[6]
	# 							pp_so.design = dg[7]
							
	# 				else :
	# 					if dg[0] :
	# 						pp_so = self.append('packing_list_data', {})
	# 						pp_so.item_code_variant = dg[1]
	# 						pp_so.yard_per_roll = dg[2]
	# 						pp_so.total_yard = dg[2]
	# 						pp_so.total_roll = 1
	# 						pp_so.group = dg[0]
	# 						pp_so.parent_item = dg[4]
	# 						pp_so.item_name = dg[3]
	# 						pp_so.warehouse = dg[5]
	# 						pp_so.colour = dg[6]
	# 						pp_so.design = dg[7]
						
	# 		else :
	# 			frappe.throw("Group Tidak Active / Tidak Memiliki Item")

	# 	else :
	# 		frappe.throw("Group Item belum dipilih")



@frappe.whitelist()
def submit_packing_list_delivery(doc,method):
	pending_order = ""
	temp = ""
	if doc.sales_invoice :
		sales_invoice = frappe.get_doc("Sales Invoice", doc.sales_invoice)
		if sales_invoice.alokasi_barang :
			#alokasi_barang = frappe.get_doc("Alokasi Barang", sales_invoice.alokasi_barang)
			order_processing = frappe.get_doc("Order Processing",sales_invoice.order_processing)
			if order_processing.pending_order :
				pending_order = order_processing.pending_order
				temp = "pending"
			else :
				temp = "tidak"

	if doc.packing_list_data :

		if temp == "pending" :
			get_pld = frappe.db.sql("""
				SELECT
				abd.`item_code_roll`,
				abd.`colour`,
				SUM(abd.`total_yard_atau_meter`),
				SUM(abd.`total_rate`),
				SUM(abd.`roll_qty`)

				FROM `tabPacking List Delivery Data` abd
				WHERE abd.`parent` = "{}"
				GROUP BY abd.`item_code_roll`, abd.`colour`, abd.`yard_atau_meter_per_roll`

			""".format(doc.name))

			for abd in get_pld :
				pending_order = pending_order
				item_code_roll = abd[0]
				colour = abd[1]
				total_qty = abd[4]

				get_data_pending_order = frappe.db.sql("""
					SELECT
					por.`roll_qty`,
					por.`qty_sisa`,
					por.`qty_terkirim`,
					por.`qty_dialokasi`
					FROM `tabPending Order Roll` por
					WHERE por.`parent`= "{}"
					AND por.`item_code_roll` = "{}"
					AND por.`colour` = "{}"
				""".format(pending_order, item_code_roll, colour))

				qty_pending_order = 0
				qty_sisa_pending_order = 0
				qty_terkirim_pending_order = 0
				qty_dialokasi_pending_order = 0

				new_qty_dialokasi_pending_order = 0
				new_qty_sisa_pending_order = 0

				if get_data_pending_order[0][1] :
					qty_sisa_pending_order = get_data_pending_order[0][1]
				
				if get_data_pending_order[0][3] :
					qty_dialokasi_pending_order = get_data_pending_order[0][3]
				else :
					qty_dialokasi_pending_order = 0

				new_qty_dialokasi_pending_order = qty_dialokasi_pending_order - get_data_pending_order[0][0]
				new_qty_sisa_pending_order = qty_sisa_pending_order + get_data_pending_order[0][0]

				frappe.db.sql ("""
					update 
					`tabPending Order Roll` 
					set 
					qty_dialokasi="{0}",
					qty_sisa="{1}"
					where 
					parent = "{2}"
					and
					item_code_roll="{3}"
					and 
					colour = "{4}"
					
					""".format(new_qty_dialokasi_pending_order, new_qty_sisa_pending_order, pending_order, item_code_roll, colour))
					



		for i in doc.packing_list_data :

			#alokasi_barang_detail = i.alokasi_barang_detail
			sales_invoice_detail = i.sales_invoice_detail

			#get_alokasi = frappe.db.sql("""
			#	SELECT
			#	por.`roll_qty`,
			#	por.`qty_sisa`,
			#	por.`qty_terkirim`,
			#	por.`qty_dialokasi`
			#	FROM `tabAlokasi Barang Data` por
			#	WHERE por.`name`= "{}"

			#""".format(alokasi_barang_detail))

			#if get_alokasi[0][1] :
			#	temp_qty_sisa = get_alokasi[0][1]
			#else :
			#	temp_qty_sisa = 0

			#if get_alokasi[0][2] :
			#	temp_qty_terkirim = get_alokasi[0][2]
			#else :
			#	temp_qty_terkirim = 0

			#temp_qty_terkirim = temp_qty_terkirim + i.roll_qty
			#temp_qty_sisa = temp_qty_sisa - i.roll_qty

			#frappe.db.sql ("""
			#	update 
			#	`tabAlokasi Barang Data` 
			#	set 
			#	qty_terkirim="{0}",
			#	qty_sisa="{1}"
			#	where 
			#	name="{2}"
				
			#	""".format(temp_qty_terkirim, temp_qty_sisa, alokasi_barang_detail))


			#get_sales_invoice = frappe.db.sql("""
			#	SELECT
			#	por.`roll_qty`,
			#	por.`qty_sisa`,
			#	por.`qty_terkirim`,
			#	por.`qty_dialokasi`
			#	FROM `tabSales Invoice Data` por
			#	WHERE por.`name`= "{}"

			#""".format(sales_invoice_detail))


			#if get_sales_invoice[0][1] :
			#	temp_qty_sisa = get_sales_invoice[0][1]
			#else :
			#	temp_qty_sisa = 0

			#if get_sales_invoice[0][2] :
			#	temp_qty_terkirim = get_sales_invoice[0][2]
			#else :
			#	temp_qty_terkirim = 0

			#temp_qty_terkirim = temp_qty_terkirim + i.roll_qty
			#temp_qty_sisa = temp_qty_sisa - i.roll_qty

			#frappe.db.sql ("""
			#	update 
			#	`tabSales Invoice Data` 
			#	set 
			#	qty_terkirim="{0}",
			#	qty_sisa="{1}"
			#	where 
			#	name="{2}"
				
			#	""".format(temp_qty_terkirim, temp_qty_sisa, sales_invoice_detail))
			pass
	if doc.packing_list_data_pcs :

		if temp == "pending" :
			for i in doc.packing_list_data_pcs :
				get_pld = frappe.db.sql("""
					SELECT
					por.`pcs_qty`,
					por.`qty_sisa`,
					por.`qty_terkirim`,
					por.`qty_dialokasi`
					FROM `tabPacking List Delivery Pcs` por
					WHERE por.`parent`= "{}"
					AND por.`item_code_pcs` = "{}"

				""".format(pending_order, i.item_code_pcs))

				temp_qty_dialokasi = 0
				temp_qty_sisa = 0

				new_qty_dialokasi = 0
				new_qty_sisa = 0

				if get_pld[0][3] :
					temp_qty_dialokasi = get_pld[0][3]
				else :
					temp_qty_dialokasi = 0

				if get_pld[0][1] :
					temp_qty_sisa = get_pld[0][1]

				new_qty_dialokasi = temp_qty_dialokasi + i.pcs_qty
				new_qty_sisa = temp_qty_sisa - i.pcs_qty

				frappe.db.sql ("""
					update 
					`tabPending Order Pcs` 
					set 
					qty_dialokasi="{0}",
					qty_sisa = "{1}"
					where 
					item_code_pcs="{2}"
					
					""".format(new_qty_dialokasi, new_qty_sisa, i.item_code_pcs))


		for i in doc.packing_list_data_pcs :
			alokasi_barang_detail = i.alokasi_barang_detail
			sales_invoice_detail = i.sales_invoice_detail

			get_alokasi = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabAlokasi Barang Pcs` por
				WHERE por.`name`= "{}"

			""".format(alokasi_barang_detail))

			if get_alokasi[0][1] :
				temp_qty_sisa = get_alokasi[0][1]
			else :
				temp_qty_sisa = 0

			if get_alokasi[0][2] :
				temp_qty_terkirim = get_alokasi[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim + i.pcs_qty
			temp_qty_sisa = temp_qty_sisa - i.pcs_qty

			frappe.db.sql ("""
				update 
				`tabAlokasi Barang Pcs` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, alokasi_barang_detail))



			get_sales_invoice = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabSales Invoice Pcs` por
				WHERE por.`name`= "{}"

			""".format(sales_invoice_detail))


			if get_sales_invoice[0][1] :
				temp_qty_sisa = get_sales_invoice[0][1]
			else :
				temp_qty_sisa = 0

			if get_sales_invoice[0][2] :
				temp_qty_terkirim = get_sales_invoice[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim + i.pcs_qty
			temp_qty_sisa = temp_qty_sisa - i.pcs_qty

			frappe.db.sql ("""
				update 
				`tabSales Invoice Pcs` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, sales_invoice_detail))


	# if doc.alokasi_barang :
	# 	if doc.packing_list_data : 
	# 		for i in doc.packing_list_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`roll_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabAlokasi Barang Data` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_roll` = "{}"
	# 				AND por.`colour` = "{}"

	# 			""".format(doc.alokasi_barang, i.item_code_roll, i.colour))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi - i.roll_qty
	# 			new_qty_terkirim = temp_qty_terkirim + i.roll_qty
	# 			new_qty_sisa = temp_qty_sisa - i.roll_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabAlokasi Barang Data` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_roll="{3}"
	# 				and 
	# 				colour = "{4}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_roll, i.colour))

	# 		for i in doc.packing_list_data :
	# 				get_data_pending_order = frappe.db.sql("""
	# 					SELECT
	# 					por.`roll_qty`,
	# 					por.`qty_sisa`,
	# 					por.`qty_terkirim`,
	# 					por.`qty_dialokasi`
	# 					FROM `tabPending Order Roll` por
	# 					WHERE por.`parent`= "{}"
	# 					AND por.`item_code_roll` = "{}"
	# 					AND por.`colour` = "{}"

	# 				""".format(doc.pending_order, i.item_code_roll, i.colour))
	# 				if get_data_pending_order[0][3] :
	# 					temp_qty_dialokasi = get_data_pending_order[0][3]
	# 				else :
	# 					temp_qty_dialokasi = 0

	# 				if get_data_pending_order[0][2] :
	# 					temp_qty_terkirim = get_data_pending_order[0][2]
	# 				else :
	# 					temp_qty_terkirim = 0


	# 				if get_data_pending_order[0][1] :
	# 					temp_qty_sisa = get_data_pending_order[0][1]
	# 				else :
	# 					temp_qty_sisa = 0

	# 				new_qty_dialokasi = temp_qty_dialokasi - i.roll_qty
	# 				new_qty_terkirim = temp_qty_terkirim + i.roll_qty
	# 				new_qty_sisa = temp_qty_sisa - i.roll_qty

	# 				frappe.db.sql ("""
	# 					update 
	# 					`tabPending Order Roll` 
	# 					set 
	# 					qty_dialokasi="{0}",
	# 					qty_terkirim="{1}",
	# 					qty_sisa="{2}"
	# 					where 
	# 					item_code_roll="{3}"
	# 					and 
	# 					colour = "{4}"
						
	# 					""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_roll, i.colour))
					

	# 	if doc.packing_list_data_pcs :
	# 		for i in doc.packing_list_data_pcs :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabAlokasi Barang Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.alokasi_barang, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi - i.pcs_qty
	# 			new_qty_terkirim = temp_qty_terkirim + i.pcs_qty
	# 			new_qty_sisa = temp_qty_sisa - i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabAlokasi Barang Pcs` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_pcs="{3}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_pcs))

	# 		for i in doc.packing_list_data_pcs :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.pending_order, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi - i.pcs_qty
	# 			new_qty_terkirim = temp_qty_terkirim + i.pcs_qty
	# 			new_qty_sisa = temp_qty_sisa - i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Pcs` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_pcs="{3}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_pcs))


	# pass
	

				# frappe.db.commit()


@frappe.whitelist()
def cancel_packing_list_delivery(doc,method):

	if doc.sales_invoice :
		sales_invoice = frappe.get_doc("Sales Invoice", doc.sales_invoice)
		if sales_invoice.alokasi_barang :
			alokasi_barang = frappe.get_doc("Alokasi Barang", sales_invoice.alokasi_barang)
			if alokasi_barang.pending_order :
				pending_order = alokasi_barang.pending_order
				temp = "pending"
			else :
				temp = "tidak"

	if doc.packing_list_data :

		if temp == "pending" :
			get_pld = frappe.db.sql("""
				SELECT
				abd.`item_code_roll`,
				abd.`colour`,
				SUM(abd.`total_yard_atau_meter`),
				SUM(abd.`total_rate`),
				SUM(abd.`roll_qty`)

				FROM `tabPacking List Delivery Data` abd
				WHERE abd.`parent` = "{}"
				GROUP BY abd.`item_code_roll`, abd.`colour`, abd.`yard_atau_meter_per_roll`

			""".format(doc.name))

			for abd in get_pld :
				pending_order = pending_order
				item_code_roll = abd[0]
				colour = abd[1]
				total_qty = abd[4]

				get_data_pending_order = frappe.db.sql("""
					SELECT
					por.`roll_qty`,
					por.`qty_sisa`,
					por.`qty_terkirim`,
					por.`qty_dialokasi`
					FROM `tabPending Order Roll` por
					WHERE por.`parent`= "{}"
					AND por.`item_code_roll` = "{}"
					AND por.`colour` = "{}"
				""".format(pending_order, item_code_roll, colour))

				qty_pending_order = 0
				qty_sisa_pending_order = 0
				qty_terkirim_pending_order = 0
				qty_dialokasi_pending_order = 0

				new_qty_dialokasi_pending_order = 0
				new_qty_sisa_pending_order = 0

				if get_data_pending_order[0][1] :
					qty_sisa_pending_order = get_data_pending_order[0][1]
				
				if get_data_pending_order[0][3] :
					qty_dialokasi_pending_order = get_data_pending_order[0][3]
				else :
					qty_dialokasi_pending_order = 0

				new_qty_dialokasi_pending_order = qty_dialokasi_pending_order + get_data_pending_order[0][0]
				new_qty_sisa_pending_order = qty_sisa_pending_order - get_data_pending_order[0][0]

				frappe.db.sql ("""
					update 
					`tabPending Order Roll` 
					set 
					qty_dialokasi="{0}",
					qty_sisa="{1}"
					where 
					parent = "{2}"
					and
					item_code_roll="{3}"
					and 
					colour = "{4}"
					
					""".format(new_qty_dialokasi_pending_order, new_qty_sisa_pending_order, pending_order, item_code_roll, colour))
					



		for i in doc.packing_list_data :

			alokasi_barang_detail = i.alokasi_barang_detail
			sales_invoice_detail = i.sales_invoice_detail

			get_alokasi = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabAlokasi Barang Data` por
				WHERE por.`name`= "{}"

			""".format(alokasi_barang_detail))

			if get_alokasi[0][1] :
				temp_qty_sisa = get_alokasi[0][1]
			else :
				temp_qty_sisa = 0

			if get_alokasi[0][2] :
				temp_qty_terkirim = get_alokasi[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim - i.roll_qty
			temp_qty_sisa = temp_qty_sisa + i.roll_qty

			frappe.db.sql ("""
				update 
				`tabAlokasi Barang Data` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, alokasi_barang_detail))


			get_sales_invoice = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabSales Invoice Data` por
				WHERE por.`name`= "{}"

			""".format(sales_invoice_detail))


			if get_sales_invoice[0][1] :
				temp_qty_sisa = get_sales_invoice[0][1]
			else :
				temp_qty_sisa = 0

			if get_sales_invoice[0][2] :
				temp_qty_terkirim = get_sales_invoice[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim - i.roll_qty
			temp_qty_sisa = temp_qty_sisa + i.roll_qty

			frappe.db.sql ("""
				update 
				`tabSales Invoice Data` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, sales_invoice_detail))

	if doc.packing_list_data_pcs :

		if temp == "pending" :
			for i in doc.packing_list_data_pcs :
				get_pld = frappe.db.sql("""
					SELECT
					por.`pcs_qty`,
					por.`qty_sisa`,
					por.`qty_terkirim`,
					por.`qty_dialokasi`
					FROM `tabPacking List Delivery Pcs` por
					WHERE por.`parent`= "{}"
					AND por.`item_code_pcs` = "{}"

				""".format(pending_order, i.item_code_pcs))

				temp_qty_dialokasi = 0
				temp_qty_sisa = 0

				new_qty_dialokasi = 0
				new_qty_sisa = 0

				if get_pld[0][3] :
					temp_qty_dialokasi = get_pld[0][3]
				else :
					temp_qty_dialokasi = 0

				if get_pld[0][1] :
					temp_qty_sisa = get_pld[0][1]

				new_qty_dialokasi = temp_qty_dialokasi - i.pcs_qty
				new_qty_sisa = temp_qty_sisa + i.pcs_qty

				frappe.db.sql ("""
					update 
					`tabPending Order Pcs` 
					set 
					qty_dialokasi="{0}",
					qty_sisa = "{1}"
					where 
					item_code_pcs="{2}"
					
					""".format(new_qty_dialokasi, new_qty_sisa, i.item_code_pcs))


		for i in doc.packing_list_data_pcs :
			alokasi_barang_detail = i.alokasi_barang_detail
			sales_invoice_detail = i.sales_invoice_detail

			get_alokasi = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabAlokasi Barang Pcs` por
				WHERE por.`name`= "{}"

			""".format(alokasi_barang_detail))

			if get_alokasi[0][1] :
				temp_qty_sisa = get_alokasi[0][1]
			else :
				temp_qty_sisa = 0

			if get_alokasi[0][2] :
				temp_qty_terkirim = get_alokasi[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim - i.pcs_qty
			temp_qty_sisa = temp_qty_sisa + i.pcs_qty

			frappe.db.sql ("""
				update 
				`tabAlokasi Barang Pcs` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, alokasi_barang_detail))



			get_sales_invoice = frappe.db.sql("""
				SELECT
				por.`roll_qty`,
				por.`qty_sisa`,
				por.`qty_terkirim`,
				por.`qty_dialokasi`
				FROM `tabSales Invoice Pcs` por
				WHERE por.`name`= "{}"

			""".format(sales_invoice_detail))


			if get_sales_invoice[0][1] :
				temp_qty_sisa = get_sales_invoice[0][1]
			else :
				temp_qty_sisa = 0

			if get_sales_invoice[0][2] :
				temp_qty_terkirim = get_sales_invoice[0][2]
			else :
				temp_qty_terkirim = 0

			temp_qty_terkirim = temp_qty_terkirim - i.pcs_qty
			temp_qty_sisa = temp_qty_sisa + i.pcs_qty

			frappe.db.sql ("""
				update 
				`tabSales Invoice Pcs` 
				set 
				qty_terkirim="{0}",
				qty_sisa="{1}"
				where 
				name="{2}"
				
				""".format(temp_qty_terkirim, temp_qty_sisa, sales_invoice_detail))



	# code lama
	# if doc.alokasi_barang :
	# 	if doc.packing_list_data : 
	# 		for i in doc.packing_list_data :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`roll_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabAlokasi Barang Data` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_roll` = "{}"
	# 				AND por.`colour` = "{}"

	# 			""".format(doc.alokasi_barang, i.item_code_roll, i.colour))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi + i.roll_qty
	# 			new_qty_terkirim = temp_qty_terkirim - i.roll_qty
	# 			new_qty_sisa = temp_qty_sisa + i.roll_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabAlokasi Barang Data` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_roll="{3}"
	# 				and 
	# 				colour = "{4}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_roll, i.colour))

	# 		for i in doc.packing_list_data :
	# 				get_data_pending_order = frappe.db.sql("""
	# 					SELECT
	# 					por.`roll_qty`,
	# 					por.`qty_sisa`,
	# 					por.`qty_terkirim`,
	# 					por.`qty_dialokasi`
	# 					FROM `tabPending Order Roll` por
	# 					WHERE por.`parent`= "{}"
	# 					AND por.`item_code_roll` = "{}"
	# 					AND por.`colour` = "{}"

	# 				""".format(doc.pending_order, i.item_code_roll, i.colour))
	# 				if get_data_pending_order[0][3] :
	# 					temp_qty_dialokasi = get_data_pending_order[0][3]
	# 				else :
	# 					temp_qty_dialokasi = 0

	# 				if get_data_pending_order[0][2] :
	# 					temp_qty_terkirim = get_data_pending_order[0][2]
	# 				else :
	# 					temp_qty_terkirim = 0


	# 				if get_data_pending_order[0][1] :
	# 					temp_qty_sisa = get_data_pending_order[0][1]
	# 				else :
	# 					temp_qty_sisa = 0

	# 				new_qty_dialokasi = temp_qty_dialokasi + i.roll_qty
	# 				new_qty_terkirim = temp_qty_terkirim - i.roll_qty
	# 				new_qty_sisa = temp_qty_sisa + i.roll_qty

	# 				frappe.db.sql ("""
	# 					update 
	# 					`tabPending Order Roll` 
	# 					set 
	# 					qty_dialokasi="{0}",
	# 					qty_terkirim="{1}",
	# 					qty_sisa="{2}"
	# 					where 
	# 					item_code_roll="{3}"
	# 					and 
	# 					colour = "{4}"
						
	# 					""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_roll, i.colour))
					

	# 	if doc.packing_list_data_pcs :
	# 		for i in doc.packing_list_data_pcs :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabAlokasi Barang Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.alokasi_barang, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi + i.pcs_qty
	# 			new_qty_terkirim = temp_qty_terkirim - i.pcs_qty
	# 			new_qty_sisa = temp_qty_sisa + i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabAlokasi Barang Pcs` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_pcs="{3}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_pcs))

	# 		for i in doc.packing_list_data_pcs :
	# 			get_data_pending_order = frappe.db.sql("""
	# 				SELECT
	# 				por.`pcs_qty`,
	# 				por.`qty_sisa`,
	# 				por.`qty_terkirim`,
	# 				por.`qty_dialokasi`
	# 				FROM `tabPending Order Pcs` por
	# 				WHERE por.`parent`= "{}"
	# 				AND por.`item_code_pcs` = "{}"

	# 			""".format(doc.pending_order, i.item_code_pcs))
	# 			if get_data_pending_order[0][3] :
	# 				temp_qty_dialokasi = get_data_pending_order[0][3]
	# 			else :
	# 				temp_qty_dialokasi = 0

	# 			if get_data_pending_order[0][2] :
	# 				temp_qty_terkirim = get_data_pending_order[0][2]
	# 			else :
	# 				temp_qty_terkirim = 0


	# 			if get_data_pending_order[0][1] :
	# 				temp_qty_sisa = get_data_pending_order[0][1]
	# 			else :
	# 				temp_qty_sisa = 0

	# 			new_qty_dialokasi = temp_qty_dialokasi + i.pcs_qty
	# 			new_qty_terkirim = temp_qty_terkirim - i.pcs_qty
	# 			new_qty_sisa = temp_qty_sisa + i.pcs_qty

	# 			frappe.db.sql ("""
	# 				update 
	# 				`tabPending Order Pcs` 
	# 				set 
	# 				qty_dialokasi="{0}",
	# 				qty_terkirim="{1}",
	# 				qty_sisa="{2}"
	# 				where 
	# 				item_code_pcs="{3}"
					
	# 				""".format(new_qty_dialokasi, new_qty_terkirim, new_qty_sisa,  i.item_code_pcs))

	# pass
	

				# frappe.db.commit()



@frappe.whitelist()
def create_delivery_note(doc,method):
	if doc.is_return : 
		cek_data = frappe.db.sql("""
			SELECT prec.`name` FROM `tabDelivery Note` prec
			WHERE prec.`packing_list_delivery` = "{}"
			AND prec.`docstatus` = 1
		""".format(doc.return_against))


		pr_doc = frappe.new_doc("Delivery Note")
		pr_doc.update({
			"customer": doc.customer,
			# "customer_name" : doc.customer_name,
			"posting_date" : doc.posting_date,
			"packing_list_delivery" : doc.name,
			"is_return" : 1,
			"return_against" : cek_data[0][0]

		})
	else :
		pr_doc = frappe.new_doc("Delivery Note")
		pr_doc.update({
			"customer": doc.customer,
			# "customer_name" : doc.customer_name,
			"posting_date" : doc.posting_date,
			"packing_list_delivery" : doc.name
		})

	

	item_code = ""
	item_name = ""
	description = ""
	qty = 0
	stock_uom = ""
	rate = 0
	total_rate = 0
	warehouse = ""

	count = 0
	length_arr = len(doc.packing_list_data)

	for i in doc.packing_list_data :
		if item_code == i.item_code_roll :
			
			qty = qty + i.total_yard_atau_meter
			total_rate = total_rate + i.total_rate
			
			count = count + 1

			if count == length_arr :
				pr_doc.append("items", {
					"item_code": item_code,
					"item_name": item_name,
					"description": description,
					"stock_uom": stock_uom,
					"qty": qty,
					"rate" : rate,
					"total_rate" : total_rate,
					"warehouse": warehouse
				})

		else :
			if count == 0 :

				item_code = i.item_code_roll
				item_name = i.item_name_roll
				description = i.item_name_roll
				received_qty = i.total_yard_atau_meter
				qty = i.total_yard_atau_meter
				stock_uom = i.inventory_uom
				rate = i.total_rate / i.total_yard_atau_meter
				total_rate = i.total_rate
				warehouse = i.warehouse
				
				count = count + 1


				if count == length_arr :
					pr_doc.append("items", {
						"item_code": item_code,
						"item_name": item_name,
						"description": description,
						"stock_uom": stock_uom,
						"qty": qty,
						"rate" : rate,
						"total_rate" : total_rate,
						"warehouse": warehouse
					})
					

			else :
				pr_doc.append("items", {
					"item_code": item_code,
					"item_name": item_name,
					"description": description,
					"stock_uom": stock_uom,
					"qty": qty,
					"rate" : rate,
					"total_rate" : total_rate,
					"warehouse": warehouse
				})
				
				item_code = i.item_code_roll
				item_name = i.item_name_roll
				description = i.item_name_roll
				received_qty = i.total_yard_atau_meter
				qty = i.total_yard_atau_meter
				stock_uom = i.inventory_uom
				rate = i.total_rate / i.total_yard_atau_meter
				total_rate = i.total_rate
				warehouse = i.warehouse

				count = count + 1

				if count == length_arr :
					pr_doc.append("items", {
						"item_code": item_code,
						"item_name": item_name,
						"description": description,
						"stock_uom": stock_uom,
						"qty": qty,
						"rate" : rate,
						"total_rate" : total_rate,
						"warehouse": warehouse
					})

	if doc.packing_list_data_pcs :
		for i in doc.packing_list_data_pcs :

			pr_doc.append("items", {
				"item_code": i.item_code_pcs,
				"item_name": i.item_name_pcs,
				"description": i.item_name_pcs,
				"stock_uom": i.pcs_uom,
				"qty": i.pcs_qty,
				"rate" : i.rate,
				"total_rate" : i.total_rate,
				"warehouse": i.warehouse
			})

	pr_doc.flags.ignore_permissions = 1
	pr_doc.submit()


@frappe.whitelist()
def cancel_delivery_note(doc,method):
	get_prec = frappe.db.sql("""
		SELECT
		pr.`name`,
		pr.`packing_list_delivery`
		FROM `tabDelivery Note` pr
		WHERE pr.`packing_list_delivery` = "{}"
	""".format(doc.name))

	pr_doc = frappe.get_doc("Delivery Note", get_prec[0][0])
	pr_doc.flags.ignore_permissions = 1
	pr_doc.cancel()




@frappe.whitelist()
def save_packing_list_delivery(doc,method):

	if doc.packing_list_data :
		for i in doc.packing_list_data :
			item = frappe.get_doc("Item", i.item_code_roll)
			i.item_name_roll = item.item_name
			i.inventory_uom = item.stock_uom
			i.warehouse = item.default_warehouse
			i.total_yard_atau_meter = float(i.roll_qty) * float(i.yard_atau_meter_per_roll)
			if i.rate :
				i.total_rate = float(i.rate) * float(i.yard_atau_meter_per_roll)


	if doc.packing_list_data_pcs :
		for i in doc.packing_list_data_pcs :
			item = frappe.get_doc("Item", i.item_code_pcs)
			i.item_name_pcs = item.item_name
			i.pcs_uom = item.stock_uom
			i.warehouse = item.default_warehouse
			if i.rate :
				i.total_rate = float(i.rate) * float(i.pcs_qty)

	
	if doc.is_return :
		prev_doc = doc.return_against

		arr_total_roll = frappe.db.sql("""
			SELECT
			SUM(plrd.`total_yard_atau_meter`)
			FROM `tabPacking List Delivery Data` plrd
			WHERE plrd.`parent` = "{}"
			GROUP BY plrd.`parent`
		""".format(prev_doc))

		arr_total_pcs = frappe.db.sql("""
			SELECT
			SUM(plrc.`total_pcs`)
			FROM `tabPacking List Delivery Pcs` plrc
			WHERE plrc.`parent` = "{}"
			GROUP BY plrc.`parent`
		""".format(prev_doc))

		total_yard = 0
		if doc.packing_list_data :
			for i in doc.packing_list_data :
				total_yard = total_yard + i.total_yard_atau_meter

			if total_yard > arr_total_roll[0] :
				frappe.throw("Tidak dapat di save karena jumlah Yard/Meter retur lebih besar")


		total_pcs = 0
		if doc.packing_list_data_pcs :
			for i in doc.packing_list_data_pcs :
				total_pcs = total_pcs + i.total_pcs

			if total_pcs > arr_total_pcs[0] :
				frappe.throw("Tidak dapat di save karena jumlah Pcs retur lebih besar")








@frappe.whitelist()
def submit_delivery_note(doc,method):
	pass
	# if doc.packing_list_delivery and doc.sales_order:
	# 	frappe.db.sql ("""
	# 		update 
	# 		`tabPacking List Delivery` 
	# 		set 
	# 		is_used=1
	# 		where 
	# 		name="{0}"
	# 		 """.format(doc.packing_list_delivery))

	# 	frappe.db.commit()
		# msgprint("Akan mengganti data di SO yang bersangkutan sesuai dengan Packing List Delivery (masih on progress)")


@frappe.whitelist()
def cancel_delivery_note(doc,method):
	pass
	# if doc.packing_list_delivery and doc.sales_order:
	# 	frappe.db.sql ("""
	# 		update 
	# 		`tabPacking List Delivery` 
	# 		set 
	# 		is_used=1
	# 		where 
	# 		name="{0}"
	# 		 """.format(doc.packing_list_delivery))

	# 	frappe.db.commit()
		# msgprint("Akan mengembalikan data SO seperti semua (masih on progress)")


@frappe.whitelist()
def make_packing_list_delivery_return(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.is_return = 1
		target.return_against = source.name
		target.packing_list_data = []
		target.packing_list_data_pcs = []
		target.posting_date = frappe.utils.data.nowdate()
		target.posting_time = frappe.utils.data.nowtime()

	def update_item_roll(source_doc, target_doc, source_parent):
		target_doc.total_roll = -1* source_doc.total_roll
		target_doc.total_yard_atau_meter = -1* source_doc.total_yard_atau_meter

	def update_item_pcs(source_doc, target_doc, source_parent):
		target_doc.total_pcs = -1* source_doc.total_pcs
		

	target_doc = get_mapped_doc("Packing List Delivery", source_name, {
		"Packing List Delivery": {
			"doctype": "Packing List Delivery",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Packing List Delivery Data": {
			"doctype": "Packing List Delivery Data",
			"postprocess": update_item_roll
		},
		"Packing List Delivery Pcs": {
			"doctype": "Packing List Delivery Pcs",
			"postprocess": update_item_pcs
		}
		
	}, target_doc, set_missing_values)

	return target_doc



@frappe.whitelist()
def get_data_from_sales_invoice(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.sales_invoice = source.name
		#target.alokasi_barang = source.alokasi_barang
		target.customer = source.customer
		target.customer_name = source.customer_name

		target.sales_partner = source.sales_partner
		target.sales_type = "%"
		target.commission_percentage = source.commission_rate
		target.total_commission = source.total_commission
		# target.sales_type == "Rate" :
		# 	target.commission_rate = source.commission_rate
		# 	target.total_commission = source.total_commission
		# else :
		# 	target.commission_percentage = source.commission_percentage
		# 	target.total_commission = source.total_commission


	def update_item_roll(source_doc, target_doc, source_parent):
		target_doc.alokasi_barang_detail = source_doc.alokasi_barang_detail
		target_doc.sales_invoice_detail = source_doc.name
		target_doc.item_code_roll = source_doc.item_code_roll
		target_doc.item_name_roll = source_doc.item_name_roll
		target_doc.yard_atau_meter_per_roll = source_doc.yard_atau_meter
		target_doc.warehouse = source_doc.warehouse
		target_doc.group = source_doc.group
		target_doc.roll_qty = source_doc.roll_qty
		target_doc.colour = source_doc.colour
		target_doc.rate = source_doc.rate
		target_doc.total_rate = source_doc.total_rate
		target_doc.inventory_uom = source_doc.inventory_uom
		target_doc.total_yard_atau_meter = source_doc.total_yard_atau_meter
		target_doc.qty_dialokasi = source_doc.qty_dialokasi
		target_doc.qty_terkirim = source_doc.qty_terkirim
		target_doc.qty_sisa = source_doc.qty_sisa
		

	def update_item_pcs(source_doc, target_doc, source_parent):
		target_doc.item_code_pcs = source_doc.item_code_pcs
		target_doc.item_name_pcs = source_doc.item_name_pcs
		target_doc.pcs_uom = source_doc.pcs_uom
		target_doc.warehouse = source_doc.warehouse
		target_doc.note = source_doc.note
		target_doc.rate = source_doc.rate
		target_doc.total_rate = source_doc.total_rate
		target_doc.pcs_qty = source_doc.pcs_qty
		target_doc.qty_dialokasi = source_doc.qty_dialokasi
		target_doc.qty_sisa = source_doc.qty_sisa
		target_doc.qty_terkirim = source_doc.qty_terkirim


	target_doc = get_mapped_doc("Sales Invoice", source_name, {
		"Sales Invoice": {
			"doctype": "Packing List Delivery",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Order Processing Data Roll": {
			"doctype": "Packing List Delivery Data",
			"postprocess": update_item_roll
		},
		"Order Processing Data Pcs": {
			"doctype": "Packing List Delivery Pcs",
			"postprocess": update_item_pcs
		}
		
	}, target_doc, set_missing_values)

	return target_doc