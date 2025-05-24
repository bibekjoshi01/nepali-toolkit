from nepali_toolkit.utils import slugify


def test_slugify_nepali():
    assert slugify("नेपाल सरकार") == "नेपाल-सरकार"
    assert slugify("मेरो_पहिलो पोस्ट!") == "मेरो-पहिलो-पोस्ट"
    assert slugify("नेपाल २०२५") == "नेपाल-२०२५"
    assert slugify("Hello World!") == "hello-world"
    assert slugify("स्पेशल @#$%^&*()") == "स्पेशल"
    assert slugify("___multiple__underscores___") == "multiple-underscores"
    assert slugify(" ---leading and trailing--- ") == "leading-and-trailing"
    assert slugify("Mix of English and नेपाली १२३") == "mix-of-english-and-नेपाली-१२३"
    assert slugify("") == ""
    assert slugify("२०७९") == "२०७९"
    assert slugify("Nepal २०८०") == "nepal-२०८०"
    assert slugify("जनकपुर १२३") == "जनकपुर-१२३"
    assert slugify("जनकपुर १२३", unique=True).startswith("जनकपुर-१२३-")


def test_slugify_nepali_unique():
    base_slug = slugify("नेपाल सरकार")
    unique_slug = slugify("नेपाल सरकार", unique=True)

    assert base_slug == "नेपाल-सरकार"
    assert unique_slug.startswith("नेपाल-सरकार-")
    # Check the unique suffix is 5 digits
    suffix = unique_slug.split("-")[-1]
    assert suffix.isdigit() and len(suffix) == 5
