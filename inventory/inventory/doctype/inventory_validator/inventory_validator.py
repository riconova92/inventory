# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

form_grid_templates = {
	"data_inventory_unchecked": "templates/includes/item_grid_packing_list_inventory_validator.html",
	"data_inventory_checked": "templates/includes/item_grid_packing_list_inventory_validator.html",
	"data_inventory_missing": "templates/includes/item_grid_packing_list_inventory_validator.html",

}



class InventoryValidator(Document):

	def get_button(self):
		if not self.get("get_item_code") :
			frappe.throw("Masukkan Item Code")
		
		item_clause = """ AND mi.`item_code`="{0}" """.format(self.get("get_item_code"))
		
		colour_clause = ""
		if self.get("get_colour") :
			colour_clause = """ AND di.`colour`="{0}" """.format(self.get("get_colour"))
		
		group_clause = ""
		if self.get("get_group") :
			group_clause = """ AND di.`group`="{0}" """.format(self.get("get_group"))
		
		data = frappe.db.sql(""" SELECT mi.`name`,mi.`item_code`,di.`colour`,di.`group`,di.`total_roll`,
			di.`yard_atau_meter_per_roll`,di.`warehouse`,di.`inventory_uom`,di.`total_yard_atau_meter` 
			FROM `tabMaster Inventory`mi JOIN `tabData Inventory`di ON di.`parent`=mi.`name`
			WHERE di.`total_roll` != 0
			{0} {1} {2} 

			ORDER BY di.`idx`
			""".format(item_clause,colour_clause,group_clause),as_dict = 1)
		# frappe.msgprint(str(data))
		for item in data :
			new_row = self.append("data_inventory_unchecked")
			new_row.item_code_variant = item.item_code
			new_row.colour = item.colour
			new_row.warehouse = item.warehouse
			new_row.inventory_uom = item.inventory_uom
			new_row.yard_atau_meter_per_roll = item.yard_atau_meter_per_roll
			new_row.total_yard_atau_meter = item.total_yard_atau_meter
			new_row.total_roll = item.total_roll
			new_row.group = item.group
		
	def validate_item(self):
		if self.item_code_variant_depan and self.yard_atau_meter and self.colour and self.warehouse and self.qty_roll :
			checker = False
			
			for d in self.get("data_inventory_unchecked"):
				if d.item_code_variant == self.item_code_variant_depan and d.yard_atau_meter_per_roll == self.yard_atau_meter and d.colour == self.colour and d.warehouse == self.warehouse  :
					if self.group_code :
						if self.qty_roll > 0 and ((not self.group_prefix+"."+self.group_code) or (self.group_prefix+"."+self.group_code) == d.group) :
							ch = ""
							for item_checked in self.get("data_inventory_checked") :
								if (item_checked.item_code_variant == self.item_code_variant_depan and 
									item_checked.yard_atau_meter_per_roll == self.yard_atau_meter and 
									item_checked.colour == self.colour and 
									item_checked.warehouse == self.warehouse
									and ((not self.group_prefix+"."+self.group_code) or (self.group_prefix+"."+self.group_code) == item_checked.group)) :
									ch = item_checked
							if ch == "" :
								frappe.throw("Beda")
								ch = self.append('data_inventory_checked') 
								ch.item_code_variant = d.item_code_variant
								ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
								ch.colour = d.colour
								ch.inventory_uom = d.inventory_uom
								ch.group = d.group
								ch.warehouse = d.warehouse
								ch.total_roll = 0
								ch.total_yard_atau_meter = 0
							
							checker = True
							ch = self.append('data_inventory_checked',{})
							
							if self.qty_roll >= d.total_roll :
								ch.total_roll = ch.total_roll + d.total_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + d.total_yard_atau_meter
								self.qty_roll = self.qty_roll - ch.total_roll
								self.remove(d)
							else :
								ch.total_roll = ch.total_roll + self.qty_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + (self.qty_roll * self.yard_atau_meter)
								d.total_roll = d.total_roll - self.qty_roll
								d.total_yard_atau_meter = d.total_yard_atau_meter - (self.qty_roll * self.yard_atau_meter)
								self.qty_roll = 0
						
						elif self.qty_roll < 0 :
							ch = ""
							for item_miss in self.get("data_inventory_missing") :
								if (item_miss.item_code_variant == self.item_code_variant_depan and 
									item_miss.yard_atau_meter_per_roll == self.yard_atau_meter and 
									item_miss.colour == self.colour and 
									item_miss.warehouse == self.warehouse
									and ((not self.group_prefix+"."+self.group_code) or (self.group_prefix+"."+self.group_code) == item_miss.group)) :
									ch = item_miss
							if ch == "" :
								frappe.throw("Beda")
								ch = self.append('data_inventory_missing') 
								ch.item_code_variant = d.item_code_variant
								ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
								ch.colour = d.colour
								ch.inventory_uom = d.inventory_uom
								ch.group = d.group
								ch.warehouse = d.warehouse
								ch.total_roll = 0
								ch.total_yard_atau_meter = 0
							
							
							if self.qty_roll <= d.total_roll :
								ch.total_roll = ch.total_roll + d.total_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + d.total_yard_atau_meter
								self.qty_roll = self.qty_roll - d.total_roll
								self.remove(d)
							else :
								ch.total_roll = ch.total_roll + self.qty_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + (self.qty_roll * self.yard_atau_meter)
								d.total_roll = d.total_roll - self.qty_roll
								d.total_yard_atau_meter = d.total_yard_atau_meter - (self.qty_roll * self.yard_atau_meter)
								self.qty_roll = 0
					
					else :
						if self.qty_roll > 0 :
							
							ch = ""
							for item_checked in self.get("data_inventory_checked") :
								if (item_checked.item_code_variant == self.item_code_variant_depan and 
									item_checked.yard_atau_meter_per_roll == self.yard_atau_meter and 
									item_checked.colour == self.colour and 
									item_checked.warehouse == self.warehouse
									and not item_checked.group ) :
									ch = item_checked
									continue
								frappe.throw("BEDA")
							if ch == "" :
								ch = self.append('data_inventory_checked') 
								ch.item_code_variant = d.item_code_variant
								ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
								ch.colour = d.colour
								ch.inventory_uom = d.inventory_uom
								ch.warehouse = d.warehouse
								ch.total_roll = 0
								ch.total_yard_atau_meter = 0
							
							checker = True
							
							if self.qty_roll >= d.total_roll :
								ch.total_roll = ch.total_roll + d.total_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + d.total_yard_atau_meter
								self.qty_roll = self.qty_roll - d.total_roll
								self.remove(d)
							else :
								ch.total_roll = ch.total_roll + self.qty_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + (self.qty_roll * self.yard_atau_meter)
								d.total_roll = d.total_roll - self.qty_roll
								d.total_yard_atau_meter = d.total_yard_atau_meter - (self.qty_roll * self.yard_atau_meter)
								self.qty_roll = 0
								
						elif self.qty_roll < 0 :
							ch = ""
							for item_miss in self.get("data_inventory_missing") :
								if (item_miss.item_code_variant == self.item_code_variant_depan and 
									item_miss.yard_atau_meter_per_roll == self.yard_atau_meter and 
									item_miss.colour == self.colour and 
									item_miss.warehouse == self.warehouse
									and not item_miss.group) :
									ch = item_miss
							if ch == "" :
								ch = self.append('data_inventory_missing') 
								ch.item_code_variant = d.item_code_variant
								ch.yard_atau_meter_per_roll = d.yard_atau_meter_per_roll
								ch.colour = d.colour
								ch.inventory_uom = d.inventory_uom
								ch.warehouse = d.warehouse
								ch.total_roll = 0
								ch.total_yard_atau_meter = 0
							
							
							if self.qty_roll <= d.total_roll :
								ch.total_roll = ch.total_roll + d.total_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + d.total_yard_atau_meter
								self.qty_roll = self.qty_roll - d.total_roll
								self.remove(d)
							else :
								ch.total_roll = ch.total_roll + self.qty_roll
								ch.total_yard_atau_meter = ch.total_yard_atau_meter + (self.qty_roll * self.yard_atau_meter)
								d.total_roll = d.total_roll - self.qty_roll
								d.total_yard_atau_meter = d.total_yard_atau_meter - (self.qty_roll * self.yard_atau_meter)
								self.qty_roll = 0
					
							
			if self.qty_roll > 0 :
				if checker :
					frappe.msgprint("Jumlah item melebihi yang tercatat pada Inventory. Kelebihan akan dimasukkan ke Missing")
				frappe.msgprint("Item tidak ada di dalam Inventory")
				add_item(self)

			self.yard_atau_meter = 0
			self.qty_roll = 1
			self.colour = self.get_colour
				
		else :
			frappe.throw("Data Item belum terisi dengan lengkap")
		
		
		
	pass
	
def add_item(self):
	count = 0
	if self.item_code_variant_depan and self.yard_atau_meter and self.colour and self.warehouse :
		master_item = frappe.get_doc("Item", self.item_code_variant_depan)
		if self.get("data_inventory_missing") :
			for i in self.data_inventory_missing :
				if self.group_prefix and self.group_code :
					if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == (self.group_prefix+"."+self.group_code)  :
						count = 1
				else :
					if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour  and not i.group :
						count = 1
			if count == 1 :
				for i in self.data_inventory_missing :
					if self.group_prefix and self.group_code :
						if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and i.group == (self.group_prefix+"."+self.group_code)  :
							i.total_roll = i.total_roll + self.qty_roll
							i.total_yard_atau_meter = i.total_yard_atau_meter + (self.yard_atau_meter * self.qty_roll)
					else :
						if i.item_code_variant == self.item_code_variant_depan and i.yard_atau_meter_per_roll == self.yard_atau_meter and i.warehouse == self.warehouse and i.colour == self.colour and not i.group  :
							i.total_roll = i.total_roll + self.qty_roll
							i.total_yard_atau_meter = i.total_yard_atau_meter + (self.yard_atau_meter * self.qty_roll)
						
			else :
				if self.group_prefix and self.group_code :
					pp_so = self.append('data_inventory_missing', {})
					pp_so.item_code_variant = self.item_code_variant_depan
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
					pp_so.total_roll = self.qty_roll
					pp_so.group = self.group_prefix+"."+self.group_code
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = master_item.stock_uom
						
				else :
					pp_so = self.append('data_inventory_missing', {})
					pp_so.item_code_variant = self.item_code_variant_depan
					pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
					pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
					pp_so.total_roll = self.qty_roll
					pp_so.warehouse = self.warehouse
					pp_so.colour = self.colour
					pp_so.inventory_uom = master_item.stock_uom

		else :
			if self.group_prefix and self.group_code :
				pp_so = self.append('data_inventory_missing', {})
				pp_so.item_code_variant = self.item_code_variant_depan
				pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
				pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
				pp_so.total_roll = self.qty_roll
				pp_so.group = self.group_prefix+"."+self.group_code
				pp_so.warehouse = self.warehouse
				pp_so.colour = self.colour
				pp_so.inventory_uom = master_item.stock_uom
					
			else :
				pp_so = self.append('data_inventory_missing', {})
				pp_so.item_code_variant = self.item_code_variant_depan
				pp_so.yard_atau_meter_per_roll = self.yard_atau_meter
				pp_so.total_yard_atau_meter = (self.yard_atau_meter * self.qty_roll)
				pp_so.total_roll = self.qty_roll
				pp_so.warehouse = self.warehouse
				pp_so.colour = self.colour
				pp_so.inventory_uom = master_item.stock_uom


			
	else :
		frappe.throw("Item Code / Colour / Warehouse / Yard / Meter tidak terisi")



@frappe.whitelist()
def save_inventory_validator(doc,method):

	# unchecked
	if doc.data_inventory_unchecked :
		total_uncheck = 0
		for i in doc.data_inventory_unchecked :
			total_uncheck = total_uncheck + float(i.total_roll)

		doc.total_uncheck = total_uncheck
			
			
	# missing
	if doc.data_inventory_missing :
		total_missing = 0
		for i in doc.data_inventory_missing :
			total_missing = total_missing + float(i.total_roll)

		doc.total_missing = total_missing
			
	