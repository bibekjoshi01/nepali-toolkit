from nepali_toolkit import random_number, random_word_number, random_name


def test_random_nepali_number():
    for _ in range(20):  # test multiple times
        num_str = random_number(1, 1000)
        # Should be Nepali digits only
        assert all(
            "\u0966" <= ch <= "\u096F" for ch in num_str
        ), f"Got invalid chars: {num_str}"


def test_random_nepali_word_number():
    for _ in range(20):
        word = random_word_number(0, 200)
        # Check that output is string and not empty
        assert isinstance(word, str)
        assert len(word) > 0


def test_random_nepali_name():
    for _ in range(20):
        name = random_name()
        # Should be from your defined name list
        assert name in [
            "आशिष",
            "सिता",
            "कृष्ण",
            "बिबेक" "गीता",
            "राजेश",
            "माया",
            "सन्देश",
            "प्रिया",
        ]
