import math

DELIMITERS = ['-', ' ', '_', '#']
MAX_RENTAL_DAYS = 3650  # sanity cap (10 years) to reject absurd / overflowing values


def sanitize_license_plate(plate):
    """Remove delimiters and upper-case a plate. Non-string input -> ''."""
    if not isinstance(plate, str):
        return ""
    plate = plate.strip()
    for ch in DELIMITERS:
        plate = plate.replace(ch, '')
    return plate.upper()


def parse_trip_mileage(mileage_csv):
    """Parse 'a, b, c' into a list of floats.

    Empty items, non-numeric items, negative values, NaN and infinity are
    skipped instead of crashing. Non-string input -> [].
    """
    if not isinstance(mileage_csv, str):
        return []
    result = []
    for part in mileage_csv.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            value = float(part)
        except (ValueError, OverflowError):
            continue
        if math.isfinite(value) and value >= 0:
            result.append(value)
    return result


def format_rental_invoice(record):
    """Format 'Driver:Days:Category'. Malformed input -> 'Invalid rental record'."""
    invalid = "Invalid rental record"
    if not isinstance(record, str):
        return invalid
    parts = record.split(':')
    if len(parts) != 3:
        return invalid
    driver = parts[0].strip()
    category = parts[2].strip()
    if not driver or not category:
        return invalid
    try:
        days = int(parts[1].strip())
    except (ValueError, OverflowError):
        return invalid
    if days <= 0 or days > MAX_RENTAL_DAYS:
        return invalid
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"


def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    clean_plate = sanitize_license_plate(raw_plate)
    print("Sanitized Plate:", clean_plate)

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    mileage_list = parse_trip_mileage(csv_input)
    print("Parsed Mileage List:", mileage_list)

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    invoice = format_rental_invoice(record_input)
    print("Rental Invoice:", invoice)


if __name__ == "__main__":
    main()
