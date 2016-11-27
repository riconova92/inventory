# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = [
		"Group Code:Data:100",
		"Item Code:Data:400",
		"Colour:Data:200",
		"UOM:Data:200",
		"Yard / Meter:Data:200",
		"Qty:Data:200",
		"Is Used ?:Data:200"
		]

	item_clause = ""
	if filters.get("item"):
		item_clause = """ AND gi.`name` LIKE "{0}" """.format(filters.get("item")+"%")
	
	# negative_clause = ""
	# if filters.get("show_complete_group"):
	# 	negative_clause = """ AND gi.`status_group` = "Complete Used" """
	# else :
	# 	negative_clause = """ AND gi.`status_group` != "Complete Used" """


	data = frappe.db.sql("""
		SELECT
		SUBSTRING_INDEX(gi.`name`, '.',-1) AS group_code,
		SUBSTRING_INDEX(gi.`name`, '.',1) AS item_code,
		
		
		dg.`colour`,
		dg.`inventory_uom`,
		dg.`yard_atau_meter`,
		dg.`total_qty_roll`,
		CASE dg.`is_used`
		WHEN 0 THEN "Not Used"
		WHEN 1 THEN "Used"
		END AS is_used

		FROM `tabGroup Item` gi
		JOIN `tabData Group` dg
		ON gi.`name` = dg.`parent`
		WHERE gi.`is_active` = 1
		{}
		""".format(item_clause),as_list=1)


	return columns, data
