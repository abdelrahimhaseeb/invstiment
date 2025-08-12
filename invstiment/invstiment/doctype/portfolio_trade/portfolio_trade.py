import frappe
from frappe.model.document import Document


class PortfolioTrade(Document):
    def on_submit(self):
        book_trade_accounting(self)


def _get_company():
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    if not company:
        frappe.throw("يرجى ضبط الشركة الافتراضية في Global Defaults")
    return company


def _get_income_account(company: str) -> str:
    # Try a specific account name first, then fallback to any leaf Income account
    acc = frappe.db.get_value(
        "Account",
        {"company": company, "account_name": ["in", ["أرباح/خسائر الاستثمارات", "Investment Gain/Loss"]], "is_group": 0},
        "name",
    )
    if acc:
        return acc
    return frappe.db.get_value("Account", {"company": company, "root_type": "Income", "is_group": 0}, "name")


def _get_expense_account(company: str) -> str:
    return frappe.db.get_value("Account", {"company": company, "root_type": "Expense", "is_group": 0}, "name")


def _get_fifo_layers(plan: str):
    """Build FIFO layers from submitted trades of the plan."""
    trades = frappe.get_all(
        "Portfolio Trade",
        filters={"plan": plan, "docstatus": 1},
        fields=["name", "trade_type", "qty", "price", "posting_date", "creation"],
        order_by="posting_date asc, creation asc",
    )
    layers = []  # list of dicts: {qty, price}
    for t in trades:
        if t.trade_type == "شراء":
            layers.append({"qty": float(t.qty), "price": float(t.price)})
        else:
            remaining = float(t.qty)
            i = 0
            while remaining > 0 and i < len(layers):
                take = min(remaining, layers[i]["qty"])
                layers[i]["qty"] -= take
                remaining -= take
                if layers[i]["qty"] <= 1e-9:
                    layers.pop(i)
                else:
                    i += 1
            # if remaining > 0: oversell, ignore for now (will yield negative inventory)
    return layers


def _compute_fifo_cost(plan: str, sell_qty: float) -> float:
    layers = _get_fifo_layers(plan)
    remaining = float(sell_qty)
    cost = 0.0
    i = 0
    while remaining > 0 and i < len(layers):
        available = layers[i]["qty"]
        take = min(remaining, available)
        cost += take * layers[i]["price"]
        remaining -= take
        if take >= available:
            i += 1
        else:
            layers[i]["qty"] -= take
    # If remaining > 0, we assume zero-cost for the extra (shouldn't happen ideally)
    return cost


def book_trade_accounting(doc):
    portfolio = frappe.get_doc("Portfolio", doc.portfolio)
    company = _get_company()

    if doc.trade_type == "شراء":
        # Dr Securities, Cr Cash
        accounts = [
            {"account": portfolio.securities_account, "debit_in_account_currency": doc.qty * doc.price},
            {"account": portfolio.cash_account, "credit_in_account_currency": doc.qty * doc.price},
        ]
    else:
        # Sell: compute FIFO cost and realized P&L
        sale_value = float(doc.qty) * float(doc.price)
        cost_value = _compute_fifo_cost(doc.plan, float(doc.qty))
        pl_value = sale_value - cost_value

        income_acc = _get_income_account(company)
        expense_acc = _get_expense_account(company)

        accounts = [
            {"account": portfolio.cash_account, "debit_in_account_currency": sale_value},
            {"account": portfolio.securities_account, "credit_in_account_currency": cost_value if cost_value > 0 else 0},
        ]
        # Recognize P/L
        if pl_value > 0:
            accounts.append({"account": income_acc, "credit_in_account_currency": pl_value})
        elif pl_value < 0:
            accounts.append({"account": expense_acc, "debit_in_account_currency": abs(pl_value)})

    je = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": doc.posting_date,
        "company": company,
        "accounts": accounts,
        "user_remark": f"قيد صفقة {doc.trade_type} للمحفظة {portfolio.name}"
    })
    je.insert()
    je.submit()
