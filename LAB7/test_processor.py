from hypothesis import given, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice


@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    try:
        result = sanitize_license_plate(s)
    except Exception as e:
        assert False, f"sanitize_license_plate crashed with: {e!r}"
    # Property: output is always a string with no delimiter characters
    assert isinstance(result, str)
    assert not any(ch in result for ch in "-_ #")


@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    try:
        result = parse_trip_mileage(s)
    except Exception as e:
        assert False, f"parse_trip_mileage crashed with: {e!r}"
    # Property: output is always a list of finite, non-negative floats
    assert isinstance(result, list)
    assert all(isinstance(m, float) and 0 <= m < float("inf") for m in result)


@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    try:
        result = format_rental_invoice(s)
    except Exception as e:
        assert False, f"format_rental_invoice crashed with: {e!r}"
    # Property: output is always a string
    assert isinstance(result, str)
