"""Core functionality for generating glyph names from Unicode data."""

import youseedee


# Mapping of script names to their short suffixes
# Compiled from analysis of actual Unicode character names
# Covers the most common scripts found in Unicode character names
SCRIPT_SUFFIXES = {
    # Major world scripts
    "ARABIC": "-ar",
    "LATIN": "-lat",
    "GREEK": "-gr",
    "CYRILLIC": "-cyr",
    "HEBREW": "-heb",
    "ARMENIAN": "-arm",
    # Indic scripts
    "DEVANAGARI": "-dev",
    "BENGALI": "-ben",
    "GURMUKHI": "-gur",
    "GUJARATI": "-guj",
    "ORIYA": "-ori",
    "TAMIL": "-tam",
    "TELUGU": "-tel",
    "KANNADA": "-kan",
    "MALAYALAM": "-mal",
    "SINHALA": "-sin",
    "GRANTHA": "-gran",
    "BRAHMI": "-brah",
    "KAITHI": "-kthi",
    "SHARADA": "-shrd",
    "BHAIKSUKI": "-bhks",
    "KHUDAWADI": "-sind",
    # Southeast Asian scripts
    "THAI": "-th",
    "LAO": "-lao",
    "MYANMAR": "-mya",
    "KHMER": "-khm",
    "JAVANESE": "-java",
    "BALINESE": "-bali",
    "CHAM": "-cham",
    # Tibetan & Himalayan
    "TIBETAN": "-tib",
    "LEPCHA": "-lepc",
    "LIMBU": "-limb",
    # East Asian scripts
    "HAN": "-han",
    "HANGUL": "-ko",
    "HIRAGANA": "-hira",
    "KATAKANA": "-kata",
    "BOPOMOFO": "-bop",
    "YI": "-yi",
    # African scripts
    "ETHIOPIC": "-eth",
    "VAI": "-vai",
    "BAMUM": "-bam",
    "ADLAM": "-adlm",
    "NKO": "-nko",
    "TIFINAGH": "-tfng",
    "OSMANYA": "-osma",
    # American scripts
    "CHEROKEE": "-chr",
    "CANADIAN": "-can",
    "DESERET": "-dsrt",
    "OSAGE": "-osge",
    # Central Asian scripts
    "MONGOLIAN": "-mon",
    "PHAGS-PA": "-phag",
    # Historical scripts
    "GEORGIAN": "-geo",
    "GLAGOLITIC": "-glag",
    "COPTIC": "-cop",
    "OGHAM": "-ogh",
    "RUNIC": "-run",
    "GOTHIC": "-goth",
    # Ancient scripts
    "CUNEIFORM": "-xsux",
    "EGYPTIAN": "-egy",
    "ANATOLIAN": "-hluw",
    "LINEAR": "-lin",
    "CYPRIOT": "-cprt",
    "PHOENICIAN": "-phnx",
    "ARAMAIC": "-arc",
    "AVESTAN": "-avst",
    "UGARITIC": "-ugar",
    # Other scripts
    "DUPLOYAN": "-dupl",
    "MENDE": "-men",
    "MIAO": "-plrd",
    "SAURASHTRA": "-saur",
    "HENTAIGANA": "-hent",
    "MASARAM": "-gonm",
    "GUNJALA": "-gong",
    "CYPRO-MINOAN": "-cpmn",
    "TANGUT": "-tang",
    "NUSHU": "-nshu",
    # Multi-word script names
    "CAUCASIAN ALBANIAN": "-aghb",
    "MRO": "-mroo",
    "TAI": "-tai",  # Covers Tai Le, Tai Tham, Tai Viet, etc.
    "OLD": "-old",  # Covers Old Italic, Old Persian, etc.
}

# Categories and descriptive words to drop from the name
DROP_CATEGORIES = {
    # General categories
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
    # Script-specific descriptive words
    "CHOSEONG",  # Hangul: initial consonant
    "JUNGSEONG",  # Hangul: medial vowel
    "JONGSEONG",  # Hangul: final consonant
    "SUNG",  # Lao: tone marking variations (keep TAM, drop SUNG)
    # Multi-part name separators (keep first word only)
    "TIMES",  # Cuneiform: "A TIMES B" -> just "a"
    # Runic descriptive names - keep shortest form
}

# Case indicator words to drop (we'll use actual casing instead)
CASE_INDICATORS = {
    "CAPITAL",
    "SMALL",
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

    # Check if this is a capital letter (before removing case indicators)
    is_capital = "CAPITAL" in parts

    # Detect script suffix (check multi-word scripts first, then single-word)
    script_suffix = ""
    script_words_to_remove = []

    # Sort scripts by word count (descending) to match multi-word scripts first
    sorted_scripts = sorted(
        SCRIPT_SUFFIXES.items(), key=lambda x: len(x[0].split()), reverse=True
    )

    for script, suffix in sorted_scripts:
        script_parts = script.split()
        # Check if all words of the script name appear consecutively in parts
        if len(script_parts) == 1:
            # Single-word script
            if script in parts:
                script_suffix = suffix
                script_words_to_remove = [script]
                break
        else:
            # Multi-word script - check for consecutive match
            for i in range(len(parts) - len(script_parts) + 1):
                if parts[i : i + len(script_parts)] == script_parts:
                    script_suffix = suffix
                    script_words_to_remove = script_parts
                    break
            if script_suffix:
                break

    # Remove script name words from parts
    if script_words_to_remove:
        # Remove all occurrences of script words
        for word in script_words_to_remove:
            parts = [p for p in parts if p != word]

    # Handle special multi-part name formats
    # For "X TIMES Y" (Cuneiform) -> keep only first word
    if "TIMES" in parts:
        times_index = parts.index("TIMES")
        parts = parts[:times_index]

    # For Runic multi-part names like "FEHU FEOH FE F" -> keep shortest
    # These have multiple space-separated uppercase single-letter variants
    if script_suffix == "-run" and len(parts) > 1:
        # Find the shortest uppercase single-letter part
        single_letters = [p for p in parts if len(p) == 1 and p.isupper()]
        if single_letters:
            parts = [single_letters[0]]
        else:
            # Keep the shortest part
            parts = [min(parts, key=len)]

    # Remove category words
    parts = [p for p in parts if p not in DROP_CATEGORIES]

    # Remove case indicator words
    parts = [p for p in parts if p not in CASE_INDICATORS]

    # Remove "WITH" and similar connecting words
    connecting_words = {"WITH", "AND", "OR", "FOR", "TO", "OF", "THE"}
    parts = [p for p in parts if p not in connecting_words]

    # Special handling for Latin combining marks
    # For Latin script: "COMBINING GRAVE ACCENT" -> "gravecombining"
    # (move "COMBINING" to the end, before script suffix)
    is_combining = False
    if "COMBINING" in name and not script_suffix:
        # No script detected means it's a Latin/generic combining mark
        is_combining = True
        # Remove COMBINING from parts - it will be appended later
        parts = [p for p in parts if p != "COMBINING"]

    if not parts:
        # If nothing left, use fallback
        return f"uni{decimal_unicode:04X}"

    # Convert to camelCase with proper casing
    # For capital letters: First letter uppercase, rest lowercase (title case)
    # Exception: Multi-letter acronyms (2-3 letter ligatures like AE, OE, IJ)
    #            keep all uppercase
    # For small letters: All lowercase in first word
    # Subsequent words are always title case

    first_part = parts[0]

    # Check if first part is a multi-letter acronym/ligature
    # These are ligatures composed of single letters (AE, OE, IJ)
    # Criteria: 2-3 letters, all uppercase, is a capital letter, all alphabetic
    is_multi_letter_ligature = (
        len(first_part) in (2, 3)  # 2-3 letters only
        and first_part.isupper()  # All uppercase
        and is_capital  # Is a capital letter
        and all(c.isalpha() for c in first_part)  # Only letters
        and script_suffix == "-lat"  # Only for Latin script
    )

    if is_multi_letter_ligature:
        # Keep as uppercase for ligatures (e.g., AE, OE, IJ)
        glyph_name = first_part
    elif is_capital:
        # Capital letter: Use title case (first upper, rest lower)
        # Applies to all scripts: Latin, Cyrillic, Armenian, Georgian, etc.
        glyph_name = first_part.capitalize()
    else:
        # Small letter or no case indicator: all lowercase
        glyph_name = first_part.lower()

    # Add remaining parts in title case
    for part in parts[1:]:
        glyph_name += part.capitalize()

    # For Latin combining marks, append "Combining" at the end
    # (before script suffix)
    if is_combining:
        glyph_name += "Combining"

    # Special handling for Arabic tanween marks
    # Replace "tan" suffix with "Tanween" for fathatan, dammatan, kasratan
    if script_suffix == "-ar" and glyph_name.endswith("tan"):
        glyph_name = glyph_name[:-3] + "Tanween"

    # Add script suffix
    glyph_name += script_suffix

    return glyph_name
