import re
from typing import Optional, Callable
from .helpers import load_nepal_postal_codes, convert_nepali_digits_to_english


def validate_phone_number(
    phone: str,
    is_mobile_no: Optional[bool] = None,
    require_country_code: Optional[bool] = None,
) -> bool:
    """
    Validates Nepali phone number with optional country code and mobile number restriction.

    Args:
        phone (str): Phone number string.
        is_mobile_no (Optional[bool]):
            - True: Validate only mobile numbers.
            - False: Validate only landline or special numbers.
            - None: Validate any valid number type.
        require_country_code (Optional[bool]):
            - True: Requires +977 or 00977 prefix.
            - False: Requires local format only.
            - None: Accepts both.

    Returns:
        bool: Whether the phone number is valid.
    """

    phone = re.sub(r"[ \-]", "", phone)  # Remove spaces and dashes

    # Country code check
    code_pattern = r"^(?:\+|00)?977"
    has_code = bool(re.match(code_pattern, phone))
    local_number = re.sub(code_pattern, "", phone)

    # Country code requirement validation
    if require_country_code is True and not has_code:
        return False
    if require_country_code is False and has_code:
        return False

    # Define patterns
    mobile_pattern = r"(98\d{8}|97\d{8}|91\d{8})"
    landline_special_pattern = r"(0?[1-9]\d{0,1}\d{5,7}|100|101|102|1498|900)"

    # Validate based on is_mobile_no flag
    if is_mobile_no is True:
        return bool(re.fullmatch(mobile_pattern, local_number))
    elif is_mobile_no is False:
        return bool(re.fullmatch(landline_special_pattern, local_number))
    else:
        # Accept either
        combined_pattern = rf"({mobile_pattern}|{landline_special_pattern})"
        return bool(re.fullmatch(combined_pattern, local_number))


def validate_nepali_name(name: str, strict: bool = False) -> bool:
    """
    Validates a name: allows Devanagari letters, ASCII letters,
    spaces, hyphens, dots, and apostrophes.

    Args:
        name (str): The name string to validate.
        strict (bool): If True, name must be non-empty after stripping.
                       If False, empty names return False anyway.

    Returns:
        bool: True if valid, False otherwise.
    """
    name = name.strip()
    if strict and not name:
        return False

    pattern = r"^[a-zA-Z\u0900-\u097F\s\-\.']+$"
    return bool(re.match(pattern, name))


def validate_postal_code(
    code: str, check: bool = True, location: Optional[str] = None
) -> bool:
    """
    Validate Nepali postal code with optional location check.

    Args:
        code (str): Postal code to validate.
        check (bool): If True, check postal code existence in dataset.
        location (Optional[str]): District or Post Office name (case-insensitive).

    Returns:
        bool: True if valid, else False.
    """
    code = code.strip()

    _postal_code_map, _post_office_map, _district_map = load_nepal_postal_codes()

    # Validate format first (5 digit number)
    if not re.fullmatch(r"\d{5}", code):
        return False

    if not check:
        return True

    if code not in _postal_code_map:
        return False

    if location is None:
        return True

    loc = location.lower().strip()

    if loc in _district_map and code in _district_map[loc]:
        return True

    if loc in _post_office_map and code in _post_office_map[loc]:
        return True

    return False


def validate_citizenship_format(cid: str) -> bool:
    """
    Validates citizenship number in format: DD-LL-WW-SSSSS

        Supports both English and Nepali digits.

    Format:
        - DD: District code (01-77)
        - LL: Local body code (00-99)
        - WW: Ward number (01-99)
        - SSSSS: Serial number (001-99999)

    Args:
        cid (str): Citizenship ID.
        check_district_code (bool): If True, validates district code (1-77).

    Returns:
        bool: True if format is valid.
    """
    cid = convert_nepali_digits_to_english(cid.strip())
    pattern = r"^(\d{2})-(\d{2})-(\d{2})-(\d{3,5})$"
    match = re.fullmatch(pattern, cid.strip())

    if not match:
        return False

    district, local, ward, serial = map(int, match.groups())

    if not (1 <= district <= 77):
        return False

    if not (0 <= local <= 99):
        return False

    if not (1 <= ward <= 99):
        return False

    if not (1 <= serial <= 99999):
        return False

    return True


def validate_pan(
    pan: str,
    check_existence: bool = False,
    existence_checker: Optional[Callable[[str], bool]] = None,
) -> bool:
    """
    Validates a PAN (Permanent Account Number) used in Nepal.

        Supports both English and Nepali digits.

    Args:
        pan (str): The PAN number as a string.
        check_existence (bool): If True, also checks existence via an external source.
        existence_checker (Callable[[str], bool], optional): Function to check existence.
            Should return True if PAN exists, False otherwise.

    Returns:
        bool: True if PAN is valid, else False.
    """
    pan = convert_nepali_digits_to_english(pan.strip())

    # Must be exactly 9 digits
    if not re.fullmatch(r"\d{9}", pan):
        return False

    if check_existence:
        if not existence_checker:
            raise ValueError(
                "existence_checker function must be provided when check_existence=True"
            )
        return existence_checker(pan)

    return True
