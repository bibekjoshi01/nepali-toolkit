import random
from .numbers import to_nepali_number, number_to_nepali_words

# For random Nepali names (short sample)
NEPALI_NAMES = [
    "आशिष",
    "सिता",
    "कृष्ण",
    "बिबेक" "गीता",
    "राजेश",
    "माया",
    "सन्देश",
    "प्रिया",
]


def random_number(start: int = 0, end: int = 1000) -> str:
    """Generate a random number between start and end and return in Nepali digits."""
    num = random.randint(start, end)
    return to_nepali_number(num)


def random_word_number(start: int = 0, end: int = 1000) -> str:
    """Generate a random number and return in Nepali words."""
    num = random.randint(start, end)
    return number_to_nepali_words(num)


def random_name() -> str:
    """Pick a random Nepali name."""
    return random.choice(NEPALI_NAMES)
