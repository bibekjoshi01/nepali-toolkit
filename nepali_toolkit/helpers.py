import json
import os


_dir = os.path.dirname(__file__)


def load_nepal_postal_codes():
    _postal_code_map = {}
    _post_office_map = {}
    _district_map = {}

    with open(
        os.path.join(_dir, "data", "postal_codes.json"), "r", encoding="utf-8"
    ) as f:
        data = json.load(f)

    _postal_code_map = {}
    _post_office_map = {}
    _district_map = {}

    for entry in data:
        code = str(entry["Postal"]["Pin Code"]).zfill(5)
        district = entry["District"].lower()
        post_office = entry["Post Office"].lower()

        _postal_code_map[code] = entry
        _post_office_map.setdefault(post_office, set()).add(code)
        _district_map.setdefault(district, set()).add(code)

    return _postal_code_map, _post_office_map, _district_map


def convert_nepali_digits_to_english(text: str) -> str:
    """Convert Nepali (Devanagari) digits to ASCII digits."""
    nepali_to_ascii = str.maketrans("०१२३४५६७८९", "0123456789")
    return text.translate(nepali_to_ascii)
