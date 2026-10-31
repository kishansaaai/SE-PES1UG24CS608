"""
Lab 6 - Branch Coverage Tests
Application under test: car_rental_rate.py
Student: SETAPESU26

This test suite exercises both the True and False outcome of every decision
branch in car_rental_rate.py, including boundary values and edge cases.

Run from this folder:
    coverage run --branch -m pytest BranchCoverageTest_SETAPESU26_car_rental_rate.py
    coverage report -m
"""

import pytest

from car_rental_rate import check_fleet_telematics, process_rental_fleet


# ---------------------------------------------------------------------------
# process_rental_fleet - validation branches
# ---------------------------------------------------------------------------

def test_non_list_rentals_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet("not-a-list", 10.0)


def test_negative_admin_fee_raises_value_error():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1.0)


def test_zero_admin_fee_is_valid():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 0.0)
    assert result["total_revenue"] == 40.0
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - rental filtering branches
# ---------------------------------------------------------------------------

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


def test_missing_is_confirmed_defaults_to_false_and_skips_rental():
    rentals = [
        {
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


def test_negative_days_is_flagged_and_skipped():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": -2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


# ---------------------------------------------------------------------------
# process_rental_fleet - vehicle type branches
# ---------------------------------------------------------------------------

def test_luxury_vehicle_uses_luxury_rate():
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


def test_suv_vehicle_uses_suv_rate():
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


def test_unknown_vehicle_type_uses_economy_rate():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "truck",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 90.0  # (40 * 2) + 10
    assert result["status"] == "STANDARD"


def test_missing_vehicle_type_defaults_to_economy():
    rentals = [
        {
            "is_confirmed": True,
            "driver_age": 30,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 90.0  # (40 * 2) + 10
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - trip segment branches and boundaries
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


def test_zero_miles_uses_standard_mileage_rate():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [0],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0  # (40 * 1) + 10 + (0 * 0.20)
    assert result["status"] == "STANDARD"


def test_300_miles_uses_standard_mileage_rate_boundary():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [300],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + (300 * 0.20) = 110
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"


def test_301_miles_uses_premium_mileage_rate_boundary():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [301],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + (301 * 0.40) = 170.40
    assert result["total_revenue"] == 170.40
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
    assert result["total_revenue"] == 210.0  # 40 + 10 + (400 * 0.40)
    assert result["status"] == "STANDARD"


def test_long_trip_for_driver_aged_21_uses_premium_rate_without_break():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 21,
            "days": 1,
            "trip_segments": [400],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + (400 * 0.40) + (20 * 1) = 230
    assert result["total_revenue"] == 230.0
    assert result["status"] == "STANDARD"


def test_long_trip_for_driver_aged_20_adds_surcharge_and_breaks():
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
    # 40 + 10 + 250 + 20 = 320; second segment is skipped by break.
    assert result["total_revenue"] == 320.0
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - driver age branches and boundaries
# ---------------------------------------------------------------------------

def test_driver_aged_25_does_not_receive_young_driver_surcharge():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 25,
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 90.0  # (40 * 2) + 10
    assert result["status"] == "STANDARD"


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
    assert result["total_revenue"] == 350.0  # (120 * 2) + 10 + (50 * 2)
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
    assert result["total_revenue"] == 190.0  # (70 * 2) + 10 + (20 * 2)
    assert result["status"] == "STANDARD"


def test_missing_driver_age_defaults_to_25_and_no_surcharge():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "days": 2,
            "trip_segments": [],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 90.0  # (40 * 2) + 10
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# process_rental_fleet - risk status branches
# ---------------------------------------------------------------------------

def test_exactly_four_risk_flags_remains_standard():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [-1, -1, -1, -1],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 50.0
    assert result["status"] == "STANDARD"


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
    assert result["total_revenue"] == 50.0
    assert result["status"] == "HIGH_RISK_AUDIT"


def test_risk_flags_from_long_trips_can_trigger_high_risk_audit():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [301, 301, 301, 301, 301],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    # 40 + 10 + (5 * 301 * 0.40) = 652
    assert result["total_revenue"] == 652.0
    assert result["status"] == "HIGH_RISK_AUDIT"


# ---------------------------------------------------------------------------
# process_rental_fleet - multiple rentals
# ---------------------------------------------------------------------------

def test_multiple_rentals_are_summed():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [100],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [],
        },
        {
            "is_confirmed": False,
            "vehicle_type": "suv",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [],
        },
    ]
    result = process_rental_fleet(rentals, 10.0)
    # Economy: 40 + 10 + 20 = 70
    # Luxury: 120 + 10 = 130
    # Unconfirmed SUV: 0
    assert result["total_revenue"] == 200.0
    assert result["status"] == "STANDARD"


# ---------------------------------------------------------------------------
# check_fleet_telematics - all branches
# ---------------------------------------------------------------------------

def test_telematics_with_no_data_returns_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_with_empty_vehicle_log_returns_safe():
    assert check_fleet_telematics([[]]) == "SAFE"


def test_telematics_with_safe_speeds_returns_safe():
    assert check_fleet_telematics([[80, 90, 100]]) == "SAFE"


def test_telematics_single_speeding_event_is_reset_by_slow_speed():
    assert check_fleet_telematics([[110, 90]]) == "SAFE"


def test_telematics_non_consecutive_speeding_events_are_safe():
    assert check_fleet_telematics([[110, 90, 110, 90]]) == "SAFE"


def test_telematics_two_consecutive_speeding_events_returns_ground_vehicle():
    assert check_fleet_telematics([[110, 120]]) == "GROUND_VEHICLE"


def test_telematics_boundary_101_twice_returns_ground_vehicle():
    assert check_fleet_telematics([[101, 101]]) == "GROUND_VEHICLE"


def test_telematics_boundary_100_is_not_speeding():
    assert check_fleet_telematics([[100, 101, 100, 101]]) == "SAFE"


def test_telematics_reset_then_consecutive_speeding_returns_ground_vehicle():
    assert check_fleet_telematics([[110, 90, 110, 120]]) == "GROUND_VEHICLE"


def test_telematics_checks_all_vehicles_in_the_matrix():
    assert check_fleet_telematics([[80, 90], [110, 120]]) == "GROUND_VEHICLE"


def test_telematics_safe_vehicles_after_one_another_returns_safe():
    assert check_fleet_telematics([[80, 90], [110, 90], [100, 100]]) == "SAFE"
