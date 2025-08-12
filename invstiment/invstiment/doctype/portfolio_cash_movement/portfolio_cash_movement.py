import frappe
from frappe.model.document import Document


class PortfolioCashMovement(Document):
    def on_submit(self):
        post_cash_journal_entry(self)


def post_cash_journal_entry(doc):
    portfolio = frappe.get_doc("Portfolio", doc.portfolio)
    company = frappe.db.get_single_value("Global Defaults", "default_company")

    if doc.movement_type == "إيداع":
        accounts = [
            {"account": portfolio.cash_account, "debit_in_account_currency": doc.amount},
            {"account": frappe.db.get_value("Account", {"company": company, "root_type": "Equity", "is_group": 0}, "name"), "credit_in_account_currency": doc.amount},
        ]
    else:
        accounts = [
            {"account": portfolio.cash_account, "credit_in_account_currency": doc.amount},
            {"account": frappe.db.get_value("Account", {"company": company, "root_type": "Equity", "is_group": 0}, "name"), "debit_in_account_currency": doc.amount},
        ]

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": doc.posting_date,
        "company": company,
        "accounts": accounts,
        "user_remark": f"حركة نقدية للمحفظة {portfolio.name}"
    })
    je.insert()
    je.submit()
