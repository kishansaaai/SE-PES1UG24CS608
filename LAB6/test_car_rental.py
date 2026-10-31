import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics

# Example test case:
def test_single_economy_rental():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100]
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"

# TODO: Add test cases to achieve 90-100% on both Line and Branch coverage!