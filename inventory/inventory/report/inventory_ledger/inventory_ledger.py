# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["DocType:Data:100",
	"DocType No:Data:100",
	"Posting Date:Date:100",
	"Item Code Variant:Data:150",
	"UOM:Data:100",
	"Warehouse:Data:150",
	"Qty Yard / Meter:Float:100",
	"Yard / Meter per Roll:Float:100",
	"Qty Roll:Int:100",
	"Rate:Currency:100"]
	
	doctype_clause = ""
	date_clause = ""
	
	if filters.get("type") :
		doctype_clause = """ AND il.`doctype_type`="{0}" """.format(filters.get("type"))
	if filters.get("from_date") and filters.get("to_date") :
		date_clause = """ AND il.`posting_date` BETWEEN '{0}' AND '{1}' """.format(filters.get("from_date"),filters.get("to_date"))
	
	
	data = frappe.db.sql(""" SELECT il.`doctype_type`,il.`doctype_no`,il.`posting_date`,ild.`item_code_variant`,
		ild.`inventory_uom`,ild.`warehouse`,ild.`qty_yard_atau_meter`,ild.`yard_atau_meter_per_roll`,ild.`qty_roll`,ild.`rate` 
		FROM `tabInventory Ledger`il JOIN `tabInventory Ledger Data`ild
		WHERE il.`is_cancelled`=0 AND il.`name` = ild.`parent` {0} {1} """.format(doctype_clause,date_clause),as_list=1)
	
	return columns, data
