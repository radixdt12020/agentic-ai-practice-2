def calculate_discount_price(original_price, discount_percent):
    # BUG 1: Missing type annotations and docstrings (violates AGENTS.md)
    # BUG 2: Crashes with ZeroDivisionError or negative pricing
    discount_amount = original_price * (discount_percent / 100)
    final_price = original_price - discount_amount
    return final_price

def split_bill(total_amount, num_people):
    # BUG 3: Division by zero if num_people == 0
    return total_amount / num_people
