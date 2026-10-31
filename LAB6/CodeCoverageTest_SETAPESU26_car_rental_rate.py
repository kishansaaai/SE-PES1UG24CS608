"""
Lab 6 - Code Coverage Tests
Application under test: car_rental_rate.py
Student: SETAPESU26

This test suite is written to execute every executable line in
car_rental_rate.py at least once (100% line/code coverage).

Run from this folder:
    coverage run -m pytest CodeCoverageTest_SETAPESU26_car_rental_rate.py
    coverage report -m
"""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


# ---------------------------------------------------------------------------
# process_rental_fleet - validation and empty results
# ---------------------------------------------------------------------------

def test_invalid_rentals_type_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet("not-a-list", 10.0)


def test_negative_admin_fee_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1.0)


def test_empty_fleet_returns_empty_batch():
    result = process_rental_fleet([], 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_unconfirmed_rental_is_skipped():
    rentals = [
        {
            "is_confirmed": False,
            "vehicle_type": "luxury",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_zero_days_is_flagged_and_skipped():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 0,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


# ---------------------------------------------------------------------------
# process_rental_fleet - vehicle rates
# ---------------------------------------------------------------------------

def test_luxury_vehicle_rate():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 250.0  # (120 * 2) + 10
    assert result["status"] == "STANDARD"


def test_suv_vehicle_rate():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 150.0  # (70 * 2) + 10
    assert result["status"] == "STANDARD"


def test_economy_vehicle_rate_with_short_trip():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0  # (40 * 2) + 10 + (100 * 0.20)
    assert result["status"] == "STANDARD"


def test_default_values_are_used_for_missing_optional_fields():
    rentals = [{"is_confirmed": True}]
    result = process_rental_fleet(rentals, 10.0)
    # Defaults: economy rate, age 25, 1 day, no trip segments.
    assert result["total_revenue"] == 50.0  # (40 * 1) + 10
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - trip segments
# ---------------------------------------------------------------------------

def test_negative_miles_are_flagged_and_ignored():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [-5],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0  # (40 * 1) + 10
    assert result["status"] == "STANDARD"


def test_long_trip_for_normal_driver_uses_premium_rate():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [400],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + (400 * 0.40) = 210
    assert result["total_revenue"] == 210.0
    assert result["status"] == "STANDARD"


def test_long_trip_for_young_driver_adds_surcharge_and_breaks():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 20,
            "days": 1,
            "trip_segments": [400, 400],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + 250 (under-21 surcharge) + 20 (young-driver fee) = 320
    # The second segment is not processed because the loop breaks.
    assert result["total_revenue"] == 320.0
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - young driver surcharges
# ---------------------------------------------------------------------------

def test_young_driver_luxury_surcharge():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 24,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # (120 * 2) + 10 + (50 * 2) = 350
    assert result["total_revenue"] == 350.0
    assert result["status"] == "STANDARD"


def test_young_driver_non_luxury_surcharge():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 24,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # (70 * 2) + 10 + (20 * 2) = 190
    assert result["total_revenue"] == 190.0
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - risk status
# ---------------------------------------------------------------------------

def test_more_than_four_risk_flags_returns_high_risk_audit():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [-1, -1, -1, -1, -1],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0  # (40 * 1) + 10
    assert result["status"] == "HIGH_RISK_AUDIT"


# ---------------------------------------------------------------------------
# check_fleet_telematics
# ---------------------------------------------------------------------------

def test_telematics_with_no_data_returns_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_with_safe_speeds_returns_safe():
    assert check_fleet_telematics([[80, 90, 100]]) == "SAFE"


def test_telematics_single_speeding_event_is_reset_by_slow_speed():
    assert check_fleet_telematics([[110, 90]]) == "SAFE"


def test_telematics_two_consecutive_speeding_events_returns_ground_vehicle():
    assert check_fleet_telematics([[110, 120]]) == "GROUND_VEHICLE"


def test_telematics_checks_all_vehicles_in_the_matrix():
    assert check_fleet_telematics([[80, 90], [110, 120]]) == "GROUND_VEHICLE"
