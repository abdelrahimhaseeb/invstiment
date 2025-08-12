import frappe


def format_currency(value, currency=None):
    try:
        return frappe.utils.fmt_money(value or 0, currency=currency)
    except Exception:
        return value
