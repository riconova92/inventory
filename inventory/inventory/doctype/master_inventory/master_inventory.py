# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MasterInventory(Document):
	pass

# @frappe.whitelist()
# def submit_purchase_receipt(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard + i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					frappe.db.commit()

# 				else :
# 					temp_colour = frappe.db.sql("""
# 					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 					WHERE iva.`parent` = "{}"
# 					""".format(i.item_code))

# 					colour = temp_colour[0][1]
# 					mi = frappe.get_doc("Master Inventory", i.parent_item)
# 					mi.append("data_inventory", {
# 						"doctype": "Data Inventory",
# 						"item_code_variant" : i.item_code,
# 						"colour" : colour,
# 						"warehouse" : i.warehouse,
# 						"yard_per_roll" : i.yard_per_roll,
# 						"total_roll" : (i.qty/i.yard_per_roll),
# 						"total_yard" : i.qty
# 					})

# 					mi.flags.ignore_permissions = 1
# 					mi.save()

# 			else :
# 				item = frappe.get_doc("Item", i.parent_item)
# 				mi = frappe.new_doc("Master Inventory")
# 				mi.update({
# 					"item_code": item.item_code,
# 					"item_name": item.item_name,
# 					"design": item.design		
# 				})

# 				temp_colour = frappe.db.sql("""
# 					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
# 					WHERE iva.`parent` = "{}"
# 					""".format(i.item_code))

# 				colour = temp_colour[0][1]
# 				mi.append("data_inventory", {
# 					"doctype": "Data Inventory",
# 					"item_code_variant" : i.item_code,
# 					"colour" : colour,
# 					"warehouse" : i.warehouse,
# 					"yard_per_roll" : i.yard_per_roll,
# 					"total_roll" : (i.qty/i.yard_per_roll),
# 					"total_yard" : i.qty
# 				})

# 				mi.flags.ignore_permissions = 1
# 				mi.save()

# @frappe.whitelist()
# def cancel_purchase_receipt(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard - i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					frappe.db.commit()


# @frappe.whitelist()
# def submit_delivery_note(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard - i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					frappe.db.commit()


# @frappe.whitelist()
# def cancel_delivery_note(doc,method):
# 	for i in doc.items :
# 		if i.parent_item :
# 			cek_inventory = frappe.db.sql("""
# 				SELECT
# 				mi.`item_code`
# 				FROM `tabMaster Inventory` mi
# 				WHERE mi.`item_code` = "{}"
# 				""".format(i.parent_item))

# 			if cek_inventory :
# 				cek_data = frappe.db.sql("""
# 					SELECT 
# 					di.`item_code_variant`,
# 					di.`total_roll`,
# 					di.`total_yard`
# 					FROM `tabData Inventory` di
# 					WHERE di.`parent` = "{}"
# 					AND di.`item_code_variant` = "{}"
# 					and di.`yard_per_roll` = "{}"
# 				""".format(i.parent_item, i.item_code, i.yard_per_roll))

# 				if cek_data :
# 					current_total_roll = cek_data[0][1]
# 					current_total_yard = cek_data[0][2]

# 					new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
# 					new_total_yard = current_total_yard + i.qty

# 					frappe.db.sql ("""
# 						update 
# 						`tabData Inventory` 
# 						set 
# 						total_roll="{0}",
# 						total_yard="{1}"
# 						where 
# 						parent="{2}"
# 						AND
# 						item_code_variant="{3}"
# 						AND
# 						yard_per_roll="{4}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll))

# 					frappe.db.commit()




@frappe.whitelist()
def submit_packing_list_receipt(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`,
					di.`total_roll`,
					di.`total_yard_atau_meter`
					FROM `tabData Inventory` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`warehouse` = "{}"
					and di.`colour` = "{}"
					and di.`group` = "{}"
					and di.`inventory_uom` = "{}"
				""".format(i.item_code_variant, i.yard_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll + i.total_roll
					new_total_yard = current_total_yard + i.total_yard_atau_meter

					frappe.db.sql ("""
						update 
						`tabData Inventory` 
						set 
						total_roll="{0}",
						total_yard_atau_meter="{1}"
						where 
						item_code_variant="{2}"
						AND
						yard_per_roll="{3}"
						and warehouse="{4}"
						and colour = "{5}"
						and group = "{6}"
						and di.`inventory_uom` = "{7}"

						 """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

					frappe.db.commit()

				else :
					
					mi = frappe.get_doc("Master Inventory", i.item_code_variant)
					mi.append("data_inventory", {
						"doctype": "Data Inventory",
						"item_code_variant" : i.item_code_variant,
						"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
						"total_roll" : i.total_roll,
						"total_yard_atau_meter" : i.total_yard_atau_meter,
						"warehouse" : i.warehouse,
						"colour" : i.colour,
						"group" : i.group,
						"inventory_uom" : i.inventory_uom
					})

					mi.flags.ignore_permissions = 1
					mi.save()

			else :
				item = frappe.get_doc("Item", i.item_code_variant)
				mi = frappe.new_doc("Master Inventory")
				mi.update({
					"item_code": item.item_code,
					"item_name": item.item_name	
				})

				
				mi.append("data_inventory", {
					"doctype": "Data Inventory",
					"item_code_variant" : i.item_code_variant,
					"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
					"total_roll" : i.total_roll,
					"total_yard_atau_meter" : i.total_yard_atau_meter,
					"warehouse" : i.warehouse,
					"colour" : i.colour,
					"group" : i.group,
					"inventory_uom" : i.inventory_uom
				})

				mi.flags.ignore_permissions = 1
				mi.save()

@frappe.whitelist()
def cancel_packing_list_receipt(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`,
					di.`total_roll`,
					di.`total_yard_atau_meter`
					FROM `tabData Inventory` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`warehouse` = "{}"
					and di.`colour` = "{}"
					and di.`group` = "{}"
					and di.`inventory_uom` = "{}"
				""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - i.total_roll
					new_total_yard = current_total_yard - i.total_yard_atau_meter

					frappe.db.sql ("""
						update 
						`tabData Inventory` 
						set 
						total_roll="{0}",
						total_yard_atau_meter="{1}"
						where 
						item_code_variant="{2}"
						AND
						yard_atau_meter_per_roll="{3}"
						and warehouse = "{4}"
						and colour = "{5}"
						and group = "{6}"
						and inventory_uom = "{7}" """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

					frappe.db.commit()


@frappe.whitelist()
def submit_packing_list_delivery(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`,
					di.`total_roll`,
					di.`total_yard_atau_meter`
					FROM `tabData Inventory` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`warehouse` = "{}"
					and di.`colour` = "{}"
					and di.`group` = "{}"
					and di.`inventory_uom` = "{}"
				""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll - i.total_roll
					new_total_yard = current_total_yard - i.total_yard_atau_meter

					frappe.db.sql ("""
						update 
						`tabData Inventory` 
						set 
						total_roll="{0}",
						total_yard_atau_meter="{1}"
						where 
						item_code_variant="{2}"
						AND
						yard_atau_meter_per_roll="{3}"
						and warehouse = "{4}"
						and colour = "{5}"
						and group = "{6}"
						and inventory_uom = "{7}" """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

					frappe.db.commit()


@frappe.whitelist()
def cancel_packing_list_delivery(doc,method):
	for i in doc.packing_list_data :
		if i.item_code_variant :
			cek_inventory = frappe.db.sql("""
				SELECT
				mi.`item_code`
				FROM `tabMaster Inventory` mi
				WHERE mi.`item_code` = "{}"
				""".format(i.item_code_variant))

			if cek_inventory :
				cek_data = frappe.db.sql("""
					SELECT 
					di.`item_code_variant`,
					di.`total_roll`,
					di.`total_yard_atau_meter`
					FROM `tabData Inventory` di
					WHERE di.`item_code_variant` = "{}"
					and di.`yard_atau_meter_per_roll` = "{}"
					and di.`warehouse` = "{}"
					and di.`colour` = "{}"
					and di.`group` = "{}"
					and di.`inventory_uom` = "{}"
				""".format(i.item_code_variant, i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

				if cek_data :
					current_total_roll = cek_data[0][1]
					current_total_yard = cek_data[0][2]

					new_total_roll = current_total_roll + i.total_roll
					new_total_yard = current_total_yard + i.total_yard_atau_meter

					frappe.db.sql ("""
						update 
						`tabData Inventory` 
						set 
						total_roll="{0}",
						total_yard_atau_meter="{1}"
						where 
						item_code_variant="{2}"
						AND
						yard_atau_meter_per_roll="{3}"
						and warehouse = "{4}"
						and colour = "{5}"
						and group = "{6}"
						and inventory_uom = "{7}" """.format(new_total_roll,new_total_yard,i.item_code_variant,i.yard_atau_meter_per_roll, i.warehouse, i.colour, i.group, i.inventory_uom))

					frappe.db.commit()




@frappe.whitelist()
def submit_stock_entry(doc,method):
	if doc.purpose == "Material Receipt" :
		for i in doc.items :
			if i.parent_item :
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(i.parent_item))

				if cek_inventory :
					cek_data = frappe.db.sql("""
						SELECT 
						di.`item_code_variant`,
						di.`total_roll`,
						di.`total_yard`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`item_code_variant` = "{}"
						and di.`yard_per_roll` = "{}"
						and di.`warehouse` = "{}"
					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.t_warehouse))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
						new_total_yard = current_total_yard + i.qty

						frappe.db.sql ("""
							update 
							`tabData Inventory` 
							set 
							total_roll="{0}",
							total_yard="{1}"
							where 
							parent="{2}"
							AND
							item_code_variant="{3}"
							AND
							yard_per_roll="{4}"
							and
							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.t_warehouse))

						frappe.db.commit()

					else :
						temp_colour = frappe.db.sql("""
						SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
						WHERE iva.`parent` = "{}"
						""".format(i.item_code))

						colour = temp_colour[0][1]
						mi = frappe.get_doc("Master Inventory", i.parent_item)
						mi.append("data_inventory", {
							"doctype": "Data Inventory",
							"item_code_variant" : i.item_code,
							"colour" : colour,
							"warehouse" : i.t_warehouse,
							"yard_per_roll" : i.yard_per_roll,
							"total_roll" : (i.qty/i.yard_per_roll),
							"total_yard" : i.qty,

						})

						mi.flags.ignore_permissions = 1
						mi.save()

				else :
					item = frappe.get_doc("Item", i.parent_item)
					mi = frappe.new_doc("Master Inventory")
					mi.update({
						"item_code": item.item_code,
						"item_name": item.item_name,
						"design": item.design		
					})

					temp_colour = frappe.db.sql("""
					SELECT iva.`parent`, iva.`attribute_value` FROM `tabItem Variant Attribute` iva
					WHERE iva.`parent` = "{}"
					""".format(i.item_code))

					colour = temp_colour[0][1]
					mi.append("data_inventory", {
						"doctype": "Data Inventory",
						"item_code_variant" : i.item_code,
						"colour" : colour,
						"warehouse" : i.t_warehouse,
						"yard_per_roll" : i.yard_per_roll,
						"total_roll" : (i.qty/i.yard_per_roll),
						"total_yard" : i.qty
					})

					mi.flags.ignore_permissions = 1
					mi.save()


	elif doc.purpose == "Material Issue" :
		for i in doc.items :
			if i.parent_item :
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(i.parent_item))

				if cek_inventory :
					cek_data = frappe.db.sql("""
						SELECT 
						di.`item_code_variant`,
						di.`total_roll`,
						di.`total_yard`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`item_code_variant` = "{}"
						and di.`yard_per_roll` = "{}"
						and di.`warehouse` = "{}"
					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.s_warehouse))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
						new_total_yard = current_total_yard - i.qty

						frappe.db.sql ("""
							update 
							`tabData Inventory` 
							set 
							total_roll="{0}",
							total_yard="{1}"
							where 
							parent="{2}"
							AND
							item_code_variant="{3}"
							AND
							yard_per_roll="{4}"
							and
							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.s_warehouse))

						frappe.db.commit()


@frappe.whitelist()
def cancel_stock_entry(doc,method):
	if doc.purpose == "Material Receipt" :
		for i in doc.items :
			if i.parent_item :
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(i.parent_item))

				if cek_inventory :
					cek_data = frappe.db.sql("""
						SELECT 
						di.`item_code_variant`,
						di.`total_roll`,
						di.`total_yard`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`item_code_variant` = "{}"
						and di.`yard_per_roll` = "{}"
						and di.`warehouse = "{}"
					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.t_warehouse))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll - (i.qty / i.yard_per_roll)
						new_total_yard = current_total_yard - i.qty

						frappe.db.sql ("""
							update 
							`tabData Inventory` 
							set 
							total_roll="{0}",
							total_yard="{1}"
							where 
							parent="{2}"
							AND
							item_code_variant="{3}"
							AND
							yard_per_roll="{4}"
							and
							warehouse="{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.t_warehouse))

						frappe.db.commit()


	elif doc.purpose == "Material Issue" :
		for i in doc.items :
			if i.parent_item :
				cek_inventory = frappe.db.sql("""
					SELECT
					mi.`item_code`
					FROM `tabMaster Inventory` mi
					WHERE mi.`item_code` = "{}"
					""".format(i.parent_item))

				if cek_inventory :
					cek_data = frappe.db.sql("""
						SELECT 
						di.`item_code_variant`,
						di.`total_roll`,
						di.`total_yard`
						FROM `tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`item_code_variant` = "{}"
						and di.`yard_per_roll` = "{}"
						and di.`warehouse` = "{}"
					""".format(i.parent_item, i.item_code, i.yard_per_roll, i.s_warehouse))

					if cek_data :
						current_total_roll = cek_data[0][1]
						current_total_yard = cek_data[0][2]

						new_total_roll = current_total_roll + (i.qty / i.yard_per_roll)
						new_total_yard = current_total_yard + i.qty

						frappe.db.sql ("""
							update 
							`tabData Inventory` 
							set 
							total_roll="{0}",
							total_yard="{1}"
							where 
							parent="{2}"
							AND
							item_code_variant="{3}"
							AND
							yard_per_roll="{4}"
							and warehouse = "{5}" """.format(new_total_roll,new_total_yard,i.parent_item,i.item_code,i.yard_per_roll, i.s_warehouse))

						frappe.db.commit()