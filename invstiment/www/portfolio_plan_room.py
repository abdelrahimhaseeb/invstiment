import frappe


def get_context(context):
    # Require login
    if frappe.session.user == "Guest":
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/login?redirect-to=/portfolios"
        return {}

    portfolio_name = frappe.form_dict.get("portfolio")
    plan_name = frappe.form_dict.get("plan")

    if not portfolio_name or not plan_name:
        frappe.throw("روابط غير مكتملة")

    p = frappe.get_doc("Portfolio", portfolio_name)
    plan = frappe.get_doc("Portfolio Plan", plan_name)

    # Get levels
    levels = []
    for lv in plan.levels:
        levels.append({
            "level_no": lv.level_no,
            "price": float(lv.price or 0),
            "cash_share": float(lv.cash_share or 0),
        })

    # Last 20 trades for this plan
    trades = frappe.get_all(
        "Portfolio Trade",
        filters={"plan": plan.name},
        fields=["name", "trade_type", "qty", "price", "posting_date"],
        order_by="posting_date desc, creation desc",
        limit=20,
    )

    context.no_cache = 1
    context.show_sidebar = 0
    context.title = f"غرفة عمليات الخطة: {plan.symbol}"
    context.portfolio = {"name": p.name, "title": p.portfolio_name, "currency": p.currency}
    context.plan = {"name": plan.name, "symbol": plan.symbol}
    context.levels = levels
    context.trades = trades
    context.new_trade_links = {
        "buy": f"/app/portfolio-trade/new-portfolio-trade?portfolio={p.name}&plan={plan.name}&trade_type=شراء",
        "sell": f"/app/portfolio-trade/new-portfolio-trade?portfolio={p.name}&plan={plan.name}&trade_type=بيع",
    }
    return context
