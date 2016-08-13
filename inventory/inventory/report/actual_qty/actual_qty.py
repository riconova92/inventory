# Copyright (c) 2013, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	
	columns = ["Item Code:Link/Master Inventory:100",
	"Item Name:Data:200",
	"UOM:Data:150",
	"Colour:Data:100",
	"Yard / Meter per Roll:Float:100",
	"Total Roll:Float:100",
	"Total Yard / Meter:Float:100"]
	
	data = frappe.db.sql(""" SELECT 
		mi.`name`,
		mi.`item_name`,
		di.`inventory_uom`,
		di.`colour`,
		di.`yard_atau_meter_per_roll`,
		di.`total_roll`,
		di.`total_yard_atau_meter` 
		FROM `tabMaster Inventory`mi 
		JOIN `tabData Inventory`di 
		WHERE mi.`name`=di.`parent` 
		AND di.`total_roll`>0 
		AND di.`total_yard_atau_meter`>0 """.format(),as_list=1)
	
	return columns, data
