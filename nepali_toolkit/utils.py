import re
import random
import unicodedata


def slugify(text: str, unique: bool = False) -> str:
    """
    Convert Nepali or mixed text into a URL-friendly slug.
    Keeps Nepali characters, ASCII letters, and numbers.
    Replaces whitespace/underscores with hyphens,
    removes special characters, and lowercases ASCII content.

    If `unique=True`, appends a random 5-digit number.
    """

    if not text:
        return ""

    # Normalize Unicode (important for consistent output)
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()

    # Replace spaces/underscores with hyphen
    text = re.sub(r"[ \t_]+", "-", text)

    # Retain: a-z, 0-9, Nepali Unicode (\u0900–\u097F), and Devanagari digits (\u0966–\u096F)
    text = re.sub(r"[^a-z0-9\u0900-\u097F\u0966-\u096F\-]", "", text)

    # Replace multiple hyphens with single
    text = re.sub(r"-{2,}", "-", text)

    # Strip leading/trailing hyphens
    text = text.strip("-")

    if unique:
        text += f"-{random.randint(10000, 99999)}"

    return text
