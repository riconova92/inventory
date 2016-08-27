# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class custom_method(Document):
	pass

@frappe.whitelist()
def divide_group(item_code_variant):
	
	group = item_code_variant.split(" ")[0]

	return group


@frappe.whitelist()
def projected_stock(item_code):

	qty_pending_order = 0
	qty_inventory = 0

	uom = frappe.get_doc("Item",item_code).stock_uom

	get_qty_pending_order = frappe.db.sql("""
		SELECT
		SUM(por.`roll_qty` - por.`delivered_qty`)
		FROM `tabPending Order` po
		JOIN `tabPending Order Roll` por
		ON po.`name` = por.`parent`
		WHERE po.`docstatus` < 2
		AND por.`docstatus` < 2
		AND (por.`roll_qty` - por.`delivered_qty`) > 0
		AND por.`item_code_roll` = "{}"
		""".format(item_code))

	get_qty_inventory = frappe.db.sql("""
		SELECT
		SUM(di.`total_roll`)
		FROM `tabData Inventory` di
		WHERE di.`item_code_variant` = "{}"
		""".format(item_code))

	if get_qty_pending_order :
		qty_pending_order = get_qty_pending_order[0][0]
	else :
		qty_pending_order = 0

	if get_qty_inventory :
		qty_inventory = get_qty_inventory[0][0]
	else :
		qty_inventory = 0

	projected_stock = int(qty_inventory) - int(qty_pending_order)
	

	return projected_stock