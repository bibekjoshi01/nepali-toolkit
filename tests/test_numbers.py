from nepali_toolkit.numbers import to_english_number, to_nepali_number, is_nepali_number


def test_to_nepali_number():
    assert to_nepali_number(123) == "१२३"
    assert to_nepali_number("2078") == "२०७८"


def test_to_english_number():
    assert to_english_number("१२३") == "123"
    assert to_english_number("२०७८") == "2078"


def test_is_nepali_number():
    assert is_nepali_number("१२३४५") is True
    assert is_nepali_number("१२३3") is False
