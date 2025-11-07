"""Unit tests for glyph name generation."""

import unittest
import youseedee
from context_glyphdata import glyph_data_for_unicode


# Test data: (codepoint, expected_result, unicode_name)
# Organized by script categories matching SCRIPT_SUFFIXES
TEST_CASES = [
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
    # Major world scripts - Greek
    (0x0391, "Alpha-gr", "GREEK CAPITAL LETTER ALPHA"),
    (0x0392, "Beta-gr", "GREEK CAPITAL LETTER BETA"),
    (0x0393, "Gamma-gr", "GREEK CAPITAL LETTER GAMMA"),
    (0x03B1, "alpha-gr", "GREEK SMALL LETTER ALPHA"),
    (0x03B2, "beta-gr", "GREEK SMALL LETTER BETA"),
    (0x03C9, "omega-gr", "GREEK SMALL LETTER OMEGA"),
    # Major world scripts - Cyrillic
    (0x0410, "A-cyr", "CYRILLIC CAPITAL LETTER A"),
    (0x0411, "Be-cyr", "CYRILLIC CAPITAL LETTER BE"),
    (0x0412, "Ve-cyr", "CYRILLIC CAPITAL LETTER VE"),
    (0x0430, "a-cyr", "CYRILLIC SMALL LETTER A"),
    (0x0431, "be-cyr", "CYRILLIC SMALL LETTER BE"),
    (0x0432, "ve-cyr", "CYRILLIC SMALL LETTER VE"),
    # Major world scripts - Hebrew
    (0x05D0, "alef-he", "HEBREW LETTER ALEF"),
    (0x05D1, "bet-he", "HEBREW LETTER BET"),
    (0x05D2, "gimel-he", "HEBREW LETTER GIMEL"),
    # Major world scripts - Armenian
    (0x0531, "Ayb-arm", "ARMENIAN CAPITAL LETTER AYB"),
    (0x0532, "Ben-arm", "ARMENIAN CAPITAL LETTER BEN"),
    (0x0561, "ayb-arm", "ARMENIAN SMALL LETTER AYB"),
    # Indic scripts - Devanagari
    (0x0905, "a-dev", "DEVANAGARI LETTER A"),
    (0x0906, "aa-dev", "DEVANAGARI LETTER AA"),
    (0x0915, "ka-dev", "DEVANAGARI LETTER KA"),
    # Indic scripts - Bengali
    (0x0985, "a-bn", "BENGALI LETTER A"),
    (0x0986, "aa-bn", "BENGALI LETTER AA"),
    (0x0995, "ka-bn", "BENGALI LETTER KA"),
    # Indic scripts - Gurmukhi
    (0x0A05, "a-gu", "GURMUKHI LETTER A"),
    (0x0A06, "aa-gu", "GURMUKHI LETTER AA"),
    (0x0A15, "ka-gu", "GURMUKHI LETTER KA"),
    # Indic scripts - Gujarati
    (0x0A85, "a-gj", "GUJARATI LETTER A"),
    (0x0A86, "aa-gj", "GUJARATI LETTER AA"),
    (0x0A95, "ka-gj", "GUJARATI LETTER KA"),
    # Indic scripts - Tamil
    (0x0B85, "a-ta", "TAMIL LETTER A"),
    (0x0B86, "aa-ta", "TAMIL LETTER AA"),
    (0x0B95, "ka-ta", "TAMIL LETTER KA"),
    # Indic scripts - Telugu
    (0x0C05, "a-te", "TELUGU LETTER A"),
    (0x0C06, "aa-te", "TELUGU LETTER AA"),
    (0x0C15, "ka-te", "TELUGU LETTER KA"),
    # Indic scripts - Kannada
    (0x0C85, "a-kn", "KANNADA LETTER A"),
    (0x0C86, "aa-kn", "KANNADA LETTER AA"),
    (0x0C95, "ka-kn", "KANNADA LETTER KA"),
    # Indic scripts - Malayalam
    (0x0D05, "a-ml", "MALAYALAM LETTER A"),
    (0x0D06, "aa-ml", "MALAYALAM LETTER AA"),
    (0x0D15, "ka-ml", "MALAYALAM LETTER KA"),
    # Indic scripts - Sinhala
    (0x0D85, "ayanna-si", "SINHALA LETTER AYANNA"),
    (0x0D86, "aayanna-si", "SINHALA LETTER AAYANNA"),
    (0x0D9A, "alpapraanaKayanna-si", "SINHALA LETTER ALPAPRAANA KAYANNA"),
    # Southeast Asian scripts - Thai
    (0x0E01, "koKai-th", "THAI CHARACTER KO KAI"),
    (0x0E02, "khoKhai-th", "THAI CHARACTER KHO KHAI"),
    (0x0E03, "khoKhuat-th", "THAI CHARACTER KHO KHUAT"),
    # Southeast Asian scripts - Lao
    (0x0E81, "ko-lo", "LAO LETTER KO"),
    (0x0E82, "kho-lo", "LAO LETTER KHO SUNG"),
    (0x0E84, "khoTam-lo", "LAO LETTER KHO TAM"),
    # Southeast Asian scripts - Myanmar
    (0x1000, "ka-my", "MYANMAR LETTER KA"),
    (0x1001, "kha-my", "MYANMAR LETTER KHA"),
    (0x1002, "ga-my", "MYANMAR LETTER GA"),
    # Southeast Asian scripts - Khmer
    (0x1780, "ka-km", "KHMER LETTER KA"),
    (0x1781, "kha-km", "KHMER LETTER KHA"),
    (0x1782, "ko-km", "KHMER LETTER KO"),
    # Tibetan & Himalayan - Tibetan
    (0x0F40, "ka-ti", "TIBETAN LETTER KA"),
    (0x0F41, "kha-ti", "TIBETAN LETTER KHA"),
    (0x0F42, "ga-ti", "TIBETAN LETTER GA"),
    # East Asian scripts - Hangul
    (0x1100, "kiyeok-ko", "HANGUL CHOSEONG KIYEOK"),
    (0x1101, "ssangkiyeok-ko", "HANGUL CHOSEONG SSANGKIYEOK"),
    (0x1102, "nieun-ko", "HANGUL CHOSEONG NIEUN"),
    # East Asian scripts - Hiragana
    (0x3041, "a-hira", "HIRAGANA LETTER SMALL A"),
    (0x3042, "a-hira", "HIRAGANA LETTER A"),
    (0x3044, "i-hira", "HIRAGANA LETTER I"),
    # East Asian scripts - Katakana
    (0x30A1, "a-kata", "KATAKANA LETTER SMALL A"),
    (0x30A2, "a-kata", "KATAKANA LETTER A"),
    (0x30A4, "i-kata", "KATAKANA LETTER I"),
    # East Asian scripts - Bopomofo
    (0x3105, "b-bo", "BOPOMOFO LETTER B"),
    (0x3106, "p-bo", "BOPOMOFO LETTER P"),
    (0x3107, "m-bo", "BOPOMOFO LETTER M"),
    # East Asian scripts - Yi
    (0xA000, "it-yi", "YI SYLLABLE IT"),
    (0xA001, "ix-yi", "YI SYLLABLE IX"),
    (0xA002, "i-yi", "YI SYLLABLE I"),
    # African scripts - Ethiopic
    (0x1200, "ha-et", "ETHIOPIC SYLLABLE HA"),
    (0x1201, "hu-et", "ETHIOPIC SYLLABLE HU"),
    (0x1202, "hi-et", "ETHIOPIC SYLLABLE HI"),
    # African scripts - Vai
    (0xA500, "ee-vai", "VAI SYLLABLE EE"),
    (0xA501, "een-vai", "VAI SYLLABLE EEN"),
    (0xA502, "hee-vai", "VAI SYLLABLE HEE"),
    # African scripts - Bamum
    (0xA6A0, "a-bam", "BAMUM LETTER A"),
    (0xA6A1, "ka-bam", "BAMUM LETTER KA"),
    (0xA6A2, "u-bam", "BAMUM LETTER U"),
    # African scripts - NKo
    (0x07CA, "a-nko", "NKO LETTER A"),
    (0x07CB, "ee-nko", "NKO LETTER EE"),
    (0x07CC, "i-nko", "NKO LETTER I"),
    # American scripts - Cherokee
    (0x13A0, "a-chr", "CHEROKEE LETTER A"),
    (0x13A1, "e-chr", "CHEROKEE LETTER E"),
    (0x13A2, "i-chr", "CHEROKEE LETTER I"),
    # Historical scripts - Georgian
    (0x10A0, "An-geo", "GEORGIAN CAPITAL LETTER AN"),
    (0x10A1, "Ban-geo", "GEORGIAN CAPITAL LETTER BAN"),
    (0x10D0, "an-geo", "GEORGIAN LETTER AN"),
    # Historical scripts - Glagolitic
    (0x2C00, "Azu-glag", "GLAGOLITIC CAPITAL LETTER AZU"),
    (0x2C01, "Buky-glag", "GLAGOLITIC CAPITAL LETTER BUKY"),
    (0x2C30, "azu-glag", "GLAGOLITIC SMALL LETTER AZU"),
    # Historical scripts - Coptic
    (0x2C80, "Alfa-cop", "COPTIC CAPITAL LETTER ALFA"),
    (0x2C81, "alfa-cop", "COPTIC SMALL LETTER ALFA"),
    (0x2C82, "Vida-cop", "COPTIC CAPITAL LETTER VIDA"),
    # Historical scripts - Ogham
    (0x1681, "beith-og", "OGHAM LETTER BEITH"),
    (0x1682, "luis-og", "OGHAM LETTER LUIS"),
    (0x1683, "fearn-og", "OGHAM LETTER FEARN"),
    # Historical scripts - Runic
    (0x16A0, "f-ru", "RUNIC LETTER FEHU FEOH FE F"),
    (0x16A1, "v-ru", "RUNIC LETTER V"),
    (0x16A2, "u-ru", "RUNIC LETTER URUZ UR U"),
    # Ancient scripts - Cuneiform
    (0x12000, "a-xsux", "CUNEIFORM SIGN A"),
    (0x12001, "a-xsux", "CUNEIFORM SIGN A TIMES A"),
    (0x12002, "a-xsux", "CUNEIFORM SIGN A TIMES BAD"),
    (0x12002, "a-xsux", "CUNEIFORM SIGN A TIMES BAD"),
    # Symbols (no script)
    (0x0024, "dollar", "DOLLAR SIGN"),
    (0x0025, "percent", "PERCENT SIGN"),
    (0x0026, "ampersand", "AMPERSAND"),
    (0x002A, "asterisk", "ASTERISK"),
    (0x002B, "plus", "PLUS SIGN"),
    (0x003D, "equals", "EQUALS SIGN"),
    (0x0040, "commercialAt", "COMMERCIAL AT"),
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
