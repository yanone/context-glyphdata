"""Unit tests for glyph name generation."""

import unittest
import youseedee
from context_glyphdata import glyph_data_for_unicode


# Test data: (codepoint, expected_result, unicode_name)
# Organized by script categories matching SCRIPT_SUFFIXES
TEST_CASES = [
    #
    # Major world scripts - Latin
    (0x0041, "A-lat", "LATIN CAPITAL LETTER A"),
    (0x0061, "a-lat", "LATIN SMALL LETTER A"),
    (0x005A, "Z-lat", "LATIN CAPITAL LETTER Z"),
    (0x007A, "z-lat", "LATIN SMALL LETTER Z"),
    (0x00C6, "AE-lat", "LATIN CAPITAL LETTER AE"),
    (0x00E6, "ae-lat", "LATIN SMALL LETTER AE"),
    (0x0152, "OE-lat", "LATIN CAPITAL LIGATURE OE"),
    (0x0153, "oe-lat", "LATIN SMALL LIGATURE OE"),
    (0x0132, "IJ-lat", "LATIN CAPITAL LIGATURE IJ"),
    (0x0133, "ij-lat", "LATIN SMALL LIGATURE IJ"),
    (0x00DF, "sharpS-lat", "LATIN SMALL LETTER SHARP S"),
    (0x1E9E, "SharpS-lat", "LATIN CAPITAL LETTER SHARP S"),
    #
    # Major world scripts - Arabic
    (0x0621, "hamza-ar", "ARABIC LETTER HAMZA"),
    (0x0622, "alefMaddaAbove-ar", "ARABIC LETTER ALEF WITH MADDA ABOVE"),
    (0x0623, "alefHamzaAbove-ar", "ARABIC LETTER ALEF WITH HAMZA ABOVE"),
    (0x0624, "wawHamzaAbove-ar", "ARABIC LETTER WAW WITH HAMZA ABOVE"),
    (0x0625, "alefHamzaBelow-ar", "ARABIC LETTER ALEF WITH HAMZA BELOW"),
    (0x0626, "yehHamzaAbove-ar", "ARABIC LETTER YEH WITH HAMZA ABOVE"),
    (0x0627, "alef-ar", "ARABIC LETTER ALEF"),
    (0x0628, "beh-ar", "ARABIC LETTER BEH"),
    (0x0629, "tehMarbuta-ar", "ARABIC LETTER TEH MARBUTA"),
    (0x062D, "hah-ar", "ARABIC LETTER HAH"),
    (0x0633, "seen-ar", "ARABIC LETTER SEEN"),
    (0x0639, "ain-ar", "ARABIC LETTER AIN"),
    (0x0642, "qaf-ar", "ARABIC LETTER QAF"),
    (0x0644, "lam-ar", "ARABIC LETTER LAM"),
    (0x0646, "noon-ar", "ARABIC LETTER NOON"),
    (0x0647, "heh-ar", "ARABIC LETTER HEH"),
    (0x064A, "yeh-ar", "ARABIC LETTER YEH"),
    #
    # Major world scripts - Greek
    (0x0391, "Alpha-gr", "GREEK CAPITAL LETTER ALPHA"),
    (0x0392, "Beta-gr", "GREEK CAPITAL LETTER BETA"),
    (0x0393, "Gamma-gr", "GREEK CAPITAL LETTER GAMMA"),
    (0x03B1, "alpha-gr", "GREEK SMALL LETTER ALPHA"),
    (0x03B2, "beta-gr", "GREEK SMALL LETTER BETA"),
    (0x03C9, "omega-gr", "GREEK SMALL LETTER OMEGA"),
    #
    # Major world scripts - Cyrillic
    (0x0410, "A-cyr", "CYRILLIC CAPITAL LETTER A"),
    (0x0411, "Be-cyr", "CYRILLIC CAPITAL LETTER BE"),
    (0x0412, "Ve-cyr", "CYRILLIC CAPITAL LETTER VE"),
    (0x0430, "a-cyr", "CYRILLIC SMALL LETTER A"),
    (0x0431, "be-cyr", "CYRILLIC SMALL LETTER BE"),
    (0x0432, "ve-cyr", "CYRILLIC SMALL LETTER VE"),
    #
    # Major world scripts - Hebrew
    (0x05D0, "alef-heb", "HEBREW LETTER ALEF"),
    (0x05D1, "bet-heb", "HEBREW LETTER BET"),
    (0x05D2, "gimel-heb", "HEBREW LETTER GIMEL"),
    #
    # Major world scripts - Armenian
    (0x0531, "Ayb-arm", "ARMENIAN CAPITAL LETTER AYB"),
    (0x0532, "Ben-arm", "ARMENIAN CAPITAL LETTER BEN"),
    (0x0561, "ayb-arm", "ARMENIAN SMALL LETTER AYB"),
    #
    # Indic scripts - Devanagari
    (0x0905, "a-dev", "DEVANAGARI LETTER A"),
    (0x0906, "aa-dev", "DEVANAGARI LETTER AA"),
    (0x0915, "ka-dev", "DEVANAGARI LETTER KA"),
    #
    # Indic scripts - Bengali
    (0x0985, "a-ben", "BENGALI LETTER A"),
    (0x0986, "aa-ben", "BENGALI LETTER AA"),
    (0x0995, "ka-ben", "BENGALI LETTER KA"),
    #
    # Indic scripts - Gurmukhi
    (0x0A05, "a-gur", "GURMUKHI LETTER A"),
    (0x0A06, "aa-gur", "GURMUKHI LETTER AA"),
    (0x0A15, "ka-gur", "GURMUKHI LETTER KA"),
    #
    # Indic scripts - Gujarati
    (0x0A85, "a-guj", "GUJARATI LETTER A"),
    (0x0A86, "aa-guj", "GUJARATI LETTER AA"),
    (0x0A95, "ka-guj", "GUJARATI LETTER KA"),
    #
    # Indic scripts - Tamil
    (0x0B85, "a-tam", "TAMIL LETTER A"),
    (0x0B86, "aa-tam", "TAMIL LETTER AA"),
    (0x0B95, "ka-tam", "TAMIL LETTER KA"),
    #
    # Indic scripts - Telugu
    (0x0C05, "a-tel", "TELUGU LETTER A"),
    (0x0C06, "aa-tel", "TELUGU LETTER AA"),
    (0x0C15, "ka-tel", "TELUGU LETTER KA"),
    #
    # Indic scripts - Kannada
    (0x0C85, "a-kan", "KANNADA LETTER A"),
    (0x0C86, "aa-kan", "KANNADA LETTER AA"),
    (0x0C95, "ka-kan", "KANNADA LETTER KA"),
    #
    # Indic scripts - Malayalam
    (0x0D05, "a-mal", "MALAYALAM LETTER A"),
    (0x0D06, "aa-mal", "MALAYALAM LETTER AA"),
    (0x0D15, "ka-mal", "MALAYALAM LETTER KA"),
    #
    # Indic scripts - Sinhala
    (0x0D85, "ayanna-sin", "SINHALA LETTER AYANNA"),
    (0x0D86, "aayanna-sin", "SINHALA LETTER AAYANNA"),
    (0x0D9A, "alpapraanaKayanna-sin", "SINHALA LETTER ALPAPRAANA KAYANNA"),
    #
    # Southeast Asian scripts - Thai
    (0x0E01, "koKai-th", "THAI CHARACTER KO KAI"),
    (0x0E02, "khoKhai-th", "THAI CHARACTER KHO KHAI"),
    (0x0E03, "khoKhuat-th", "THAI CHARACTER KHO KHUAT"),
    #
    # Southeast Asian scripts - Lao
    (0x0E81, "ko-lao", "LAO LETTER KO"),
    (0x0E82, "kho-lao", "LAO LETTER KHO SUNG"),
    (0x0E84, "khoTam-lao", "LAO LETTER KHO TAM"),
    #
    # Southeast Asian scripts - Myanmar
    (0x1000, "ka-mya", "MYANMAR LETTER KA"),
    (0x1001, "kha-mya", "MYANMAR LETTER KHA"),
    (0x1002, "ga-mya", "MYANMAR LETTER GA"),
    #
    # Southeast Asian scripts - Khmer
    (0x1780, "ka-khm", "KHMER LETTER KA"),
    (0x1781, "kha-khm", "KHMER LETTER KHA"),
    (0x1782, "ko-khm", "KHMER LETTER KO"),
    #
    # Tibetan & Himalayan - Tibetan
    (0x0F40, "ka-tib", "TIBETAN LETTER KA"),
    (0x0F41, "kha-tib", "TIBETAN LETTER KHA"),
    (0x0F42, "ga-tib", "TIBETAN LETTER GA"),
    #
    # East Asian scripts - Hangul
    (0x1100, "kiyeokCho-ko", "HANGUL CHOSEONG KIYEOK"),
    (0x1101, "ssangkiyeokCho-ko", "HANGUL CHOSEONG SSANGKIYEOK"),
    (0x1102, "nieunCho-ko", "HANGUL CHOSEONG NIEUN"),
    (0x11A8, "kiyeokJong-ko", "HANGUL JONGSEONG KIYEOK"),
    (0x3131, "kiyeok-ko", "HANGUL LETTER KIYEOK"),
    #
    # East Asian scripts - Hiragana
    (0x3041, "smallA-hira", "HIRAGANA LETTER SMALL A"),
    (0x3042, "a-hira", "HIRAGANA LETTER A"),
    (0x3044, "i-hira", "HIRAGANA LETTER I"),
    #
    # East Asian scripts - Katakana
    (0x30A1, "smallA-kata", "KATAKANA LETTER SMALL A"),
    (0x30A2, "a-kata", "KATAKANA LETTER A"),
    (0x30A4, "i-kata", "KATAKANA LETTER I"),
    #
    # East Asian scripts - Bopomofo
    (0x3105, "b-bop", "BOPOMOFO LETTER B"),
    (0x3106, "p-bop", "BOPOMOFO LETTER P"),
    (0x3107, "m-bop", "BOPOMOFO LETTER M"),
    #
    # East Asian scripts - Yi
    (0xA000, "itSyllable-yi", "YI SYLLABLE IT"),
    (0xA001, "ixSyllable-yi", "YI SYLLABLE IX"),
    (0xA002, "iSyllable-yi", "YI SYLLABLE I"),
    #
    # African scripts - Ethiopic
    (0x1200, "haSyllable-eth", "ETHIOPIC SYLLABLE HA"),
    (0x1201, "huSyllable-eth", "ETHIOPIC SYLLABLE HU"),
    (0x1202, "hiSyllable-eth", "ETHIOPIC SYLLABLE HI"),
    #
    # African scripts - Vai
    (0xA500, "eeSyllable-vai", "VAI SYLLABLE EE"),
    (0xA501, "eenSyllable-vai", "VAI SYLLABLE EEN"),
    (0xA502, "heeSyllable-vai", "VAI SYLLABLE HEE"),
    #
    # African scripts - Bamum
    (0xA6A0, "a-bam", "BAMUM LETTER A"),
    (0xA6A1, "ka-bam", "BAMUM LETTER KA"),
    (0xA6A2, "u-bam", "BAMUM LETTER U"),
    #
    # African scripts - NKo
    (0x07CA, "a-nko", "NKO LETTER A"),
    (0x07CB, "ee-nko", "NKO LETTER EE"),
    (0x07CC, "i-nko", "NKO LETTER I"),
    #
    # American scripts - Cherokee
    (0x13A0, "aLetter-chr", "CHEROKEE LETTER A"),
    (0x13A1, "eLetter-chr", "CHEROKEE LETTER E"),
    (0x13A2, "iLetter-chr", "CHEROKEE LETTER I"),
    #
    # Historical scripts - Georgian
    (0x10A0, "An-geo", "GEORGIAN CAPITAL LETTER AN"),
    (0x10A1, "Ban-geo", "GEORGIAN CAPITAL LETTER BAN"),
    (0x10D0, "anLetter-geo", "GEORGIAN LETTER AN"),
    #
    # Historical scripts - Glagolitic
    (0x2C00, "Azu-glag", "GLAGOLITIC CAPITAL LETTER AZU"),
    (0x2C01, "Buky-glag", "GLAGOLITIC CAPITAL LETTER BUKY"),
    (0x2C30, "azu-glag", "GLAGOLITIC SMALL LETTER AZU"),
    #
    # Historical scripts - Coptic
    (0x2C80, "Alfa-cop", "COPTIC CAPITAL LETTER ALFA"),
    (0x2C81, "alfa-cop", "COPTIC SMALL LETTER ALFA"),
    (0x2C82, "Vida-cop", "COPTIC CAPITAL LETTER VIDA"),
    #
    # Historical scripts - Ogham
    (0x1681, "beith-ogh", "OGHAM LETTER BEITH"),
    (0x1682, "luis-ogh", "OGHAM LETTER LUIS"),
    (0x1683, "fearn-ogh", "OGHAM LETTER FEARN"),
    #
    # Historical scripts - Runic
    (0x16A0, "fehuFeohFe-run", "RUNIC LETTER FEHU FEOH FE F"),
    (0x16A1, "v-run", "RUNIC LETTER V"),
    (0x16A2, "uruzUr-run", "RUNIC LETTER URUZ UR U"),
    (0x16A9, "os-run", "RUNIC LETTER OS O"),
    (0x16AC, "longBranchOss-run", "RUNIC LETTER LONG-BRANCH-OSS O"),
    (0x16AE, "o-run", "RUNIC LETTER O"),
    #
    # Ancient scripts - Cuneiform
    (0x12000, "a-xsux", "CUNEIFORM SIGN A"),
    (0x12001, "aTimesA-xsux", "CUNEIFORM SIGN A TIMES A"),
    (0x12002, "aTimesBad-xsux", "CUNEIFORM SIGN A TIMES BAD"),
    (0x12157, "ka-xsux", "CUNEIFORM SIGN KA"),
    (0x12158, "kaTimesA-xsux", "CUNEIFORM SIGN KA TIMES A"),
    (0x120B7, "ga2-xsux", "CUNEIFORM SIGN GA2"),
    (
        0x120B8,
        "ga2TimesAPlusDaPlusHa-xsux",
        "CUNEIFORM SIGN GA2 TIMES A PLUS DA PLUS HA",
    ),
    #
    # Combining marks - Latin script
    (0x0300, "graveCombining", "COMBINING GRAVE ACCENT"),
    (0x0301, "acuteCombining", "COMBINING ACUTE ACCENT"),
    (0x0302, "circumflexCombining", "COMBINING CIRCUMFLEX ACCENT"),
    (0x0303, "tildeCombining", "COMBINING TILDE"),
    (0x0304, "macronCombining", "COMBINING MACRON"),
    (0x0308, "diaeresisCombining", "COMBINING DIAERESIS"),
    (0x030A, "ringAboveCombining", "COMBINING RING ABOVE"),
    (0x030C, "caronCombining", "COMBINING CARON"),
    (0x0327, "cedillaCombining", "COMBINING CEDILLA"),
    (0x0328, "ogonekCombining", "COMBINING OGONEK"),
    #
    # Combining marks - Arabic script
    (0x064B, "fathaTanween-ar", "ARABIC FATHATAN"),
    (0x064C, "dammaTanween-ar", "ARABIC DAMMATAN"),
    (0x064D, "kasraTanween-ar", "ARABIC KASRATAN"),
    (0x064E, "fatha-ar", "ARABIC FATHA"),
    (0x064F, "damma-ar", "ARABIC DAMMA"),
    (0x0650, "kasra-ar", "ARABIC KASRA"),
    (0x0651, "shadda-ar", "ARABIC SHADDA"),
    (0x0652, "sukun-ar", "ARABIC SUKUN"),
    (0x0653, "maddahAbove-ar", "ARABIC MADDAH ABOVE"),
    (0x0654, "hamzaAbove-ar", "ARABIC HAMZA ABOVE"),
    #
    # Combining marks - Devanagari script
    (0x0901, "candrabindu-dev", "DEVANAGARI SIGN CANDRABINDU"),
    (0x0902, "anusvara-dev", "DEVANAGARI SIGN ANUSVARA"),
    (0x0903, "visarga-dev", "DEVANAGARI SIGN VISARGA"),
    #
    # Symbols (no script)
    (0x0024, "dollarSign", "DOLLAR SIGN"),
    (0x0025, "percentSign", "PERCENT SIGN"),
    (0x0026, "ampersand", "AMPERSAND"),
    (0x002A, "asterisk", "ASTERISK"),
    (0x002B, "plusSign", "PLUS SIGN"),
    (0x003D, "equalsSign", "EQUALS SIGN"),
    (0x0040, "commercialAt", "COMMERCIAL AT"),
    #
    # Recently fixed duplicates - Runic DOTTED variants
    (0x16C0, "dottedN-run", "RUNIC LETTER DOTTED-N"),
    (0x16D4, "dottedP-run", "RUNIC LETTER DOTTED-P"),
    (0x16DB, "dottedL-run", "RUNIC LETTER DOTTED-L"),
    #
    # Recently fixed duplicates - Small Capital I variants
    (0x026A, "SmallCapitalI-lat", "LATIN LETTER SMALL CAPITAL I"),
    (0xA7AE, "CapitalSmallCapitalI-lat", "LATIN CAPITAL LETTER SMALL CAPITAL I"),
    #
    # Recently fixed duplicates - Ethiopic syllable TO/THE
    (0x1276, "toSyllable-eth", "ETHIOPIC SYLLABLE TO"),
    (0x1325, "theSyllable-eth", "ETHIOPIC SYLLABLE THE"),
    #
    # Recently fixed duplicates - Canadian SYLLABICS
    (0x1450, "toSyllabics-can", "CANADIAN SYLLABICS TO"),
    (0x155E, "theSyllabics-can", "CANADIAN SYLLABICS THE"),
    #
    # Recently fixed duplicates - TAI YO LETTER vs SIGN
    (0x1E6E2, "yoUe-tai", "TAI YO LETTER UE"),
    (0x1E6E3, "yoSignUe-tai", "TAI YO SIGN UE"),
    #
    # Recently fixed duplicates - Greek SYMBOL variants
    (0x03D0, "betaSymbol-gr", "GREEK BETA SYMBOL"),
    (0x03D1, "thetaSymbol-gr", "GREEK THETA SYMBOL"),
    (0x03D5, "phiSymbol-gr", "GREEK PHI SYMBOL"),
    (0x03D6, "piSymbol-gr", "GREEK PI SYMBOL"),
    #
    # Recently fixed duplicates - Hebrew ACCENT vs PUNCTUATION
    (0x059C, "gereshAccent-heb", "HEBREW ACCENT GERESH"),
    (0x05F3, "gereshPunctuation-heb", "HEBREW PUNCTUATION GERESH"),
    (0x059D, "gereshMuqdamAccent-heb", "HEBREW ACCENT GERESH MUQDAM"),
    (0x05F4, "gershayimPunctuation-heb", "HEBREW PUNCTUATION GERSHAYIM"),
    #
    # Recently fixed duplicates - Arabic SMALL variants
    (0x0618, "smallFatha-ar", "ARABIC SMALL FATHA"),
    (0x0619, "smallDamma-ar", "ARABIC SMALL DAMMA"),
    #
    # Recently fixed duplicates - Yi SYLLABLE vs RADICAL
    (0xA490, "radicalQot-yi", "YI RADICAL QOT"),
    #
    # Recently fixed duplicates - Brahmi NUMBER vs DIGIT
    (0x11052, "numberOne-brah", "BRAHMI NUMBER ONE"),
    (0x11066, "digitZero-brah", "BRAHMI DIGIT ZERO"),
    #
    # Recently fixed duplicates - Logical operators (kept AND/OR)
    (0x2A53, "doubleLogicalAnd", "DOUBLE LOGICAL AND"),
    (0x2A54, "doubleLogicalOr", "DOUBLE LOGICAL OR"),
    #
    # Recently fixed duplicates - Parenthesized variants
    (0x2474, "parenthesizedDigitOne", "PARENTHESIZED DIGIT ONE"),
    (0x3220, "parenthesizedIdeographOne", "PARENTHESIZED IDEOGRAPH ONE"),
    #
    # Recently fixed duplicates - Case-aware LETTER preservation
    #
    # Latin: LETTER vs SMALL LETTER (caseless variants move LETTER to end)
    (0x0242, "glottalStop-lat", "LATIN SMALL LETTER GLOTTAL STOP"),
    (0x0294, "glottalStopLetter-lat", "LATIN LETTER GLOTTAL STOP"),
    #
    # Greek: LETTER vs SMALL LETTER (caseless variants move LETTER to end)
    (0x03D9, "archaicKoppa-gr", "GREEK SMALL LETTER ARCHAIC KOPPA"),
    (0x03D8, "archaicKoppaLetter-gr", "GREEK LETTER ARCHAIC KOPPA"),
    #
    # Georgian: LETTER vs CAPITAL/SMALL (caseless move LETTER to end)
    (0x2D00, "an-geo", "GEORGIAN SMALL LETTER AN"),
    (0x10D0, "anLetter-geo", "GEORGIAN LETTER AN"),
    (0x10A0, "An-geo", "GEORGIAN CAPITAL LETTER AN"),
    #
    # Cherokee: LETTER vs SMALL LETTER (caseless variants move LETTER to end)
    (0xAB70, "a-chr", "CHEROKEE SMALL LETTER A"),
    (0x13A0, "aLetter-chr", "CHEROKEE LETTER A"),
    (0x13F9, "yi-chr", "CHEROKEE SMALL LETTER YI"),
    (0x13F1, "yiLetter-chr", "CHEROKEE LETTER YI"),
    #
    # Limbu: LETTER vs SMALL LETTER (caseless variants move LETTER to end)
    (0x1930, "ka-limb", "LIMBU SMALL LETTER KA"),
    (0x1901, "kaLetter-limb", "LIMBU LETTER KA"),
    (0x1931, "nga-limb", "LIMBU SMALL LETTER NGA"),
    (0x1905, "ngaLetter-limb", "LIMBU LETTER NGA"),
    #
    # Phags-pa: LETTER vs SMALL LETTER (caseless variants move LETTER to end)
    (0xA856, "a-phag", "PHAGS-PA LETTER SMALL A"),
    (0xA85D, "aLetter-phag", "PHAGS-PA LETTER A"),
    #
    # Hiragana/Katakana: SMALL is size variant, not case (keep SMALL)
    (0x3041, "smallA-hira", "HIRAGANA LETTER SMALL A"),
    (0x3042, "a-hira", "HIRAGANA LETTER A"),
    (0x3043, "smallI-hira", "HIRAGANA LETTER SMALL I"),
    (0x3044, "i-hira", "HIRAGANA LETTER I"),
    (0x30A1, "smallA-kata", "KATAKANA LETTER SMALL A"),
    (0x30A2, "a-kata", "KATAKANA LETTER A"),
    #
    # Non-script SIGN preservation (COLON vs COLON SIGN, etc.)
    (0x003A, "colon", "COLON"),
    (0x20A1, "colonSign", "COLON SIGN"),
]


class TestGlyphNameGeneration(unittest.TestCase):
    """Test cases for glyph name transformation."""

    def test_all_glyph_names(self):
        """Test all glyph name transformations with data validation."""
        for codepoint, expected_result, expected_name in TEST_CASES:
            with self.subTest(codepoint=f"U+{codepoint:04X}"):
                # Verify the Unicode name matches our test data
                ucd = youseedee.ucd_data(codepoint)
                self.assertIsNotNone(ucd, f"No UCD data for U+{codepoint:04X}")
                self.assertIn("Name", ucd, f"No name in UCD for U+{codepoint:04X}")

                actual_name = ucd["Name"]
                self.assertEqual(
                    actual_name,
                    expected_name,
                    f"Unicode name mismatch for U+{codepoint:04X}: "
                    f"expected '{expected_name}', got '{actual_name}'",
                )

                # Test the glyph name generation
                result = glyph_data_for_unicode(codepoint)
                self.assertEqual(
                    result,
                    expected_result,
                    f"U+{codepoint:04X} {expected_name}: "
                    f"expected '{expected_result}', got '{result}'",
                )


if __name__ == "__main__":
    unittest.main()
