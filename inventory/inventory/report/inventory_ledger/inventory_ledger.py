# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Item Code:Link/Item:100","Colour:Link/Colour:100","Yard/Meter:Float:100","Group:Data:100",
		"In Qty:Float:100","Out Qty:Float:100","Document:Link/DocType:100","Document No:Dynamic Link/Document:100"]
	
	item_clause = ""
	if filters.get("item") :
		item_clause = """ AND j.`item_code_variant` = "{0}" """.format(filters.get("item"))
	
	document_no_clause = ""
	if filters.get("document_no") :
		document_no_clause = """ AND i.`name`="{0}" """.format(filters.get("document_no"))
	data = []
	if not filters.get("document") :
		new_data = frappe.db.sql(""" 
			SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll`,0,
				"Packing List Receipt",i.`name` FROM `tabPacking List Receipt`i JOIN `tabPacking List Receipt Data`j ON i.`name`=j.`parent`
				WHERE i.`docstatus`=1
				{0} {1}
				ORDER BY j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`
				""".format(document_no_clause,item_clause),as_list=1)
		data = data + new_data		
		
		new_data = frappe.db.sql(""" 
			SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0,j.`total_roll`,
				"Packing List Receipt",i.`name` FROM `tabPacking List Delivery`i JOIN `tabPacking List Delivery Data`j ON i.`name`=j.`parent`
				WHERE i.`docstatus`=1
				{0} {1}
				ORDER BY j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`
			""".format(document_no_clause,item_clause),as_list=1)
		data = data + new_data
		
		new_data = frappe.db.sql("""
			SELECT * FROM 
				(
				SELECT j.`item_code_roll`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll` AS `in_qty`, 0 AS `out_qty`,"Stock Recon Inventory" AS `document`,i.`name` 
				FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 {0} {1}
				
				UNION ALL 
				
				SELECT j.`item_code_roll`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0 AS `in_qty`, j.`total_roll` AS `out_qty`,"Stock Recon Inventory" AS `document`,i.`name` 
				FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Item Out`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 {0} {1}
				)d 
				ORDER BY d.`item_code_roll`,d.`colour`,d.`yard_atau_meter_per_roll`,d.`group`
			""".format(document_no_clause,item_clause),as_list=1)
		data = data + new_data
		
		new_data = frappe.db.sql("""
			SELECT * FROM
				(
				SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll` AS `in_qty`,0 AS `out_qty`,"Repack Inventory",i.`name` 
				FROM `tabRepack Inventory`i JOIN `tabRepack Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 AND j.`status`="To" {0} {1}

				UNION ALL
				
				SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0 AS `in_qty`,j.`total_roll` AS `out_qty`,"Repack Inventory",i.`name` 
				FROM `tabRepack Inventory`i JOIN `tabRepack Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 AND j.`status`="From" {0} {1}
				)d
				
				ORDER BY d.`item_code_variant`,d.`colour`,d.`yard_atau_meter_per_roll`,d.`group`

			""".format(document_no_clause,item_clause),as_list=1)
		data = data + new_data
		
	elif filters.get("document") == "Packing List Receipt" :
		data = frappe.db.sql(""" 
			SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll`,0,
				"Packing List Receipt",i.`name` FROM `tabPacking List Receipt`i JOIN `tabPacking List Receipt Data`j ON i.`name`=j.`parent`
				WHERE i.`docstatus`=1
				{0} {1}
				ORDER BY j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`
				""".format(document_no_clause,item_clause),as_list=1)
	elif filters.get("document") == "Packing List Delivery" :
		data = frappe.db.sql(""" 
			SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0,j.`total_roll`,
				"Packing List Receipt",i.`name` FROM `tabPacking List Delivery`i JOIN `tabPacking List Delivery Data`j ON i.`name`=j.`parent`
				WHERE i.`docstatus`=1
				{0} {1}
				ORDER BY j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`
			""".format(document_no_clause,item_clause),as_list=1)
	elif filters.get("document") == "Stock Recon Inventory" :
		data = frappe.db.sql("""
			SELECT * FROM 
				(
				SELECT j.`item_code_roll`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll` AS `in_qty`, 0 AS `out_qty`,"Stock Recon Inventory" AS `document`,i.`name` 
				FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 {0} {1}
				
				UNION ALL 
				
				SELECT j.`item_code_roll`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0 AS `in_qty`, j.`total_roll` AS `out_qty`,"Stock Recon Inventory" AS `document`,i.`name` 
				FROM `tabStock Recon Inventory`i JOIN `tabStock Recon Inventory Item Out`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 {0} {1}
				)d 
				ORDER BY d.`item_code_roll`,d.`colour`,d.`yard_atau_meter_per_roll`,d.`group`
			""".format(document_no_clause,item_clause),as_list=1)
	elif filters.get("document") == "Repack Inventory" :
		data = frappe.db.sql("""
			SELECT * FROM
				(
				SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,j.`total_roll` AS `in_qty`,0 AS `out_qty`,"Repack Inventory",i.`name` 
				FROM `tabRepack Inventory`i JOIN `tabRepack Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 AND j.`status`="To" {0} {1}

				UNION ALL
				
				SELECT j.`item_code_variant`,j.`colour`,j.`yard_atau_meter_per_roll`,j.`group`,0 AS `in_qty`,j.`total_roll` AS `out_qty`,"Repack Inventory",i.`name` 
				FROM `tabRepack Inventory`i JOIN `tabRepack Inventory Item`j ON i.`name`=j.`parent` WHERE i.`docstatus`=1 AND j.`status`="From" {0} {1}
				)d
				
				ORDER BY d.`item_code_variant`,d.`colour`,d.`yard_atau_meter_per_roll`,d.`group`

			""".format(document_no_clause,item_clause),as_list=1)
	
	return columns, data
