import json
import os
from typing import Optional, Union, Literal, Dict, List
from rapidfuzz import process, fuzz
from abc import ABC
from functools import lru_cache

# Load the data
_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

with open(os.path.join(_data_dir, "provinces.json"), encoding="utf-8") as f:
    _provinces = json.load(f)

with open(os.path.join(_data_dir, "districts.json"), encoding="utf-8") as f:
    _districts = json.load(f)

with open(os.path.join(_data_dir, "municipalities.json"), encoding="utf-8") as f:
    _municipalities = json.load(f)


# Type Definitions
EntityType = Literal["province", "district", "municipality", None]
LangType = Literal["en", "np", None]

SUPPORTED_LANGUAGES = {"en", "np"}


class _base(ABC):
    """
    Abstract base class providing common utilities for geodata access.
    """

    @staticmethod
    def _normalize_mode(mode: Optional[str]) -> Optional[str]:
        """
        Normalize and validate the language mode input.

        :param mode: Language code or None
        :return: Normalized language code or None
        """
        if mode is None:
            return None
        if not isinstance(mode, str):
            raise TypeError("Mode must be a string or None.")
        mode = mode.lower()
        if mode not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language mode '{mode}'. Supported modes: {', '.join(SUPPORTED_LANGUAGES)}"
            )
        return mode

    @staticmethod
    def _get_values_by_lang(mode: str, values: List) -> List[Dict]:
        name_key = f"name_{mode}"
        hq_key = f"headquarter_{mode}"

        return [
            {
                **{
                    k: v
                    for k, v in val.items()
                    if not k.startswith("name_") and not k.startswith("headquarter_")
                },
                "name": val.get(name_key, ""),
                "headquarter": val.get(hq_key, ""),
            }
            for val in values
        ]

    @staticmethod
    def _get_single_value_by_lang(mode: str, value: Dict) -> Dict:
        name_key = f"name_{mode}"
        hq_key = f"headquarter_{mode}"

        return {
            **{
                k: v
                for k, v in value.items()
                if not k.startswith("name_") and not k.startswith("headquarter_")
            },
            "name": value[name_key],
            "headquarter": value[hq_key],
        }

    @staticmethod
    def _get_by_id(id: int, values: List):
        return next((val for val in values if val["id"] == id), None)

    @staticmethod
    def _get_by_name(name: str, values: List):
        return next(
            (
                d
                for d in values
                if d["name_en"].lower() == name.lower() or d["name_np"] == name
            ),
            None,
        )


class provinces(_base):
    """
    Utility class for accessing province data with support for English and Nepali.
    """

    @classmethod
    @lru_cache(maxsize=None)
    def all(cls, mode: LangType = None) -> List[Dict]:
        """
        Return a list of all provinces, optionally filtered by language.

        :param mode: 'en' for English, 'np' for Nepali, None for full data
        :return: List of province dictionaries
        """
        mode = cls._normalize_mode(mode)

        if mode in SUPPORTED_LANGUAGES:
            return cls._get_values_by_lang(mode, _provinces)
        return [d.copy() for d in _provinces]

    @classmethod
    def get(
        cls, id: Optional[int] = None, name: Optional[str] = None, mode: LangType = None
    ) -> Optional[Dict]:
        """
        Get a single province by ID or name, optionally filtered by language.

        :param id: Province ID (int)
        :param name: Province name in English or Nepali (str)
        :param mode: 'en' or 'np' to return only the name in that language
        :return: Province dictionary or None if not found
        """
        if id is None and name is None:
            raise ValueError("Either 'id' or 'name' must be provided.")

        result = None

        if id is not None:
            if not isinstance(id, int):
                raise TypeError("'id' must be an integer.")
            result = cls._get_by_id(id, _provinces)

        elif name:
            if not isinstance(name, str):
                raise TypeError("'name' must be a string.")
            result = cls._get_by_name(name, _provinces)

        if not result:
            return None

        mode = cls._normalize_mode(mode)

        if mode in SUPPORTED_LANGUAGES:
            return cls._get_single_value_by_lang(mode, result)
        return result.copy()


class districts(_base):
    """
    Utility class for accessing district data with support for English and Nepali.
    """

    @classmethod
    @lru_cache(maxsize=None)
    def all(cls, mode: LangType = None) -> List[Dict]:
        """
        Return a list of all districts, optionally filtered by language.

        :param mode: 'en' for English, 'np' for Nepali, None for full data
        :return: List of district dictionaries
        """
        mode = cls._normalize_mode(mode)
        if mode in ("en", "np"):
            return cls._get_values_by_lang(mode, _districts)
        return [d.copy() for d in _districts]

    @classmethod
    def get(
        cls, id: Optional[int] = None, name: Optional[str] = None, mode: LangType = None
    ) -> Optional[Dict]:
        """
        Get a single district by ID or name, optionally filtered by language.

        :param id: District ID (int)
        :param name: District name in English or Nepali (str)
        :param mode: 'en' or 'np' to return only the name in that language
        :return: District dictionary or None if not found
        """

        if id is None and name is None:
            raise ValueError("Either 'id' or 'name' must be provided.")

        result = None

        if id is not None:
            if not isinstance(id, int):
                raise TypeError("'id' must be an integer.")
            result = cls._get_by_id(id, _districts)

        elif name:
            if not isinstance(name, str):
                raise TypeError("'name' must be a string.")
            result = cls._get_by_name(name, _districts)

        if not result:
            return None

        mode = cls._normalize_mode(mode)
        if mode in SUPPORTED_LANGUAGES:
            return cls._get_single_value_by_lang(mode, result)
        return result.copy()

    @classmethod
    def get_by_province(
        cls, province: Union[int, str], mode: LangType = None
    ) -> List[Dict]:
        """
        Get districts by province ID or name (English/Nepali), with optional language output.
        """
        if isinstance(province, int):
            province_id = province
        elif isinstance(province, str):
            matched_province = provinces.get(name=province)
            province_id = matched_province["id"] if matched_province else None
        else:
            raise TypeError("'province' must be an int or str.")

        if province_id is None:
            return []

        mode = cls._normalize_mode(mode)
        filtered = [d for d in _districts if d["province_id"] == province_id]

        if mode in SUPPORTED_LANGUAGES:
            return cls._get_values_by_lang(mode, filtered)
        return [d.copy() for d in filtered]


class municipalities(_base):
    """
    Utility class for accessing municipality data with support for English and Nepali.
    """

    @classmethod
    @lru_cache(maxsize=None)
    def all(cls) -> List[Dict]:
        """
        :return: List of district dictionaries
        """
        return [m.copy() for m in _municipalities]

    @classmethod
    def get(
        cls, id: Optional[int] = None, name: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get a single municipalilty by ID or name

        :param id: Municipality ID (int)
        :return: Municipality dictionary or None if not found
        """

        if id is None and name is None:
            raise ValueError("Either 'id' or 'name' must be provided.")

        if id is not None:
            if not isinstance(id, int):
                raise TypeError("'id' must be an integer.")
            return cls._get_by_id(id, _municipalities)

        elif name:
            if not isinstance(name, str):
                raise TypeError("'name' must be a string.")
            return next(
                (d for d in _municipalities if d["name_en"].lower() == name.lower()),
                None,
            )

        return None

    @classmethod
    def get_by_district(cls, district: Union[int, str]) -> List[Dict]:
        """
        Get municipalities by district ID or name (English/Nepali)
        """

        if isinstance(district, int):
            district_id = district
        elif isinstance(district, str):
            matched_district = districts.get(name=district)
            district_id = matched_district["id"] if matched_district else None
        else:
            raise TypeError("'district' must be an int or str.")

        if district_id is None:
            return []

        return [m for m in _municipalities if m["district_id"] == district_id]


class wards(_base):
    """
    Utility class for accessing wards data.
    """

    @classmethod
    def get_by_municipality(cls, municipality: Union[int, str]) -> List[int]:
        if isinstance(municipality, int):
            municipality_id = municipality
        elif isinstance(municipality, str):
            matched_municipality = municipalities.get(name=municipality)
            municipality_id = (
                matched_municipality["id"] if matched_municipality else None
            )
        else:
            raise TypeError("'municipality' must be an int or str.")

        if municipality_id is None:
            return []

        muni = municipalities.get(id=municipality_id)

        if not muni or "ward_count" not in muni:
            return []

        return list(range(1, muni["ward_count"] + 1))


class find(_base):
    @classmethod
    def province_by_district(cls, district: Union[int, str]) -> Optional[dict]:
        district_data = (
            districts.get(name=district)
            if isinstance(district, str)
            else next((d for d in _districts if d["id"] == district), None)
        )
        if not district_data:
            return None
        return next(
            (p for p in _provinces if p["id"] == district_data["province_id"]), None
        )

    @classmethod
    def district_by_municipality(cls, muni: Union[int, str]) -> Optional[dict]:
        muni_data = (
            next(
                (m for m in _municipalities if m["name_en"].lower() == muni.lower()),
                None,
            )
            if isinstance(muni, str)
            else next((m for m in _municipalities if m["id"] == muni), None)
        )
        if not muni_data:
            return None
        return next(
            (d for d in _districts if d["id"] == muni_data["district_id"]), None
        )

    @classmethod
    def get_hierarchy(cls, municipality_id: int) -> Optional[dict]:
        muni = next((m for m in _municipalities if m["id"] == municipality_id), None)
        if not muni:
            return None

        district = next((d for d in _districts if d["id"] == muni["district_id"]), None)
        province = (
            next((p for p in _provinces if p["id"] == district["province_id"]), None)
            if district
            else None
        )

        return {
            "province": province["name_en"] if province else None,
            "district": district["name_en"] if district else None,
            "municipality": muni["name_en"],
        }

    @classmethod
    def search(
        cls, name: str, type: EntityType = None, threshold: int = 80
    ) -> Optional[dict]:
        name = name.strip().lower()

        datasets = {
            "province": _provinces,
            "district": _districts,
            "municipality": _municipalities,
        }

        def build_search_map(data):
            # Create (label, original_data) for both English and Nepali names
            return [(item["name_en"].lower(), item) for item in data] + [
                (item["name_np"], item) for item in data
            ]

        if type:
            data = datasets.get(type)
            choices = build_search_map(data)
        else:
            # Combine all types
            choices = []
            for t, data in datasets.items():
                choices.extend(
                    [
                        (name, {**item, "type": t})
                        for name, item in build_search_map(data)
                    ]
                )

        # Perform fuzzy match
        match = process.extractOne(
            name, [label for label, _ in choices], scorer=fuzz.token_sort_ratio
        )
        if match and match[1] >= threshold:
            matched_label = match[0]
            result = next(item for label, item in choices if label == matched_label)
            return result if "type" in result else {"type": type, **result}

        return None
