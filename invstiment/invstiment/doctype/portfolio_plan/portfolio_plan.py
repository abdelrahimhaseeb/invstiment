import frappe
from frappe.model.document import Document


class PortfolioPlan(Document):
    def validate(self):
        if self.fair_value <= self.lowest_price:
            frappe.throw("القيمة العادلة يجب أن تكون أعلى من أقل سعر")

    def on_submit(self):
        calculate_theoretical_levels(self)


def calculate_theoretical_levels(doc):
    # Generate 5 levels between fair_value and lowest_price
    levels_count = 5
    price_step = (doc.fair_value - doc.lowest_price) / (levels_count - 1)

    unit = doc.investment_amount / (doc.division_factor * (levels_count * (levels_count + 1) / 2))
    # inverted pyramid weights: 1,2,3,4,5
    weights = list(range(1, levels_count + 1))

    doc.levels = []
    for i in range(levels_count):
        level_no = i + 1
        price = doc.fair_value - price_step * i
        cash_share = unit * weights[i] * doc.division_factor
        doc.append("levels", {"level_no": level_no, "price": price, "cash_share": cash_share})
