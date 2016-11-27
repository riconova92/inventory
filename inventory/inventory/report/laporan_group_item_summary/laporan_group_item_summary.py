# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []

	columns = [
		"Item Code:Data:400",
		"Group Code:Data:100",
		"Keterangan Group:Data:200",
		"Status Group:Data:200"]

	item_clause = ""
	if filters.get("item"):
		item_clause = """ AND gi.`name` LIKE "{0}" """.format(filters.get("item")+"%")
	
	negative_clause = ""
	if filters.get("show_complete_group"):
		negative_clause = """ AND gi.`status_group` = "Complete Used" """
	else :
		negative_clause = """ AND gi.`status_group` != "Complete Used" """


	data = frappe.db.sql("""
		SELECT
		SUBSTRING_INDEX(gi.`name`, '.',1) AS item_code,
		SUBSTRING_INDEX(gi.`name`, '.',-1) AS group_code,
		gi.`keterangan_group`,
		gi.`status_group`
		FROM `tabGroup Item` gi
		WHERE gi.`is_active` = 1
		{}
		{}
		ORDER BY gi.`name`
		""".format(item_clause, negative_clause),as_list=1)




	return columns, data
