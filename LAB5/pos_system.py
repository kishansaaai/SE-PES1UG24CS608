"""Calculate retail bills, preview discounts and save receipt logs."""

import re
import secrets

price_list = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
sales_total = 0
receipt_lines = []


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Calculate a bill and record it in the running sales total."""
    global sales_total
    if receipts is None:
        receipts = []
    subtotal = 0
    for item in cart_items:
        try:
            subtotal += price_list[item[0]] * item[1]
        except (KeyError, TypeError, IndexError):
            subtotal += 0
    total = subtotal + subtotal * tax_rate
    receipts.append(total)
    sales_total += total
    receipt_lines.append(
        f"Receipt #{1000 + secrets.randbelow(9000)} total={total:.2f}"
    )
    return total


def apply_promo_code(code_str):
    """Apply a discount using multiplication or subtraction."""
    match = re.fullmatch(
        r"total\s*([*-])\s*(\d+(?:\.\d+)?)", code_str.strip()
    )
    if match is None:
        raise ValueError("Enter a supported discount expression.")
    operation, amount = match.groups()
    if operation == "*":
        return sales_total * float(amount)
    return sales_total - float(amount)


def update_stock(item, qty):
    """Run the original stock update and report unknown products."""
    try:
        price_list[item] = price_list[item]
        print("Stock updated for", item, "by", qty)
    except KeyError:
        print("Unknown product:", item)


def save_receipt_log(filename="pos_log.txt"):
    """Append the receipt lines and close the file after writing."""
    with open(filename, "a", encoding="utf-8") as log_file:
        for line in receipt_lines:
            log_file.write(line + "\n")


def print_sales():
    """Display the running sales total."""
    print("Sales so far: " + str(sales_total))


def main():
    """Run the original checkout examples and ask for a discount."""
    print("Bill 1:", process_checkout([("pen", 3), ("notebook", 2)]))
    print("Bill 2:", process_checkout([("bag", 1), ("laptop", 1)]))
    print("Bill 3:", process_checkout([("bottle", -4)]))
    print("Bill 4:", process_checkout([("pen", "2")], tax_rate=-1))
    update_stock("laptop", 5)
    print("After promo:", apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    print("After your promo:", apply_promo_code(code))
    save_receipt_log()
    print_sales()


main()
