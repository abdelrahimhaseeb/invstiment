import frappe
from frappe import _
from frappe.model.document import Document


class Portfolio(Document):
    def after_insert(self):
        create_portfolio_accounts(self)


def get_dashboard_data():
    """Show related docs on Portfolio dashboard with automatic filtering by 'portfolio'."""
    return {
        "fieldname": "portfolio",
        "transactions": [
            {
                "label": _("الإدارة"),
                "items": [
                    "Portfolio Plan",
                    "Portfolio Trade",
                    "Portfolio Cash Movement",
                ],
            }
        ],
    }


def _get_or_create_parent_group(company: str, label: str, account_type: str | None = None) -> str:
    """Return a group account name for given label (and optional account_type);
    if not found, create it under Asset root.
    """
    # Try by account_type first (if provided)
    parent = None
    if account_type:
        parent = frappe.db.get_value(
            "Account", {"company": company, "account_type": account_type, "is_group": 1}, "name"
        )
    # Fallback search by account_name label (handles localized charts)
    if not parent:
        parent = frappe.db.get_value(
            "Account", {"company": company, "account_name": label, "is_group": 1}, "name"
        )
    if parent:
        return parent

    # Find the top-level Asset root group for this company
    assets_root = frappe.db.get_value(
        "Account",
        {
            "company": company,
            "root_type": "Asset",
            "is_group": 1,
            # top-level (no parent) or empty parent
            "parent_account": ["in", [None, ""]],
        },
        "name",
    )
    if not assets_root:
        # fallback: any Asset group
        assets_root = frappe.db.get_value(
            "Account", {"company": company, "root_type": "Asset", "is_group": 1}, "name"
        )
    if not assets_root:
        frappe.throw("لم يتم العثور على مجموعة الأصول (Asset) في شجرة الحسابات")

    # Create the missing parent group under Assets
    grp_doc = {
        "doctype": "Account",
        "account_name": label,
        "company": company,
        "parent_account": assets_root,
        "is_group": 1,
        "root_type": "Asset",
    }
    if account_type:
        grp_doc["account_type"] = account_type
    grp = frappe.get_doc(grp_doc).insert()
    return grp.name


def create_portfolio_accounts(doc):
    # Create Cash and Securities accounts and link them
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        frappe.throw("يرجى ضبط الشركة الافتراضية في Global Defaults")

    # Get or create parent groups
    # Cash parent: try by account_type, then by name, else create
    cash_parent = frappe.db.get_value(
        "Account", {"company": company, "account_type": "Cash", "is_group": 1}, "name"
    )
    if not cash_parent:
        cash_parent = frappe.db.get_value(
            "Account",
            {"company": company, "account_name": ["in", ["Cash", "نقدية"]], "is_group": 1},
            "name",
        )
    if not cash_parent:
        cash_parent = _get_or_create_parent_group(company, label="Cash", account_type="Cash")

    # Securities/Investments parent: prefer by name to avoid relying on account_type existence
    securities_parent = frappe.db.get_value(
        "Account",
        {"company": company, "account_name": ["in", ["Investments", "استثمارات", "الاستثمارات"]], "is_group": 1},
        "name",
    )
    if not securities_parent:
        # Create an Investments-like group if missing (no strict account_type needed)
        securities_parent = _get_or_create_parent_group(company, label="Investments", account_type=None)

    cash = frappe.get_doc({
        "doctype": "Account",
        "account_name": f"نقدية {doc.portfolio_name}",
        "company": company,
        "account_type": "Cash",
        "parent_account": cash_parent,
        "is_group": 0,
        "root_type": "Asset",
    }).insert()

    sec = frappe.get_doc({
        "doctype": "Account",
        "account_name": f"قيمة أسهم {doc.portfolio_name}",
        "company": company,
        # avoid enforcing non-standard account_type; group determines classification
        "parent_account": securities_parent,
        "is_group": 0,
        "root_type": "Asset",
    }).insert()

    frappe.db.set_value(doc.doctype, doc.name, "cash_account", cash.name)
    frappe.db.set_value(doc.doctype, doc.name, "securities_account", sec.name)
