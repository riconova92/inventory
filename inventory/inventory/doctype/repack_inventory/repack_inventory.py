# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


form_grid_templates = {
	"repack_inventory_item": "templates/includes/repack_inventory.html"
}

class RepackInventory(Document):
	pass


@frappe.whitelist()
def save_repack_inventory(doc,method):

	if doc.total_roll > doc.available_qty :
		frappe.throw("Qty lebih besar daripada yang available di inventory")

	count = 0
	if doc.item_code :
		count = 0
	else :
		frappe.throw("Item Code belum diisi")

	if doc.colour :
		count = 0
	else :
		frappe.throw("Colour belum diisi")

	if doc.yard_atau_meter_per_roll :
		count = 0
	else :
		frappe.throw("Yard / Meter belum diisi")

	if doc.total_roll :
		count = 0
	else :
		frappe.throw("Total Roll belum diisi")

	if doc.group :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
			and di.`group` = "{}"
			and di.`total_roll` >= {}
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom, doc.group, doc.total_roll))
	else :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
			and di.`total_roll` >= {}
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom, doc.total_roll))


	if cek_data :
		count = 0
	else :
		frappe.throw("Itam "+str(doc.item_codedo.item_code)+" "+str(doc.colour)+" "+str(doc.yard_atau_meter_per_roll)+" "+str(item.stock_uom)+" tidak ada di dalam inventory")

	yard_total_from = doc.total_roll * doc.yard_atau_meter_per_roll


	if doc.repack_inventory_item :
		count = 0
	else :
		frappe.throw("Data Perubahannya belum diinputkan")

	yard_total_to = 0
	for i in doc.repack_inventory_item :
		yard_total_to = yard_total_to + (i.yard_atau_meter_per_roll * i.total_roll)


	if yard_total_from > yard_total_to or yard_total_from < yard_total_to :
		frappe.throw("Total Yard From dan Total Yard To tidak sama")

	# for i in doc.repack_inventory_item :
	# 	if i.status == "From" :
	# 		if i.group :
	# 			item = frappe.get_doc("Item", i.item_code_variant)
	# 			cek_data = frappe.db.sql("""
	# 				SELECT 
	# 				di.`item_code_variant`,
	# 				di.`total_roll`,
	# 				di.`total_yard_atau_meter`
	# 				FROM `tabData Inventory` di
	# 				WHERE di.`item_code_variant` = "{}"
	# 				and di.`yard_atau_meter_per_roll` = "{}"
	# 				and di.`warehouse` = "{}"
	# 				and di.`colour` = "{}"
	# 				and di.`inventory_uom` = "{}"
	# 				and di.`group` = "{}"
	# 			""".format(i.item_code_variant, i.yard_atau_meter_per_roll, item.default_warehouse, i.colour, item.stock_uom, i.group))
	# 		else :
	# 			item = frappe.get_doc("Item", i.item_code_variant)
	# 			cek_data = frappe.db.sql("""
	# 				SELECT 
	# 				di.`item_code_variant`,
	# 				di.`total_roll`,
	# 				di.`total_yard_atau_meter`
	# 				FROM `tabData Inventory` di
	# 				WHERE di.`item_code_variant` = "{}"
	# 				and di.`yard_atau_meter_per_roll` = "{}"
	# 				and di.`warehouse` = "{}"
	# 				and di.`colour` = "{}"
	# 				and di.`inventory_uom` = "{}"
	# 				and di.`group` is null
					
	# 			""".format(i.item_code_variant, i.yard_atau_meter_per_roll, item.default_warehouse, i.colour, item.stock_uom))

	# 		if cek_data :
	# 			count = 0
	# 		else :
	# 			frappe.throw("Itam "+str(i.item_code_variant)+" "+str(i.colour)+" "+str(i.yard_atau_meter_per_roll)+" "+str(item.stock_uom)+" tidak ada di dalam inventory")


@frappe.whitelist()
def submit_repack_inventory(doc,method):

	if doc.group :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
			and di.`group` = "{}"
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom, doc.group))

		if cek_data :
			current_total_roll = cek_data[0][1]
			current_total_yard = cek_data[0][2]

			new_total_roll = current_total_roll - doc.total_roll
			new_total_yard = current_total_yard - (doc.total_roll * doc.yard_atau_meter_per_roll)

			frappe.db.sql ("""
				UPDATE 
				`tabData Inventory` di
				SET 
				di.`total_roll`="{0}",
				di.`total_yard_atau_meter`="{1}"
				WHERE di.`item_code_variant`="{2}"
				AND di.`yard_atau_meter_per_roll`="{3}"
				AND di.`warehouse`="{4}"
				AND di.`colour` = "{5}"
				AND di.`group` = "{6}"
				AND di.`inventory_uom` = "{7}"

			""".format(new_total_roll, new_total_yard, doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))


		for i in doc.repack_inventory_item :
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
			""".format(doc.item_code, i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll + i.total_roll
				new_total_yard = current_total_yard + (i.total_roll * i.yard_atau_meter_per_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`group` = "{6}"
					AND di.`inventory_uom` = "{7}"

				""".format(new_total_roll,new_total_yard,doc.item_code,i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))

			else :
				mi = frappe.get_doc("Master Inventory", doc.item_code)
				mi.append("data_inventory", {
					"doctype": "Data Inventory",
					"item_code_variant" : doc.item_code,
					"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
					"total_roll" : i.total_roll,
					"total_yard_atau_meter" : (i.total_roll * i.yard_atau_meter_per_roll),
					"warehouse" : item.default_warehouse,
					"colour" : doc.colour,
					"group" : doc.group,
					"inventory_uom" : item.stock_uom
				})

				mi.flags.ignore_permissions = 1
				mi.save()

			# menambah item ke dalam group
			mi = frappe.get_doc("Group Item", doc.group)
			mi.append("data_group", {
				"doctype": "Data Group",
				"item_code_variant" : doc.item_code,
				"colour" : doc.colour,
				"yard_atau_meter" : i.yard_atau_meter_per_roll,
				"item_name" : item.item_name,
				"warehouse" : item.default_warehouse,
				"inventory_uom" : item.stock_uom,
				"total_qty_meter_atau_yard" : i.yard_atau_meter_per_roll * i.total_roll,
				"total_qty_roll" : i.total_roll
			})
			mi.flags.ignore_permissions = 1
			mi.save()

		# menghapus data dari group
		mi = frappe.get_doc("Group Item", doc.group)
		for d in mi.get("data_group") :
			if d.item_code_variant == doc.item_code and d.colour == doc.colour and d.yard_atau_meter == doc.yard_atau_meter_per_roll :
				mi.remove(d)
		mi.flags.ignore_permissions = 1
		mi.save()

	# else tanpa group
	else :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom))

		if cek_data :
			current_total_roll = cek_data[0][1]
			current_total_yard = cek_data[0][2]

			new_total_roll = current_total_roll - doc.total_roll
			new_total_yard = current_total_yard - (doc.total_roll * doc.yard_atau_meter_per_roll)

			frappe.db.sql ("""
				UPDATE 
				`tabData Inventory` di
				SET 
				di.`total_roll`="{0}",
				di.`total_yard_atau_meter`="{1}"
				WHERE di.`item_code_variant`="{2}"
				AND di.`yard_atau_meter_per_roll`="{3}"
				AND di.`warehouse`="{4}"
				AND di.`colour` = "{5}"
				AND di.`inventory_uom` = "{6}"

			""".format(new_total_roll, new_total_yard, doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))


		for i in doc.repack_inventory_item :
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
				and di.`inventory_uom` = "{}"
			""".format(doc.item_code, i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll + i.total_roll
				new_total_yard = current_total_yard + (i.total_roll * i.yard_atau_meter_per_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`inventory_uom` = "{6}"

				""".format(new_total_roll,new_total_yard,doc.item_code,i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))

			else :
				mi = frappe.get_doc("Master Inventory", doc.item_code)
				mi.append("data_inventory", {
					"doctype": "Data Inventory",
					"item_code_variant" : doc.item_code,
					"yard_atau_meter_per_roll" : i.yard_atau_meter_per_roll,
					"total_roll" : i.total_roll,
					"total_yard_atau_meter" : (i.total_roll * i.yard_atau_meter_per_roll),
					"warehouse" : item.default_warehouse,
					"colour" : doc.colour,
					"inventory_uom" : item.stock_uom
				})

				mi.flags.ignore_permissions = 1
				mi.save()


@frappe.whitelist()
def cancel_repack_inventory(doc,method):
	if doc.group :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
			and di.`group` = "{}"
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom, doc.group))

		if cek_data :
			current_total_roll = cek_data[0][1]
			current_total_yard = cek_data[0][2]

			new_total_roll = current_total_roll + doc.total_roll
			new_total_yard = current_total_yard + (doc.total_roll * doc.yard_atau_meter_per_roll)

			frappe.db.sql ("""
				UPDATE 
				`tabData Inventory` di
				SET 
				di.`total_roll`="{0}",
				di.`total_yard_atau_meter`="{1}"
				WHERE di.`item_code_variant`="{2}"
				AND di.`yard_atau_meter_per_roll`="{3}"
				AND di.`warehouse`="{4}"
				AND di.`colour` = "{5}"
				AND di.`group` = "{6}"
				AND di.`inventory_uom` = "{7}"

			""".format(new_total_roll, new_total_yard, doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))


		for i in doc.repack_inventory_item :
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
			""".format(doc.item_code, i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll - i.total_roll
				new_total_yard = current_total_yard - (i.total_roll * i.yard_atau_meter_per_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`group` = "{6}"
					AND di.`inventory_uom` = "{7}"

				""".format(new_total_roll,new_total_yard,doc.item_code,i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, doc.group, item.stock_uom))


			# menambah item ke dalam group
			mi = frappe.get_doc("Group Item", doc.group)
			for d in mi.get("data_group") :
				if d.item_code_variant == doc.item_code and d.colour == doc.colour and d.yard_atau_meter == i.yard_atau_meter_per_roll :
					mi.remove(d)
			mi.flags.ignore_permissions = 1
			mi.save()



		# menghapus data dari group
		mi = frappe.get_doc("Group Item", doc.group)
		mi.append("data_group", {
			"doctype": "Data Group",
			"item_code_variant" : doc.item_code,
			"colour" : doc.colour,
			"yard_atau_meter" : doc.yard_atau_meter_per_roll,
			"item_name" : item.item_name,
			"warehouse" : item.default_warehouse,
			"inventory_uom" : item.stock_uom,
			"total_qty_meter_atau_yard" : doc.yard_atau_meter_per_roll * doc.total_roll,
			"total_qty_roll" : doc.total_roll
		})
		mi.flags.ignore_permissions = 1
		mi.save()


	# else tanpa group
	else :
		item = frappe.get_doc("Item", doc.item_code)
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
			and di.`inventory_uom` = "{}"
		""".format(doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour, item.stock_uom))

		if cek_data :
			current_total_roll = cek_data[0][1]
			current_total_yard = cek_data[0][2]

			new_total_roll = current_total_roll + doc.total_roll
			new_total_yard = current_total_yard + (doc.total_roll * doc.yard_atau_meter_per_roll)

			frappe.db.sql ("""
				UPDATE 
				`tabData Inventory` di
				SET 
				di.`total_roll`="{0}",
				di.`total_yard_atau_meter`="{1}"
				WHERE di.`item_code_variant`="{2}"
				AND di.`yard_atau_meter_per_roll`="{3}"
				AND di.`warehouse`="{4}"
				AND di.`colour` = "{5}"
				AND di.`inventory_uom` = "{6}"

			""".format(new_total_roll, new_total_yard, doc.item_code, doc.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))


		for i in doc.repack_inventory_item :
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
				and di.`inventory_uom` = "{}"
			""".format(doc.item_code, i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))

			if cek_data :
				current_total_roll = cek_data[0][1]
				current_total_yard = cek_data[0][2]

				new_total_roll = current_total_roll - i.total_roll
				new_total_yard = current_total_yard - (i.total_roll * i.yard_atau_meter_per_roll)

				frappe.db.sql ("""
					UPDATE 
					`tabData Inventory` di
					SET 
					di.`total_roll`="{0}",
					di.`total_yard_atau_meter`="{1}"
					WHERE di.`item_code_variant`="{2}"
					AND di.`yard_atau_meter_per_roll`="{3}"
					AND di.`warehouse`="{4}"
					AND di.`colour` = "{5}"
					AND di.`inventory_uom` = "{6}"

				""".format(new_total_roll,new_total_yard,doc.item_code,i.yard_atau_meter_per_roll, item.default_warehouse, doc.colour,  item.stock_uom))