# -*- coding: utf-8 -*-
# Copyright (c) 2015, Myme and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint

class InventoryReceipt(Document):
	def add_item(self):
		frappe.msgprint("test")