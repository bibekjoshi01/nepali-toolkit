from nepali_toolkit.validators import (
    validate_citizenship_format,
    validate_phone_number,
    validate_nepali_name,
    validate_pan,
)
from nepali_toolkit.validators import validate_postal_code


def test_validate_phone_number():
    # Valid mobile numbers (local and with country code)
    assert validate_phone_number("9841234567")
    assert validate_phone_number("+9779812345678")
    assert validate_phone_number("9798765432")
    assert validate_phone_number("9198765432")
    assert validate_phone_number("9841234567", is_mobile_no=True)
    assert validate_phone_number("+9779812345678", is_mobile_no=True)
    assert not validate_phone_number(
        "01234567", is_mobile_no=True
    )  # landline, fail mobile-only

    # Valid landline numbers and special numbers (local and with country code)
    assert validate_phone_number("01-234567")
    assert validate_phone_number("0141234567")
    assert validate_phone_number("100")  # emergency number
    assert validate_phone_number("+977101", is_mobile_no=False)  # fire, special number
    assert not validate_phone_number(
        "9841234567", is_mobile_no=False
    )  # mobile, fail landline-only

    # Invalid numbers
    assert not validate_phone_number("1234567890")  # invalid pattern
    assert not validate_phone_number("+9876543210")  # invalid country code prefix
    assert not validate_phone_number(
        "+09-786754", is_mobile_no=True
    )  # invalid format mobile-only

    # Country code requirements
    assert validate_phone_number("+9779812345678", require_country_code=True)
    assert not validate_phone_number(
        "9812345678", require_country_code=True
    )  # no country code but required

    assert validate_phone_number("9812345678", require_country_code=False)
    assert not validate_phone_number(
        "+9779812345678", require_country_code=False
    )  # country code not allowed here

    # Accept both with require_country_code=None (default)
    assert validate_phone_number("9812345678", require_country_code=None)
    assert validate_phone_number("+9779812345678", require_country_code=None)


def test_nepali_name():
    assert validate_nepali_name("Bibek Joshi")
    assert validate_nepali_name("बिबेक जोशी")
    assert not validate_nepali_name("  ", strict=True)
    assert validate_nepali_name("नेपाल-भारत", strict=True)
    assert not validate_nepali_name("123", strict=True)
    assert not validate_nepali_name("", strict=True)


# Postal Code Validators


def test_postal_code_format_valid():
    assert validate_postal_code("10700") is True
    assert validate_postal_code("99999") is False
    assert validate_postal_code("1234") is False
    assert validate_postal_code("123456") is False
    assert validate_postal_code("12a45") is False


def test_postal_code_without_check():
    assert validate_postal_code("12345", check=False) is True
    assert validate_postal_code("abcde", check=False) is False


def test_postal_code_with_check():
    assert validate_postal_code("10700", check=True) is True
    assert validate_postal_code("99999", check=True) is False


def test_postal_code_with_location_district():
    assert validate_postal_code("10700", location="Achham") is True
    assert validate_postal_code("10700", location="Kathmandu") is False
    assert validate_postal_code("10700", location="  achham  ") is True


def test_postal_code_with_location_post_office():
    assert validate_postal_code("10701", location="Chaurpati") is True
    assert validate_postal_code("10701", location="Birtamode") is False
    assert validate_postal_code("10701", location="chaurpati") is True


def test_postal_code_invalid_inputs():
    assert validate_postal_code("", check=True) is False
    assert validate_postal_code("     ", check=True) is False
    assert validate_postal_code("abcde", check=True) is False
    assert validate_postal_code("1000", check=True) is False


# Pan No Validators


def mock_pan_exists(pan: str) -> bool:
    # Simulate a check against a database or external API
    return pan in {"123456789", "987654321"}


def test_validate_pan_existence_check():
    assert validate_pan("123456789") is True
    assert validate_pan("987654321") is True
    assert validate_pan("12345678") is False  # Too short
    assert validate_pan("1234567890") is False  # Too long
    assert validate_pan("12345A789") is False  # Contains letter

    def mock_checker(pan: str) -> bool:
        return pan == "111222333"

    assert validate_pan(
        "111222333", check_existence=True, existence_checker=mock_checker
    )
    assert not validate_pan(
        "999888777", check_existence=True, existence_checker=mock_checker
    )

    try:
        validate_pan("५६७४३५२३४", check_existence=True)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert (
            str(e)
            == "existence_checker function must be provided when check_existence=True"
        )


def test_valid_citizenship_format():
    assert validate_citizenship_format("75-01-78-00348")
    assert validate_citizenship_format("01-00-01-00001")

    assert validate_citizenship_format("७५-०१-७८-००३४८")
    assert validate_citizenship_format("०१-००-०१-००००१")

    assert not validate_citizenship_format("75017800348")  # missing dashes
    assert not validate_citizenship_format("75-01-78")  # incomplete
    assert not validate_citizenship_format("७५-०१-७८-००००००")  # serial too long
    assert not validate_citizenship_format("99-01-01-00001")  # invalid district

    assert validate_citizenship_format("01-01-01-00001")
    assert not validate_citizenship_format("99-01-01-00001")
