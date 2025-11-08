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
    "SUNG",  # Lao: tone marking variations (keep TAM, drop SUNG)
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
    # IMPORTANT: Only match scripts at the BEGINNING of the name to avoid
    # ambiguity (e.g., "CHEROKEE LETTER YI" should match CHEROKEE, not YI)
    script_suffix = ""
    script_words_to_remove = []

    # Sort scripts by word count (descending) to match multi-word scripts first
    sorted_scripts = sorted(
        SCRIPT_SUFFIXES.items(), key=lambda x: len(x[0].split()), reverse=True
    )

    for script, suffix in sorted_scripts:
        script_parts = script.split()
        # Check if the script name appears at the START of parts
        if len(script_parts) <= len(parts):
            if parts[: len(script_parts)] == script_parts:
                script_suffix = suffix
                script_words_to_remove = script_parts
                break

    # Remove script name words from parts
    if script_words_to_remove:
        # Remove all occurrences of script words
        for word in script_words_to_remove:
            parts = [p for p in parts if p != word]

    # Track special variants before removing descriptors
    # These help disambiguate otherwise identical names
    is_small_variant = "SMALL" in parts and not script_suffix
    is_symbol_for = "SYMBOL" in parts and "FOR" in parts
    is_punctuation_variant = "PUNCTUATION" in parts and not script_suffix
    is_small_capital = "SMALL" in parts and "CAPITAL" in parts
    is_symbol_variant = "SYMBOL" in parts and script_suffix  # Greek symbols
    is_accent_variant = "ACCENT" in parts and script_suffix  # Hebrew accents
    is_punctuation_script_variant = "PUNCTUATION" in parts and script_suffix
    # SMALL is only a variant for scripts when LETTER/LIGATURE is NOT present
    # (e.g., "ARABIC SMALL FATHA" vs "ARABIC FATHA")
    # but NOT for "LATIN SMALL LETTER A" or "LATIN SMALL LIGATURE OE"
    is_small_script_variant = (
        "SMALL" in parts
        and script_suffix
        and "CAPITAL" not in parts
        and "LETTER" not in parts
        and "LIGATURE" not in parts
    )
    # Keep category words that disambiguate
    has_radical = "RADICAL" in parts
    has_number = "NUMBER" in parts
    has_digit = "DIGIT" in parts
    has_ideograph = "IDEOGRAPH" in parts
    has_syllable = "SYLLABLE" in parts or "SYLLABICS" in parts

    # Remove category words (but keep some for disambiguation)
    parts_to_keep = set()
    if is_small_variant or is_small_capital or is_small_script_variant:
        parts_to_keep.add("SMALL")
    if is_symbol_for or is_symbol_variant:
        parts_to_keep.add("SYMBOL")
    # For non-script symbols, keep SYMBOL if it helps disambiguate
    if not script_suffix and "SYMBOL" in parts:
        parts_to_keep.add("SYMBOL")
    if is_punctuation_variant or is_punctuation_script_variant:
        parts_to_keep.add("PUNCTUATION")
    if is_accent_variant:
        parts_to_keep.add("ACCENT")
    # Keep category words that disambiguate
    if has_radical:
        parts_to_keep.add("RADICAL")
    if has_number:
        parts_to_keep.add("NUMBER")
    if has_digit:
        parts_to_keep.add("DIGIT")
    if has_ideograph:
        parts_to_keep.add("IDEOGRAPH")
    # Note: SYLLABLE/SYLLABICS now extracted as suffix, not kept in parts
    # Note: LETTER for caseless variants now extracted as suffix too
    # Keep MARK, LETTER, SIGN when they disambiguate
    if "MARK" in parts and "LETTER" not in parts:
        parts_to_keep.add("MARK")

    # Track if LETTER should be moved to end (for caseless variants)
    letter_suffix = ""
    if script_suffix:  # For script characters
        if "VOWEL" in parts:
            parts_to_keep.add("SIGN")  # VOWEL vs VOWEL SIGN
        # Move LETTER to end for caseless letters in scripts with case
        # e.g., "LATIN LETTER GLOTTAL STOP" -> "glottalStopLetter-lat"
        # Scripts with case: Latin, Greek, Cyrillic, Georgian, Cherokee, Limbu, Phags-pa
        scripts_with_case = {
            "-lat",
            "-gr",
            "-cyr",
            "-geo",
            "-glag",
            "-cop",
            "-arm",
            "-chr",
            "-limb",
            "-phag",
        }
        has_case_indicator = "SMALL" in parts or "CAPITAL" in parts

        # For Hiragana/Katakana, SMALL is part of letter name, not case
        # So treat as if it has case indicator (to avoid moving LETTER)
        if script_suffix in {"-hira", "-kata"}:
            has_case_indicator = True

        if (
            "LETTER" in parts
            and not has_case_indicator
            and script_suffix in scripts_with_case
        ):
            letter_suffix = "Letter"
        # Keep SIGN for specific scripts
        scripts_with_sign = {"-tai"}  # TAI YO: LETTER vs SIGN
        if "SIGN" in parts and script_suffix in scripts_with_sign:
            parts_to_keep.add("SIGN")
        if "MARK" in parts and ("LETTER" in name or "SIGN" in name):
            # e.g., SAMARITAN MARK IN vs SAMARITAN LETTER IN
            parts_to_keep.add("MARK")
            # Also move LETTER to end for caseless marks
            if (
                "LETTER" in parts
                and not has_case_indicator
                and script_suffix in scripts_with_case
            ):
                letter_suffix = "Letter"
    else:
        # For non-script items, keep SIGN to disambiguate
        # e.g., "COLON" vs "COLON SIGN"
        if "SIGN" in parts:
            parts_to_keep.add("SIGN")

    # Special handling for syllable tokens - extract before filtering
    # "YI SYLLABLE IT" -> "itSyllable-yi"
    # "ETHIOPIC SYLLABLE HA" -> "haSyllable-eth"
    # "CANADIAN SYLLABICS A" -> "aSyllabics-can"
    syllable_suffix = ""
    if "SYLLABLE" in parts:
        syllable_suffix = "Syllable"
        # SYLLABLE will be removed by DROP_CATEGORIES
    elif "SYLLABICS" in parts:
        syllable_suffix = "Syllabics"
        # Remove SYLLABICS from parts (not in DROP_CATEGORIES)
        parts = [p for p in parts if p != "SYLLABICS"]

    parts = [p for p in parts if p not in DROP_CATEGORIES or p in parts_to_keep]

    # Special handling for Hangul position indicators
    # Keep track if it's initial/medial/final before removing
    hangul_position = ""
    if script_suffix == "-ko":
        if "CHOSEONG" in name:
            hangul_position = "Cho"  # Initial
        elif "JUNGSEONG" in name:
            hangul_position = "Jung"  # Medial
        elif "JONGSEONG" in name:
            hangul_position = "Jong"  # Final
        # Remove the position words after saving them
        parts = [p for p in parts if p not in {"CHOSEONG", "JUNGSEONG", "JONGSEONG"}]

    # Remove case indicator words (but keep SMALL/CAPITAL for variant detection)
    case_indicators_to_remove = CASE_INDICATORS.copy()
    if is_small_variant or is_small_capital or is_small_script_variant:
        case_indicators_to_remove.discard("SMALL")
    # For small capitals, keep both SMALL and CAPITAL for disambiguation
    if is_small_capital:
        case_indicators_to_remove.discard("CAPITAL")
    # For Hiragana/Katakana, SMALL is part of the letter identity, not case
    if script_suffix in {"-hira", "-kata"}:
        case_indicators_to_remove.discard("SMALL")
    parts = [p for p in parts if p not in case_indicators_to_remove]

    # Remove "WITH" and similar connecting words (but keep FOR in SYMBOL FOR)
    # Don't remove TO/THE/OF when they're the main content (e.g., syllable names)
    # Only remove them if there are other content words left
    connecting_words_tentative = {"WITH", "OF"}
    if not is_symbol_for:
        connecting_words_tentative.add("FOR")
    # Don't remove TO/THE for syllables - they're the syllable value
    if not has_syllable:
        connecting_words_tentative.update({"TO", "THE"})
    # Count how many non-connecting content words we have
    content_words = [p for p in parts if p not in connecting_words_tentative]
    if len(content_words) > 0:
        # We have other content, safe to remove connecting words
        parts = [p for p in parts if p not in connecting_words_tentative]
    # Otherwise keep TO/THE/OF as they're the actual content
    # Keep AND/OR for logical operators - they're essential

    # Handle special multi-part name formats AFTER filtering
    # For Runic: handle hyphenated compounds and multi-part names
    if script_suffix == "-run":
        # Split hyphenated parts like "LONG-BRANCH-OSS" or "DOTTED-N"
        expanded_parts = []
        for part in parts:
            if "-" in part:
                # Split hyphenated parts
                expanded_parts.extend(part.split("-"))
            else:
                expanded_parts.append(part)
        parts = expanded_parts

        # For runic letters, filter single-letter transcription variants
        # "FEHU FEOH FE F" -> keep "FEHU", "FEOH", "FE", drop "F"
        # "OS O" -> keep "OS", drop "O"
        # "DOTTED-N" -> keep "DOTTED", "N" (both meaningful, not variants)
        # "V" -> keep "V" (only one part)

        # If we have 2+ parts and at least one is multi-letter (2+ chars),
        # check if they look like transcription variants
        if len(parts) >= 2:
            multi_letter_parts = [p for p in parts if len(p) > 1]
            single_letter_parts = [p for p in parts if len(p) == 1]

            # If ALL multi-letter parts look like transcriptions
            # (not descriptors like DOTTED, LONG, BRANCH)
            # then drop single letters
            descriptors = {"DOTTED", "LONG", "BRANCH", "SHORT", "GOLDEN"}
            non_descriptor_multi = [
                p for p in multi_letter_parts if p not in descriptors
            ]

            if non_descriptor_multi and single_letter_parts:
                # We have transcription variants, keep multi-letter only
                parts = multi_letter_parts
        # Otherwise keep all parts

    # Special handling for Latin combining marks
    # For Latin script: "COMBINING GRAVE ACCENT" -> "graveCombining"
    # (move "COMBINING" to the end, before script suffix)
    is_combining = False
    if "COMBINING" in name and not script_suffix:
        # No script detected means it's a Latin/generic combining mark
        is_combining = True
        # Remove COMBINING from parts - it will be appended later
        parts = [p for p in parts if p != "COMBINING"]

    # Special handling for Hebrew accent and punctuation marks
    # "HEBREW ACCENT GERESH" -> "gereshAccent-heb"
    # "HEBREW PUNCTUATION GERESH" -> "gereshPunctuation-heb"
    hebrew_suffix = ""
    if script_suffix == "-heb":
        if "ACCENT" in parts:
            hebrew_suffix = "Accent"
            parts = [p for p in parts if p != "ACCENT"]
        elif "PUNCTUATION" in parts:
            hebrew_suffix = "Punctuation"
            parts = [p for p in parts if p != "PUNCTUATION"]

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

    # For Hebrew, append accent/punctuation type at the end
    # (before script suffix)
    if hebrew_suffix:
        glyph_name += hebrew_suffix

    # For syllables, append syllable/syllabics type at the end
    # (before script suffix)
    if syllable_suffix:
        glyph_name += syllable_suffix

    # For caseless letters, append letter type at the end
    # (before script suffix)
    if letter_suffix:
        glyph_name += letter_suffix

    # For Hangul, append position indicator (before script suffix)
    if hangul_position:
        glyph_name += hangul_position

    # Special handling for Arabic tanween marks
    # Replace "tan" suffix with "Tanween" for fathatan, dammatan, kasratan
    if script_suffix == "-ar" and glyph_name.endswith("tan"):
        glyph_name = glyph_name[:-3] + "Tanween"

    # Add script suffix
    glyph_name += script_suffix

    return glyph_name
