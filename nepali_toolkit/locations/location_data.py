import json
import os
from typing import Optional, Union, Literal, Dict
from rapidfuzz import process, fuzz

_dir = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(_dir, "data", "provinces.json"), encoding="utf-8") as f:
    _provinces = json.load(f)

with open(os.path.join(_dir, "data", "districts.json"), encoding="utf-8") as f:
    _districts = json.load(f)

with open(os.path.join(_dir, "data", "municipalities.json"), encoding="utf-8") as f:
    _municipalities = json.load(f)


EntityType = Literal["province", "district", "municipality", None]


class Location:
    class provinces:
        @staticmethod
        def list() -> list[Dict]:
            return _provinces

        @staticmethod
        def get_by_name(name: str) -> dict:
            return next(
                (
                    p
                    for p in _provinces
                    if p["name_en"].lower() == name.lower() or p["name_np"] == name
                ),
                None,
            )

        @staticmethod
        def get_by_id(id: int) -> dict:
            return next((p for p in _provinces if p["id"] == id or p["id"] == id), None)

    class districts:
        @staticmethod
        def list() -> list[Dict]:
            return _districts

        @staticmethod
        def get_by_name(name: str) -> Optional[dict]:
            return next(
                (
                    d
                    for d in _districts
                    if d["name_en"].lower() == name.lower() or d["name_np"] == name
                ),
                None,
            )

        @staticmethod
        def get_by_id(id: int) -> Optional[dict]:
            return next((p for p in _districts if p["id"] == id or p["id"] == id), None)

        @staticmethod
        def get_by_province(province: Union[int, str]) -> list:
            """Get districts by province name or number"""
            province_id = (
                province
                if isinstance(province, int)
                else next(
                    (
                        p["id"]
                        for p in _provinces
                        if p["name_en"].lower() == province.lower()
                        or p["name_np"] == province
                    ),
                    None,
                )
            )
            return (
                [d for d in _districts if d["province_id"] == province_id]
                if province_id
                else []
            )

    class municipalities:
        @staticmethod
        def list() -> list:
            return _municipalities

        @staticmethod
        def get_by_name(name: str) -> dict | None:
            return next(
                (m for m in _municipalities if m["name_en"].lower() == name.lower()),
                None,
            )

        @staticmethod
        def get_by_id(id: int) -> dict | None:
            return next((m for m in _municipalities if m["id"] == id), None)

        @staticmethod
        def get_by_district(district: Union[int, str]) -> list:
            district_id = (
                district
                if isinstance(district, int)
                else next(
                    (
                        d["id"]
                        for d in _districts
                        if d["name_en"].lower() == district.lower()
                        or d["name_np"] == district
                    ),
                    None,
                )
            )
            return (
                [m for m in _municipalities if m["district_id"] == district_id]
                if district_id
                else []
            )

    class wards:
        @staticmethod
        def get_by_municipality(municipality: Union[int, str]) -> list[int]:
            muni = None
            if isinstance(municipality, int):
                muni = next(
                    (m for m in _municipalities if m["id"] == municipality), None
                )
            else:
                muni = next(
                    (
                        m
                        for m in _municipalities
                        if m["name_en"].lower() == municipality.lower()
                        or m["name_np"] == municipality
                    ),
                    None,
                )
            if not muni:
                return []
            return list(range(1, muni["ward_count"] + 1))

    class find:
        @staticmethod
        def province_by_district(district: Union[int, str]) -> Optional[dict]:
            district_data = (
                Location.districts.get_by_name(district)
                if isinstance(district, str)
                else next((d for d in _districts if d["id"] == district), None)
            )
            if not district_data:
                return None
            return next(
                (p for p in _provinces if p["id"] == district_data["province_id"]), None
            )

        @staticmethod
        def district_by_municipality(muni: Union[int, str]) -> Optional[dict]:
            muni_data = (
                next(
                    (
                        m
                        for m in _municipalities
                        if m["name_en"].lower() == muni.lower()
                    ),
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

    @staticmethod
    def get_hierarchy(municipality_id: int) -> Optional[dict]:
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

    @staticmethod
    def search(
        name: str, type: EntityType = None, threshold: int = 80
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
