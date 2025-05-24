from nepali_toolkit.numbers import number_to_nepali_words


def test_number_to_nepali_words():
    assert number_to_nepali_words(0) == "शून्य"
    assert number_to_nepali_words(5) == "पाँच"
    assert number_to_nepali_words(10) == "दश"
    assert number_to_nepali_words(25) == "पच्चीस"
    assert number_to_nepali_words(67) == "सत्तसठ्ठी"
    assert number_to_nepali_words(100) == "एक सय"
    assert number_to_nepali_words(125) == "एक सय पच्चीस"
    assert number_to_nepali_words(1012) == "एक हजार बाह्र"
    assert number_to_nepali_words(100000) == "एक लाख"
    assert number_to_nepali_words(1234567) == "बाह्र लाख चौँतीस हजार पाँच सय सत्तसठ्ठी"
