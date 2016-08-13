# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InventoryLedger(Document):
	pass

@frappe.whitelist()
def submit_packing_list_receipt(doc,method):
	mi = frappe.new_doc("Inventory Ledger")
	mi.update({
		"doctype_type": "Packing List Receipt",
		"doctype_no": doc.name,
		"posting_date": doc.posting_date,
		"posting_time": doc.posting_time,
		"company": doc.company,
	})
	for i in doc.packing_list_data :
		mi.append("inventory_ledger_data", {
			"doctype": "Inventory Ledger Data",
			"item_code_variant" : i.item_code_variant,
			"item_parent" : i.parent_item,
			"item_name" : i.item_name,
			"inventory_uom" : i.inventory_uom,
			"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
			"qty_roll" : i.total_roll,
			"qty_yard_atau_meter" : i.total_yard_atau_meter,
			"warehouse" : i.warehouse,
			"colour" : i.colour
		})

	mi.flags.ignore_permissions = 1
	mi.save()


@frappe.whitelist()
def cancel_packing_list_receipt(doc,method):
	# for i in doc.items :
	frappe.db.sql ("""
		update 
		`tabInventory Ledger` 
		set 
		is_cancelled=1			
		where 
		doctype_no = "{}" 
		AND
		doctype_type="Packing List Receipt"
		""".format(doc.name))

	frappe.db.commit()



@frappe.whitelist()
def submit_packing_list_delivery(doc,method):
	mi = frappe.new_doc("Inventory Ledger")
	mi.update({
		"doctype_type": "Packing List Delivery",
		"doctype_no": doc.name,
		"posting_date": doc.posting_date,
		"posting_time": doc.posting_time,
		"company": doc.company,
	})
	for i in doc.packing_list_data :
		mi.append("inventory_ledger_data", {
			"doctype": "Inventory Ledger Data",
			"item_code_variant" : i.item_code_variant,
			"item_parent" : i.parent_item,
			"item_name" : i.item_name,
			"inventory_uom" : i.inventory_uom,
			"warehouse" : i.warehouse,
			"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
			"qty_roll" : i.total_roll,
			"qty_yard_atau_meter" : i.total_yard_atau_meter,
			"warehouse" : i.warehouse,
			"colour" : i.colour
		})

	mi.flags.ignore_permissions = 1
	mi.save()

@frappe.whitelist()
def cancel_packing_list_delivery(doc,method):
	# for i in doc.items :
	frappe.db.sql ("""
		update 
		`tabInventory Ledger` 
		set 
		is_cancelled=1			
		where 
		doctype_no = "{}" 
		AND
		doctype_type="Packing List Delivery"
		""".format(doc.name))

	frappe.db.commit()



# @frappe.whitelist()
# def submit_stock_entry(doc,method):
# 	mi = frappe.new_doc("Inventory Ledger")
# 	mi.update({
# 		"doctype_type": "Stock Entry",
# 		"doctype_no": doc.name,
# 		"posting_date": doc.posting_date,
# 		"posting_time": doc.posting_time,
# 		"company": doc.company,
# 		"purpose" : doc.purpose
# 	})
# 	if doc.purpose == "Material Receipt" :
# 		for i in doc.items :
# 			mi.append("inventory_ledger_data", {
# 				"doctype": "Inventory Ledger Data",
# 				"item_code_variant" : i.item_code,
# 				"item_parent" : i.parent_item,
# 				"item_name" : i.item_name,
# 				"stock_uom" : frappe.get_doc("Item",i.item_code).stock_uom,
# 				"warehouse" : i.t_warehouse,
# 				"yard_per_roll" : i.konversi_roll_ke_yard,
# 				"qty_roll" : (i.qty/i.konversi_roll_ke_yard),
# 				"qty_yard" : i.qty,
# 				"rate": i.basic_rate
# 			})

# 		mi.flags.ignore_permissions = 1
# 		mi.save()

# 	elif doc.purpose == "Material Issue" :
# 		for i in doc.items :
# 			mi.append("inventory_ledger_data", {
# 				"doctype": "Inventory Ledger Data",
# 				"item_code_variant" : i.item_code,
# 				"item_parent" : i.parent_item,
# 				"item_name" : i.item_name,
# 				"stock_uom" : frappe.get_doc("Item",i.item_code).stock_uom,
# 				"warehouse" : i.s_warehouse,
# 				"yard_per_roll" : i.konversi_roll_ke_yard,
# 				"qty_roll" : (i.qty/i.konversi_roll_ke_yard),
# 				"qty_yard" : i.qty,
# 				"rate": i.basic_rate
# 			})

# 		mi.flags.ignore_permissions = 1
# 		mi.save()

# @frappe.whitelist()
# def cancel_stock_entry(doc,method):
# 	# pass
# 	# for i in doc.items :
# 	frappe.db.sql ("""
# 		update 
# 		`tabInventory Ledger` 
# 		set 
# 		is_cancelled=1			
# 		where 
# 		doctype_no = "{}" 
# 		AND
# 		doctype_type="Stock Entry"
# 		""".format(doc.name))

# 	frappe.db.commit()