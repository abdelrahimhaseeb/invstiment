app_name = "invstiment"
app_title = "Invstiment"
app_publisher = "abdelrahim"
app_description = "Investment module app"
app_email = "haseeb.inv@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "invstiment",
# 		"logo": "/assets/invstiment/logo.png",
# 		"title": "Invstiment",
# 		"route": "/invstiment",
# 		"has_permission": "invstiment.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/invstiment/css/hub.css",
]
app_include_js = [
    # Redirect Desk landing to the Workspaces Hub
    "/assets/invstiment/js/startup.js",
    # Toolbar quick access to the Hub
    "/assets/invstiment/js/toolbar_hub_button.js",
    # Fullscreen overlay fallback for the Hub
    "/assets/invstiment/js/hub_overlay.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/invstiment/css/invstiment.css"
# web_include_js = "/assets/invstiment/js/invstiment.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "invstiment/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "invstiment/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "portfolios"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# ERPNext and Frappe both define jinja.hooks as dict with lists inside; to avoid merge errors, use filters list
jinja = {
    "filters": [
        # utils lives under invstiment.invstiment
        "invstiment.invstiment.utils.format_currency",
    ]
}

# Dynamic Website Routes
website_route_rules = [
    {"from_route": "/portfolios/<portfolio>", "to_route": "portfolios_detail"},
    {"from_route": "/portfolios/<portfolio>/plans/<plan>", "to_route": "portfolio_plan_room"},
]

# Installation
# ------------

# before_install = "invstiment.install.before_install"
# after_install = "invstiment.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "invstiment.uninstall.before_uninstall"
# after_uninstall = "invstiment.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "invstiment.utils.before_app_install"
# after_app_install = "invstiment.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "invstiment.utils.before_app_uninstall"
# after_app_uninstall = "invstiment.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "invstiment.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"invstiment.tasks.all"
# 	],
# 	"daily": [
# 		"invstiment.tasks.daily"
# 	],
# 	"hourly": [
# 		"invstiment.tasks.hourly"
# 	],
# 	"weekly": [
# 		"invstiment.tasks.weekly"
# 	],
# 	"monthly": [
# 		"invstiment.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "invstiment.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "invstiment.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "invstiment.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["invstiment.utils.before_request"]
# after_request = ["invstiment.utils.after_request"]

# Job Events
# ----------
# before_job = ["invstiment.utils.before_job"]
# after_job = ["invstiment.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"invstiment.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

