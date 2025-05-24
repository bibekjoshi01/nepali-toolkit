import os
import json

_dir = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(_dir, "data", "number_words_map.json"), encoding="utf-8") as f:
    number_words = json.load(f)

# Define common place values
UNITS = [(10**7, "करोड"), (10**5, "लाख"), (10**3, "हजार"), (100, "सय")]


def number_to_nepali_words(number: int | str) -> str:
    """Convert a number to its Nepali words representation."""
    try:
        number = int(number)
    except ValueError:
        raise ValueError("Input must be an integer or string representing an integer")

    if number == 0:
        return number_words["0"]

    result = []
    for value, label in UNITS:
        unit = number // value
        if unit:
            result.append(f"{number_to_nepali_words(unit)} {label}")
            number %= value

    if number:
        if str(number) in number_words:
            result.append(number_words[str(number)])
        else:
            # For numbers not in JSON (e.g. 67), split tens and units
            tens = (number // 10) * 10
            units = number % 10
            if tens:
                result.append(number_words.get(str(tens), ""))
            if units:
                result.append(number_words.get(str(units), ""))

    return " ".join(filter(None, result))
