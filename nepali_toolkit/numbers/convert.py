import os
import json
from typing import Union

_dir = os.path.dirname(os.path.dirname(__file__))

# Load the digit mapping from JSON
with open(os.path.join(_dir, "data", "digits_map.json"), encoding="utf-8") as f:
    digits_map = json.load(f)


def to_nepali_number(number: Union[int, float, str]) -> str:
    """Convert English digits to Nepali (Devanagari) digits."""
    if not isinstance(number, (int, float, str)):
        raise ValueError("Input must be int, float, or str.")

    return "".join(digits_map["to_nepali"].get(char, char) for char in str(number))


def to_english_number(nepali_number: str) -> str:
    """Convert Nepali (Devanagari) digits to English digits."""
    if not isinstance(nepali_number, str):
        raise ValueError("Input must be a string.")

    return "".join(digits_map["to_english"].get(char, char) for char in nepali_number)


def is_nepali_number(text: str, strict: bool = False) -> bool:
    """
    Check if the given string is a Nepali number.

    - If strict=True: All characters must be Nepali digits.
    - If strict=False: All numeric characters must be Nepali digits;
                       non-digit characters (like '-' or '.') are ignored.
    """
    if not isinstance(text, str):
        return False

    if strict:
        return all(char in digits_map["to_english"] for char in text)
    else:
        return all(
            char not in digits_map["to_english"].values()  # English digit
            if char.isdigit()
            else True  # ignore symbols
            for char in text
        )


def contains_nepali_digits(text: str) -> bool:
    """Check if any Nepali digit is in the given string."""
    if not isinstance(text, str):
        return False

    return any(char in digits_map["to_english"] for char in text)
