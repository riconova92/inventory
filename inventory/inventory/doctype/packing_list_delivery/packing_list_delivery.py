# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PackingListDelivery(Document):
	def add_item(self):
		count = 0


		if self.item_code_variant and self.yard_atau_meter :
			parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
			item_name = frappe.get_doc("Item", self.item_code_variant).item_name
			if self.packing_list_data :
				for i in self.packing_list_data :
					if i.item_code_variant == self.item_code_variant and i.yard_per_roll == self.yard_atau_meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour :
						count = 1

				if count == 1 :
					for i in self.packing_list_data :
						if i.item_code_variant == self.item_code_variant and i.yard_per_roll == self.yard_atau_meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour  :
							new_total_yard = i.total_yard
							new_total_roll = i.total_roll
							i.total_roll = new_total_roll + 1
							i.total_yard = new_total_yard + self.yard_atau_meter
				
				else :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant
					pp_so.yard_per_roll = self.yard_atau_meter
					pp_so.total_yard = self.yard_atau_meter
					pp_so.total_roll = 1
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					

			else :
				pp_so = self.append('packing_list_data', {})
				pp_so.item_code_variant = self.item_code_variant
				pp_so.yard_per_roll = self.yard_atau_meter
				pp_so.total_yard = self.yard_atau_meter
				pp_so.total_roll = 1
				pp_so.parent_item = parent_item
				pp_so.item_name = item_name
				pp_so.warehouse = self.warehouse
				pp_so.colour = self.colour
				

		elif self.item_code_variant and self.meter :
			parent_item = frappe.get_doc("Item", self.item_code_variant).variant_of
			item_name = frappe.get_doc("Item", self.item_code_variant).item_name
			if self.packing_list_data :
				for i in self.packing_list_data :
					if i.item_code_variant == self.item_code_variant and i.meter_per_roll == self.meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour :
						count = 1

				if count == 1 :
					for i in self.packing_list_data :
						if i.item_code_variant == self.item_code_variant and i.meter_per_roll == self.meter and i.group == "" and i.warehouse == self.warehouse and i.colour == self.colour  :
							new_total_meter = i.total_meter
							new_total_roll = i.total_roll
							i.total_roll = new_total_roll + 1
							i.total_meter = new_total_meter + self.meter
				else :
					pp_so = self.append('packing_list_data', {})
					pp_so.item_code_variant = self.item_code_variant
					pp_so.meter_per_roll = self.meter
					pp_so.total_meter = self.meter
					pp_so.total_roll = 1
					pp_so.parent_item = parent_item
					pp_so.item_name = item_name
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					

			else :
				pp_so = self.append('packing_list_data', {})
				pp_so.item_code_variant = self.item_code_variant
				pp_so.meter_per_roll = self.meter
				pp_so.total_meter = self.meter
				pp_so.total_roll = 1
				pp_so.parent_item = parent_item
				pp_so.item_name = item_name
				pp_so.warehouse = self.warehouse
				pp_so.colour = self.colour
				

		else :
			frappe.throw("Item Code / Yard tidak terisi")




	def get_item(self):
		if self.group_item :
			get_data_group = frappe.db.sql("""
				SELECT
				gi.`group_code`,
				dg.`item_code_variant`,
				dg.`yard_per_roll`,
				dg.`item_name`,
				dg.`parent_item`,
				dg.`warehouse`,
				dg.`colour`,
				dg.`design`
				FROM `tabGroup Item` gi
				JOIN `tabData Group` dg
				ON gi.`name` = dg.`parent`
				WHERE gi.`is_active` = 1
				AND gi.`group_code` = "{}"
			""".format(self.group_item))

			if get_data_group :
				for dg in get_data_group :
					cek_inventory = frappe.db.sql("""
						SELECT
						di.`parent`,
						di.`item_code_variant`,
						di.`yard_per_roll`,
						di.`warehouse`,
						di.`total_roll`,
						di.`total_yard`
						FROM
						`tabData Inventory` di
						WHERE di.`parent` = "{}"
						AND di.`item_code_variant` = "{}"
						AND di.`warehouse` = "{}"
						AND di.`yard_per_roll` = "{}"
						and di.`colour` = "{}"
						and di.`design` = "{}"
					""".format(dg[4], dg[1], dg[5], dg[2], dg[6], dg[7]))

					if cek_inventory[0][4] <= 0 or cek_inventory[0][5] <= 0 :
						frappe.throw("Group "+self.group_item+" tidak dapat dijual sebagai group karena item "+dg[1]+" tidak memiliki stock (stocknya 0) \n Gunakan Add Item biasa untuk menjual bukan sebagai grup")


			if get_data_group :
				for dg in get_data_group :
					count = 0
					if self.packing_list_data :
						for i in self.packing_list_data :
							if i.item_code_variant == dg[1] and i.yard_per_roll == dg[2] and i.group == dg[0] and i.warehouse == dg[5] and i.colour == dg[6] and i.design == dg[7] :
								count = 1

						if count == 1 :
							for i in self.packing_list_data :
								if i.item_code_variant == dg[1] and i.yard_per_roll == dg[2] and i.group == dg[0] and i.warehouse == dg[5]  and i.colour == dg[6] and i.design == dg[7] :
									new_total_yard = i.total_yard
									new_total_roll = i.total_roll
									i.total_roll = new_total_roll + 1
									i.total_yard = new_total_yard + dg[2]
						else :
							if dg[0] :
								pp_so = self.append('packing_list_data', {})
								pp_so.item_code_variant = dg[1]
								pp_so.yard_per_roll = dg[2]
								pp_so.total_yard = dg[2]
								pp_so.total_roll = 1
								pp_so.group = dg[0]
								pp_so.parent_item = dg[4]
								pp_so.item_name = dg[3]
								pp_so.warehouse = dg[5]
								pp_so.colour = dg[6]
								pp_so.design = dg[7]
							
					else :
						if dg[0] :
							pp_so = self.append('packing_list_data', {})
							pp_so.item_code_variant = dg[1]
							pp_so.yard_per_roll = dg[2]
							pp_so.total_yard = dg[2]
							pp_so.total_roll = 1
							pp_so.group = dg[0]
							pp_so.parent_item = dg[4]
							pp_so.item_name = dg[3]
							pp_so.warehouse = dg[5]
							pp_so.colour = dg[6]
							pp_so.design = dg[7]
						
			else :
				frappe.throw("Group Tidak Active / Tidak Memiliki Item")

		else :
			frappe.throw("Group Item belum dipilih")



@frappe.whitelist()
def submit_delivery_note(doc,method):
	if doc.packing_list_delivery and doc.purchase_order:
		frappe.db.sql ("""
			update 
			`tabPacking List Delivery` 
			set 
			is_used=1
			where 
			name="{0}"
			 """.format(doc.packing_list_delivery))

		frappe.db.commit()
		msgprint("Akan mengganti data di SO yang bersangkutan sesuai dengan Packing List Delivery (masih on progress)")

@frappe.whitelist()
def cancel_delivery_note(doc,method):
	if doc.packing_list_delivery and doc.purchase_order:
		frappe.db.sql ("""
			update 
			`tabPacking List Delivery` 
			set 
			is_used=1
			where 
			name="{0}"
			 """.format(doc.packing_list_delivery))

		frappe.db.commit()
		msgprint("Akan mengembalikan data SO seperti semua (masih on progress)")