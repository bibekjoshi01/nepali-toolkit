from nepali_toolkit.locations import Location


def test_provinces_list():
    provinces = Location.provinces.list()
    assert isinstance(provinces, list)
    assert len(provinces) == 7
    assert any(p["name_en"] == "Madhesh Province" for p in provinces)


def test_provinces_get_by_name():
    result = Location.provinces.get_by_name("Sudurpashchim Province")
    assert result is not None
    assert result["id"] == 7

    result = Location.provinces.get_by_name("कोशी प्रदेश")
    assert result is not None
    assert result["id"] == 1

    result_invalid = Location.provinces.get_by_name("Non Existing")
    assert result_invalid is None


def test_provinces_get_by_id():
    result = Location.provinces.get_by_id(2)
    assert result is not None
    assert result["name_en"] == "Madhesh Province"

    result_invalid = Location.provinces.get_by_id(99)
    assert result_invalid is None


def test_list_districts():
    all_districts = Location.districts.list()
    assert isinstance(all_districts, list)
    assert any(d["name_en"] == "Bhojpur" for d in all_districts)


def test_get_district_by_name():
    district_data = Location.districts.get_by_name("Kanchanpur")
    assert district_data is not None
    assert district_data["name_np"] == "कञ्चनपुर"

    district_data = Location.districts.get_by_name("भोजपुर")
    assert district_data is not None
    assert district_data["name_en"] == "Bhojpur"


def test_get_district_by_id():
    district_data = Location.districts.get_by_id(77)
    assert district_data is not None
    assert district_data["name_en"] == "Kailali"


def test_get_districts_by_province_id():
    province_districts = Location.districts.get_by_province(7)
    assert isinstance(province_districts, list)
    assert len(province_districts) == 9
    assert any(d["name_en"] == "Kanchanpur" for d in province_districts)


def test_get_districts_by_province_name():
    province_districts = Location.districts.get_by_province("Koshi Province")
    assert isinstance(province_districts, list)
    assert len(province_districts) == 14
    assert any(d["name_en"] == "Jhapa" for d in province_districts)

    province_districts = Location.districts.get_by_province("बागमती प्रदेश")
    print(province_districts)
    assert isinstance(province_districts, list)
    assert any(d["name_np"] == "काठमाडौँ" for d in province_districts)


def test_list_municipalities():
    all_munis = Location.municipalities.list()
    assert isinstance(all_munis, list)
    assert any(m["name_en"] == "Bhojpur Municipality" for m in all_munis)


def test_get_municipality_by_name():
    muni = Location.municipalities.get_by_name("Bhojpur Municipality")
    assert muni is not None
    assert muni["name_en"] == "Bhojpur Municipality"


def test_get_municipality_by_id():
    muni = Location.municipalities.get_by_id(732)
    assert muni is not None
    assert muni["name_en"] == "Bhimdatta Municipality"


def test_get_municipalities_by_district_id():
    munis = Location.municipalities.get_by_district(76)
    assert isinstance(munis, list)
    assert len(munis) == 9
    assert any(m["name_en"] == "Bhimdatta Municipality" for m in munis)


def test_get_municipalities_by_district_name():
    munis = Location.municipalities.get_by_district("Bhojpur")
    assert isinstance(munis, list)
    assert any(m["name_en"] == "Hatuwagadhi Rural Municipality" for m in munis)
