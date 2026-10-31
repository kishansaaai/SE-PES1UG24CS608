def process_rental_fleet(rentals, base_admin_fee):
    if not isinstance(rentals, list) or base_admin_fee < 0:
        raise ValueError("Invalid rental list or admin fee")

    total_revenue = 0.0
    risk_flags = 0

    for rental in rentals:
        if not rental.get("is_confirmed", False):
            continue

        vehicle_type = rental.get("vehicle_type", "economy")
        driver_age = rental.get("driver_age", 25)
        days = rental.get("days", 1)

        if days <= 0:
            risk_flags += 1
            continue

        if vehicle_type == "luxury":
            daily_rate = 120.0
        elif vehicle_type == "suv":
            daily_rate = 70.0
        else:
            daily_rate = 40.0

        contract_total = (daily_rate * days) + base_admin_fee

        for miles in rental.get("trip_segments", []):
            if miles < 0:
                risk_flags += 1
                continue
            if miles > 300:
                risk_flags += 1
                if driver_age < 21:
                    contract_total += 250.0
                    break
                contract_total += miles * 0.40
            else:
                contract_total += miles * 0.20

        if driver_age < 25:
            contract_total += 50.0 * days if vehicle_type == "luxury" else 20.0 * days

        total_revenue += contract_total

    if risk_flags > 4:
        return {"total_revenue": round(total_revenue, 2), "status": "HIGH_RISK_AUDIT"}
    if total_revenue == 0.0:
        return {"total_revenue": 0.0, "status": "EMPTY_BATCH"}
    return {"total_revenue": round(total_revenue, 2), "status": "STANDARD"}


def check_fleet_telematics(telematics_matrix):
    if not telematics_matrix:
        return "NO_DATA"

    for vehicle_logs in telematics_matrix:
        speeding_streak = 0
        for speed in vehicle_logs:
            if speed > 100:
                speeding_streak += 1
                if speeding_streak >= 2:
                    return "GROUND_VEHICLE"
            else:
                speeding_streak = 0
    return "SAFE"