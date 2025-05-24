import os
import json


_dir = os.path.dirname(os.path.dirname(__file__))

# Load the digit mapping from JSON
with open(os.path.join(_dir, "data", "digits_map.json"), encoding="utf-8") as f:
    digits_map = json.load(f)


def to_nepali_number(number: int | str) -> str:
    """Convert Engling digits to Nepali (Devanagari) digits"""
    return "".join(digits_map["to_nepali"].get(char, char) for char in str(number))


def to_english_number(nepali_number: str) -> str:
    """Convert Nepali (Devanagari) digits to English digits."""
    return "".join(
        digits_map["to_english"].get(char, char) for char in str(nepali_number)
    )


def is_nepali_number(text: str) -> bool:
    """Check if the given string contains only Nepali digits."""
    return all(char in digits_map["to_english"] for char in text)
