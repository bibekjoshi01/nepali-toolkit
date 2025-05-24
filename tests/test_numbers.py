from nepali_toolkit.numbers import (
    to_english_number,
    to_nepali_number,
    is_nepali_number,
    contains_nepali_digits,
)


def test_to_nepali_number():
    assert to_nepali_number(123) == "१२३"
    assert to_nepali_number("2078") == "२०७८"
    assert to_nepali_number("2078-05-02") == "२०७८-०५-०२"
    assert to_nepali_number(3.14) == "३.१४"
    assert to_nepali_number("0.01%") == "०.०१%"


def test_to_english_number():
    assert to_english_number("१२३") == "123"
    assert to_english_number("२०७८") == "2078"
    assert to_english_number("२०७८-०५-०२") == "2078-05-02"
    assert to_english_number("३.१४") == "3.14"


def test_is_nepali_number():
    assert is_nepali_number("१२३४५") is True
    assert is_nepali_number("१२३-०९-७८-३४") is True
    assert is_nepali_number("१२३-०९-७८-३४", strict=True) is False
    assert is_nepali_number("१२३3") is False
    assert is_nepali_number("१२३४५६७८९०", strict=True) is True
    assert is_nepali_number("") is True  # empty is valid in non-strict
    assert is_nepali_number("", strict=True) is True


def test_contains_nepali_digits():
    assert contains_nepali_digits("२०७८") is True
    assert contains_nepali_digits("abc१२३xyz") is True
    assert contains_nepali_digits("123") is False
    assert contains_nepali_digits("") is False


def test_roundtrip_conversion():
    original = "7895"
    nepali = to_nepali_number(original)
    english = to_english_number(nepali)
    assert english == original

    nepali_back = to_nepali_number(english)
    assert nepali_back == nepali


def test_invalid_inputs():
    import pytest

    with pytest.raises(ValueError):
        to_nepali_number([123])  # list is invalid

    with pytest.raises(ValueError):
        to_english_number(123)  # int is invalid

    assert is_nepali_number(123) is False
    assert contains_nepali_digits(123) is False
