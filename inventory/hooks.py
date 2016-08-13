# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "inventory"
app_title = "Inventory"
app_publisher = "Myme"
app_description = "Inventory"
app_icon = "octicon octicon-package"
app_color = "grey"
app_email = "technical.erpsonic@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/inventory/css/inventory.css"
# app_include_js = "/assets/inventory/js/inventory.js"

# include js, css files in header of web template
# web_include_css = "/assets/inventory/css/inventory.css"
# web_include_js = "/assets/inventory/js/inventory.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "inventory.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "inventory.install.before_install"
# after_install = "inventory.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "inventory.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"inventory.tasks.all"
# 	],
# 	"daily": [
# 		"inventory.tasks.daily"
# 	],
# 	"hourly": [
# 		"inventory.tasks.hourly"
# 	],
# 	"weekly": [
# 		"inventory.tasks.weekly"
# 	]
# 	"monthly": [
# 		"inventory.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "inventory.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "inventory.event.get_events"
# }

