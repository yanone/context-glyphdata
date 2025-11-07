"""Core functionality for generating glyph names from Unicode data."""

import youseedee


# Mapping of script names to their short suffixes
SCRIPT_SUFFIXES = {
    "ARABIC": "-ar",
    "LATIN": "-lat",
    "GREEK": "-gr",
    "CYRILLIC": "-cyr",
    "HEBREW": "-he",
    "DEVANAGARI": "-dev",
    "BENGALI": "-bn",
    "GURMUKHI": "-gu",
    "GUJARATI": "-gj",
    "ORIYA": "-or",
    "TAMIL": "-ta",
    "TELUGU": "-te",
    "KANNADA": "-kn",
    "MALAYALAM": "-ml",
    "SINHALA": "-si",
    "THAI": "-th",
    "LAO": "-lo",
    "TIBETAN": "-ti",
    "MYANMAR": "-my",
    "GEORGIAN": "-geo",
    "HANGUL": "-ko",
    "ETHIOPIC": "-et",
    "CHEROKEE": "-chr",
    "CANADIAN": "-ca",
    "OGHAM": "-og",
    "RUNIC": "-ru",
    "KHMER": "-km",
    "MONGOLIAN": "-mn",
    "HIRAGANA": "-hira",
    "KATAKANA": "-kata",
    "BOPOMOFO": "-bo",
    "HAN": "-han",
    "YI": "-yi",
    "ARMENIAN": "-arm",
}

# Categories to drop from the name
DROP_CATEGORIES = {
    "LETTER",
    "MARK",
    "NUMBER",
    "PUNCTUATION",
    "SYMBOL",
    "SEPARATOR",
    "DIGIT",
    "SIGN",
    "LIGATURE",
    "SYLLABLE",
    "RADICAL",
    "IDEOGRAPH",
    "CHARACTER",
    "ACCENT",
}


def glyph_data_for_unicode(decimal_unicode):
    """
    Generate a short camelCase glyph name from a Unicode codepoint.

    Args:
        decimal_unicode (int): The Unicode codepoint as a decimal integer.

    Returns:
        str: A short camelCase glyph name.

    Example:
        >>> glyph_data_for_unicode(0x0627)  # ARABIC LETTER ALEF
        'alef-ar'
    """
    # Get Unicode character data
    ucd = youseedee.ucd_data(decimal_unicode)

    if not ucd or "Name" not in ucd:
        # Fallback for characters without names
        return f"uni{decimal_unicode:04X}"

    name = ucd["Name"]

    # Start processing the name
    parts = name.split()

    # Detect script suffix
    script_suffix = ""
    for script, suffix in SCRIPT_SUFFIXES.items():
        if script in parts:
            script_suffix = suffix
            # Remove script name from parts
            parts = [p for p in parts if p != script]
            break

    # Remove category words
    parts = [p for p in parts if p not in DROP_CATEGORIES]

    # Remove "WITH" and similar connecting words
    connecting_words = {"WITH", "AND", "OR", "FOR", "TO", "OF", "THE"}
    parts = [p for p in parts if p not in connecting_words]

    if not parts:
        # If nothing left, use fallback
        return f"uni{decimal_unicode:04X}"

    # Convert to camelCase
    # First word is lowercase, rest are title case
    glyph_name = parts[0].lower()
    for part in parts[1:]:
        glyph_name += part.capitalize()

    # Add script suffix
    glyph_name += script_suffix

    return glyph_name
