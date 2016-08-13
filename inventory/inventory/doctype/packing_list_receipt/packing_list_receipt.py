# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint


class PackingListReceipt(Document):
	def add_item(self):
		count = 0

		if self.item_code_variant and self.yard_atau_meter and self.colour and self.warehouse :
			parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
			item_name = frappe.get_doc("Item", self.item_code_variant).item_name
			if self.packing_list_data :
				for i in self.packing_list_data :
					if self.group_prefix and self.group_code :
						if i.item_code_variant == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == self.group_prefix+self.group_code and i.inventory_uom == self.inventory_uom :
							count = 1
					else :
						if i.item_code_variant == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom :
							count = 1

				if count == 1 :
					for i in self.packing_list_data :
						if self.group_prefix and self.group_code :
							if i.item_code_variant == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == self.group_prefix+self.group_code and i.inventory_uom == self.inventory_uom :
								new_total_yard_atau_meter = i.total_yard_atau_meter
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + 1
								i.total_yard_atau_meter = new_total_yard_atau_meter + self.yard_atau_meter
						else :
							if i.item_code_variant == self.item_code_variant and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.inventory_uom == self.inventory_uom :
								new_total_yard_atau_meter = i.total_yard_atau_meter
								new_total_roll = i.total_roll
								i.total_roll = new_total_roll + 1
								i.total_yard_atau_meter = new_total_yard_atau_meter + self.yard_atau_meter
						
				else :
					if self.group_prefix and self.group_code :
						pp_so = self.append('packing_list_data', {})
						pp_so.item_code_variant = self.item_code_variant
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
						pp_so.total_yard_atau_meter = self.yard_atau_meter
						pp_so.total_roll = 1
						pp_so.group = self.group_prefix + self.group_code
						pp_so.parent_item = parent_item
						pp_so.item_name = item_name
						pp_so.warehouse = self.warehouse
						pp_so.colour = self.colour
						pp_so.inventory_uom = self.inventory_uom
						
					else :
						pp_so = self.append('packing_list_data', {})
						pp_so.item_code_variant = self.item_code_variant
						pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
						pp_so.total_yard_atau_meter = self.yard_atau_meter
						pp_so.total_roll = 1
						pp_so.parent_item = parent_item
						pp_so.item_name = item_name
						pp_so.warehouse = self.warehouse
						pp_so.colour = self.colour
						pp_so.inventory_uom = self.inventory_uom

			else :
				if self.group_prefix and self.group_code :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = self.yard_atau_meter
					pp_so.total_roll = 1
					pp_so.group = self.group_prefix + self.group_code
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = self.inventory_uom
					
				else :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = self.yard_atau_meter
					pp_so.total_roll = 1
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = self.inventory_uom
			
		else :
			frappe.throw("Item Code / Colour / Warehouse / Yard / Meter tidak terisi")


	def add_pcs(self):
		count = 0

		if self.item_code_pcs and self.warehouse_pcs :
			parent_item = frappe.get_doc("Item", self.item_code_pcs).variant_of
			item_name = frappe.get_doc("Item", self.item_code_pcs).item_name
			if self.packing_list_data_pcs :
				for i in self.packing_list_data_pcs :
					if self.group_prefix_pcs and self.group_code_pcs :
						if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs and i.group == self.group_prefix_pcs+self.group_code_pcs :
							count = 1
					else :
						if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
							count = 1

				if count == 1 :
					for i in self.packing_list_data_pcs :
						if self.group_prefix_pcs and self.group_code_pcs :
							if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs and i.group == self.group_prefix_pcs+self.group_code_pcs :
								new_total_pcs = i.total_pcs
								i.total_pcs = new_total_pcs + 1
						else :
							if i.item_code_pcs == self.item_code_pcs and i.warehouse_pcs == self.warehouse_pcs :
								new_total_pcs = i.total_pcs
								i.total_pcs = new_total_pcs + 1
				else :
					if self.group_prefix_pcs and self.group_code_pcs :
						pp_so = self.append('packing_list_data_pcs', {})
						pp_so.item_code_pcs = self.item_code_pcs
						pp_so.total_pcs = 1
						pp_so.parent_item_pcs = parent_item
						pp_so.item_name_pcs = item_name
						pp_so.warehouse_pcs = self.warehouse_pcs
						pp_so.uom_pcs = self.uom_pcs
						pp_so.group = self.group_prefix_pcs + self.group_code_pcs
						
					else :
						pp_so = self.append('packing_list_data_pcs', {})
						pp_so.item_code_pcs = self.item_code_pcs
						pp_so.total_pcs = 1
						pp_so.parent_item_pcs = parent_item
						pp_so.item_name_pcs = item_name
						pp_so.warehouse_pcs = self.warehouse_pcs
						pp_so.uom_pcs = self.uom_pcs

			else :
				if self.group_prefix_pcs and self.group_code_pcs :
					pp_so = self.append('packing_list_data_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.total_pcs = 1
					pp_so.parent_item_pcs = parent_item
					pp_so.item_name_pcs = item_name
					pp_so.warehouse_pcs = self.warehouse_pcs
					pp_so.group = self.group_prefix_pcs + self.group_code_pcs
					pp_so.uom_pcs = self.uom_pcs
					
				else :
					pp_so = self.append('packing_list_data_pcs', {})
					pp_so.item_code_pcs = self.item_code_pcs
					pp_so.total_pcs = 1
					pp_so.parent_item_pcs = parent_item
					pp_so.item_name_pcs = item_name
					pp_so.warehouse_pcs = self.warehouse_pcs
					pp_so.uom_pcs = self.uom_pcs
			
		else :
			frappe.throw("Item Code / Warehouse tidak terisi")

@frappe.whitelist()
def submit_packing_list_receipt(doc,method):
	count = 0
	for data in doc.packing_list_data :
		if data.group :
			cek_group = frappe.db.sql("""
				SELECT
				mi.`group_code`
				FROM `tabGroup Item` mi
				WHERE mi.`group_code` = "{}"
				AND mi.`uom` = "{}"
				""".format(data.group, data.group))

			if cek_group :
				cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`
					FROM `tabData Group` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`colour` = "{}"
				""".format(data.item_code_variant, data.yard_atau_meter_per_roll, data.colour))

				if cek_data :
					count = 0
				else :
					
					mi = frappe.get_doc("Group Item", data.group)
					mi.append("data_group", {
					"doctype": "Data Group",
					"item_code_variant" : data.item_code_variant,
					"colour" : data.colour,
					"yard_atau_meter_per_roll" : data.yard_atau_meter_per_roll,
					"parent_item" : data.parent_item,
					"item_name" : data.item_name,
					"warehouse" : data.warehouse
				})
				mi.flags.ignore_permissions = 1
				mi.save()

			else :
				mi = frappe.new_doc("Group Item")
				mi.update({
					"group_code": data.group,
					"group_name": data.group,
					"is_active": 1		
				})
				
				item = frappe.get_doc("Item", data.parent_item)
				mi.append("data_group", {
					"doctype": "Data Group",
					"item_code_variant" : data.item_code_variant,
					"colour" : data.colour,
					"yard_atau_meter_per_roll" : data.yard_atau_meter_per_roll,
					"parent_item" : data.parent_item,
					"item_name" : data.item_name,
					"warehouse" : data.warehouse
				})

				mi.flags.ignore_permissions = 1
				mi.save()


@frappe.whitelist()
def cancel_packing_list_receipt(doc,method):
	pass
	# count = 0
	# for data in doc.packing_list_data :
	# 	if data.group :
	# 		frappe.db.sql ("""
	# 			DELETE FROM `tabData Group` dg
	# 			WHERE dg.`parent`= "{0}"
	# 			AND dg.`item_code_variant` = "{1}"
	# 			AND dg.`yard_per_roll` = "{2}" 
	# 			AND dg.`warehouse` = "{3}"
	# 			""".format(data.group, data.item_code_variant, data.yard_per_roll, data.warehouse))

	# 		frappe.db.commit()



@frappe.whitelist()
def submit_purchase_receipt(doc,method):
	if doc.packing_list_receipt and doc.purchase_order:
		frappe.db.sql ("""
			update 
			`tabPacking List Receipt` 
			set 
			is_used=1
			where 
			name="{0}"
			 """.format(doc.packing_list_receipt))

		frappe.db.commit()
		msgprint("Akan mengganti data di PO yang bersangkutan sesuai dengan Packing List Receipt (masih on progress)")

@frappe.whitelist()
def cancel_purchase_receipt(doc,method):
	if doc.packing_list_receipt and doc.purchase_order:
		frappe.db.sql ("""
			update 
			`tabPacking List Receipt` 
			set 
			is_used=0
			where 
			name="{0}"
			 """.format(doc.packing_list_receipt))

		frappe.db.commit()
		msgprint("Akan mengembalikan data PO seperti semua (masih on progress)")