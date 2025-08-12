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

    portfolio_name = frappe.form_dict.get("portfolio")
    if not portfolio_name:
        frappe.throw("لا يوجد معرف محفظة في الرابط")

    p = frappe.get_doc("Portfolio", portfolio_name)

    cash_bal = _account_balance(p.cash_account)
    sec_bal = _account_balance(p.securities_account)
    total = cash_bal + sec_bal

    plans = frappe.get_all(
        "Portfolio Plan",
        filters={"portfolio": p.name},
        fields=["name", "symbol", "fair_value", "lowest_price", "investment_amount"],
        order_by="creation desc",
    )

    plan_cards = []
    for pl in plans:
        plan_cards.append({
            "name": pl.name,
            "symbol": pl.symbol,
            "fair_value": float(pl.fair_value or 0),
            "lowest_price": float(pl.lowest_price or 0),
            "investment_amount": float(pl.investment_amount or 0),
            "room_link": f"/portfolios/{p.name}/plans/{pl.name}",
            "desk_link": f"/app/portfolio-plan/{pl.name}",
        })

    trades = frappe.get_all(
        "Portfolio Trade",
        filters={"portfolio": p.name},
        fields=["name", "plan", "trade_type", "qty", "price", "posting_date"],
        order_by="posting_date desc, creation desc",
        limit=10,
    )

    context.no_cache = 1
    context.show_sidebar = 0
    context.title = f"تفاصيل المحفظة {p.portfolio_name}"
    context.portfolio = {
        "name": p.name,
        "title": p.portfolio_name,
        "currency": p.currency,
        "cash_balance": cash_bal,
        "securities_balance": sec_bal,
        "total": total,
        "new_plan_link": f"/app/portfolio-plan/new-portfolio-plan?portfolio={p.name}",
        "cash_mgmt_link": f"/app/portfolio-cash-movement/new-portfolio-cash-movement?portfolio={p.name}",
        "desk_link": f"/app/portfolio/{p.name}",
    }
    context.plans = plan_cards
    context.trades = trades
    return context
