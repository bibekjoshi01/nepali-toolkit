from nepali_toolkit.datetime import date


def test_nepali_basic_date():
    x = date(2078, 9, 1)
    y = date(2078, 2, 8)
    assert str(x) == "2078-09-01"
    assert (x == y) is False
    assert (x > y) is True
    assert (x < y) is False 
