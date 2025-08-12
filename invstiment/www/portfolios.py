import frappe


def _account_balance(account: str) -> float:
    if not account:
        return 0.0
    res = frappe.db.get_all(
        "GL Entry",
        filters={"account": account, "docstatus": 1},
        fields=["sum(debit) as dr", "sum(credit) as cr"],
    )
    if not res:
        return 0.0
    dr = float(res[0].get("dr") or 0)
    cr = float(res[0].get("cr") or 0)
    return dr - cr


def get_context(context):
    # Require login
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?redirect-to=/portfolios"
        return {}

    portfolios = frappe.get_all(
        "Portfolio",
        fields=["name", "portfolio_name", "currency", "cash_account", "securities_account"],
        order_by="creation desc",
    )

    cards = []
    for p in portfolios:
        cash_bal = _account_balance(p.cash_account)
        sec_bal = _account_balance(p.securities_account)
        total = cash_bal + sec_bal
        cards.append({
            "name": p.name,
            "title": p.portfolio_name,
            "currency": p.currency,
            "cash_balance": cash_bal,
            "securities_balance": sec_bal,
            "total": total,
            "desk_link": f"/app/portfolio/{p.name}",
            "details_link": f"/portfolios/{p.name}",
            "new_plan_link": f"/app/portfolio-plan/new-portfolio-plan?portfolio={p.name}",
            "cash_mgmt_link": f"/app/portfolio-cash-movement/new-portfolio-cash-movement?portfolio={p.name}",
        })

    context.no_cache = 1
    context.show_sidebar = 0
    context.portfolios = cards
    context.title = "نظرة عامة على المحافظ"
    return context
