"""Unit tests for glyph name generation."""

import unittest
from context_glyphdata import glyph_data_for_unicode


class TestGlyphNameGeneration(unittest.TestCase):
    """Test cases for glyph name transformation."""

    def test_arabic_letter_alef(self):
        """Test: ARABIC LETTER ALEF -> alef-ar"""
        # U+0627 ARABIC LETTER ALEF
        result = glyph_data_for_unicode(0x0627)
        self.assertEqual(result, "alef-ar")

    def test_arabic_letter_beh(self):
        """Test: ARABIC LETTER BEH -> beh-ar"""
        # U+0628 ARABIC LETTER BEH
        result = glyph_data_for_unicode(0x0628)
        self.assertEqual(result, "beh-ar")

    def test_latin_capital_letter_a(self):
        """Test: LATIN CAPITAL LETTER A -> A-lat"""
        # U+0041 LATIN CAPITAL LETTER A
        result = glyph_data_for_unicode(0x0041)
        self.assertEqual(result, "A-lat")

    def test_greek_letter(self):
        """Test: GREEK CAPITAL LETTER ALPHA -> Alpha-gr"""
        # U+0391 GREEK CAPITAL LETTER ALPHA
        result = glyph_data_for_unicode(0x0391)
        self.assertEqual(result, "Alpha-gr")

    def test_cyrillic_letter(self):
        """Test: CYRILLIC CAPITAL LETTER A -> A-cyr"""
        # U+0410 CYRILLIC CAPITAL LETTER A
        result = glyph_data_for_unicode(0x0410)
        self.assertEqual(result, "A-cyr")

    def test_hebrew_letter(self):
        """Test: HEBREW LETTER ALEF -> alef-he"""
        # U+05D0 HEBREW LETTER ALEF
        result = glyph_data_for_unicode(0x05D0)
        self.assertEqual(result, "alef-he")

    def test_thai_letter(self):
        """Test: THAI CHARACTER KO KAI -> koKai-th"""
        # U+0E01 THAI CHARACTER KO KAI
        result = glyph_data_for_unicode(0x0E01)
        # Note: THAI uses "CHARACTER" not "LETTER"
        self.assertEqual(result, "koKai-th")

    def test_devanagari_letter(self):
        """Test: DEVANAGARI LETTER KA -> ka-dev"""
        # U+0915 DEVANAGARI LETTER KA
        result = glyph_data_for_unicode(0x0915)
        self.assertEqual(result, "ka-dev")

    def test_no_script_fallback(self):
        """Test characters without recognized scripts use fallback"""
        # U+0020 SPACE (no script in name)
        result = glyph_data_for_unicode(0x0020)
        # Should return some form of name, exact format may vary
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    # Lowercase letter tests
    def test_latin_small_letter_a(self):
        """Test: LATIN SMALL LETTER A -> a-lat"""
        # U+0061 LATIN SMALL LETTER A
        result = glyph_data_for_unicode(0x0061)
        self.assertEqual(result, "a-lat")

    def test_latin_small_letter_z(self):
        """Test: LATIN SMALL LETTER Z -> z-lat"""
        # U+007A LATIN SMALL LETTER Z
        result = glyph_data_for_unicode(0x007A)
        self.assertEqual(result, "z-lat")

    def test_greek_small_letter_alpha(self):
        """Test: GREEK SMALL LETTER ALPHA -> alpha-gr"""
        # U+03B1 GREEK SMALL LETTER ALPHA
        result = glyph_data_for_unicode(0x03B1)
        self.assertEqual(result, "alpha-gr")

    def test_greek_small_letter_omega(self):
        """Test: GREEK SMALL LETTER OMEGA -> omega-gr"""
        # U+03C9 GREEK SMALL LETTER OMEGA
        result = glyph_data_for_unicode(0x03C9)
        self.assertEqual(result, "omega-gr")

    def test_cyrillic_small_letter_a(self):
        """Test: CYRILLIC SMALL LETTER A -> a-cyr"""
        # U+0430 CYRILLIC SMALL LETTER A
        result = glyph_data_for_unicode(0x0430)
        self.assertEqual(result, "a-cyr")

    # Symbol tests
    def test_plus_sign(self):
        """Test: PLUS SIGN -> plus"""
        # U+002B PLUS SIGN
        result = glyph_data_for_unicode(0x002B)
        self.assertEqual(result, "plus")

    def test_equals_sign(self):
        """Test: EQUALS SIGN -> equals"""
        # U+003D EQUALS SIGN
        result = glyph_data_for_unicode(0x003D)
        self.assertEqual(result, "equals")

    def test_asterisk(self):
        """Test: ASTERISK -> asterisk"""
        # U+002A ASTERISK
        result = glyph_data_for_unicode(0x002A)
        self.assertEqual(result, "asterisk")

    def test_ampersand(self):
        """Test: AMPERSAND -> ampersand"""
        # U+0026 AMPERSAND
        result = glyph_data_for_unicode(0x0026)
        self.assertEqual(result, "ampersand")

    def test_at_sign(self):
        """Test: COMMERCIAL AT -> commercial"""
        # U+0040 COMMERCIAL AT
        result = glyph_data_for_unicode(0x0040)
        self.assertEqual(result, "commercialAt")

    def test_dollar_sign(self):
        """Test: DOLLAR SIGN -> dollar"""
        # U+0024 DOLLAR SIGN
        result = glyph_data_for_unicode(0x0024)
        self.assertEqual(result, "dollar")

    def test_percent_sign(self):
        """Test: PERCENT SIGN -> percent"""
        # U+0025 PERCENT SIGN
        result = glyph_data_for_unicode(0x0025)
        self.assertEqual(result, "percent")

    # Multi-part Arabic character tests
    def test_arabic_letter_teh_marbuta(self):
        """Test: ARABIC LETTER TEH MARBUTA -> tehMarbuta-ar"""
        # U+0629 ARABIC LETTER TEH MARBUTA
        result = glyph_data_for_unicode(0x0629)
        self.assertEqual(result, "tehMarbuta-ar")

    def test_arabic_letter_hah(self):
        """Test: ARABIC LETTER HAH -> hah-ar"""
        # U+062D ARABIC LETTER HAH
        result = glyph_data_for_unicode(0x062D)
        self.assertEqual(result, "hah-ar")

    def test_arabic_letter_seen(self):
        """Test: ARABIC LETTER SEEN -> seen-ar"""
        # U+0633 ARABIC LETTER SEEN
        result = glyph_data_for_unicode(0x0633)
        self.assertEqual(result, "seen-ar")

    def test_arabic_letter_ain(self):
        """Test: ARABIC LETTER AIN -> ain-ar"""
        # U+0639 ARABIC LETTER AIN
        result = glyph_data_for_unicode(0x0639)
        self.assertEqual(result, "ain-ar")

    def test_arabic_letter_qaf(self):
        """Test: ARABIC LETTER QAF -> qaf-ar"""
        # U+0642 ARABIC LETTER QAF
        result = glyph_data_for_unicode(0x0642)
        self.assertEqual(result, "qaf-ar")

    def test_arabic_letter_lam(self):
        """Test: ARABIC LETTER LAM -> lam-ar"""
        # U+0644 ARABIC LETTER LAM
        result = glyph_data_for_unicode(0x0644)
        self.assertEqual(result, "lam-ar")

    def test_arabic_letter_noon(self):
        """Test: ARABIC LETTER NOON -> noon-ar"""
        # U+0646 ARABIC LETTER NOON
        result = glyph_data_for_unicode(0x0646)
        self.assertEqual(result, "noon-ar")

    def test_arabic_letter_heh(self):
        """Test: ARABIC LETTER HEH -> heh-ar"""
        # U+0647 ARABIC LETTER HEH
        result = glyph_data_for_unicode(0x0647)
        self.assertEqual(result, "heh-ar")

    def test_arabic_letter_yeh(self):
        """Test: ARABIC LETTER YEH -> yeh-ar"""
        # U+064A ARABIC LETTER YEH
        result = glyph_data_for_unicode(0x064A)
        self.assertEqual(result, "yeh-ar")

    def test_arabic_letter_hamza(self):
        """Test: ARABIC LETTER HAMZA -> hamza-ar"""
        # U+0621 ARABIC LETTER HAMZA
        result = glyph_data_for_unicode(0x0621)
        self.assertEqual(result, "hamza-ar")

    def test_arabic_letter_alef_with_madda_above(self):
        """Test: ARABIC LETTER ALEF WITH MADDA ABOVE -> alefMaddaAbove-ar"""
        # U+0622 ARABIC LETTER ALEF WITH MADDA ABOVE
        result = glyph_data_for_unicode(0x0622)
        self.assertEqual(result, "alefMaddaAbove-ar")

    def test_arabic_letter_alef_with_hamza_above(self):
        """Test: ARABIC LETTER ALEF WITH HAMZA ABOVE -> alefHamzaAbove-ar"""
        # U+0623 ARABIC LETTER ALEF WITH HAMZA ABOVE
        result = glyph_data_for_unicode(0x0623)
        self.assertEqual(result, "alefHamzaAbove-ar")

    def test_arabic_letter_waw_with_hamza_above(self):
        """Test: ARABIC LETTER WAW WITH HAMZA ABOVE -> wawHamzaAbove-ar"""
        # U+0624 ARABIC LETTER WAW WITH HAMZA ABOVE
        result = glyph_data_for_unicode(0x0624)
        self.assertEqual(result, "wawHamzaAbove-ar")

    def test_arabic_letter_alef_with_hamza_below(self):
        """Test: ARABIC LETTER ALEF WITH HAMZA BELOW -> alefHamzaBelow-ar"""
        # U+0625 ARABIC LETTER ALEF WITH HAMZA BELOW
        result = glyph_data_for_unicode(0x0625)
        self.assertEqual(result, "alefHamzaBelow-ar")

    def test_arabic_letter_yeh_with_hamza_above(self):
        """Test: ARABIC LETTER YEH WITH HAMZA ABOVE -> yehHamzaAbove-ar"""
        # U+0626 ARABIC LETTER YEH WITH HAMZA ABOVE
        result = glyph_data_for_unicode(0x0626)
        self.assertEqual(result, "yehHamzaAbove-ar")

    # Multi-letter ligature tests (all uppercase)
    def test_latin_capital_ligature_ae(self):
        """Test: LATIN CAPITAL LETTER AE -> AE-lat"""
        # U+00C6 LATIN CAPITAL LETTER AE
        result = glyph_data_for_unicode(0x00C6)
        self.assertEqual(result, "AE-lat")

    def test_latin_small_ligature_ae(self):
        """Test: LATIN SMALL LETTER AE -> ae-lat"""
        # U+00E6 LATIN SMALL LETTER AE
        result = glyph_data_for_unicode(0x00E6)
        self.assertEqual(result, "ae-lat")

    def test_latin_capital_ligature_oe(self):
        """Test: LATIN CAPITAL LETTER OE -> OE-lat"""
        # U+0152 LATIN CAPITAL LETTER OE
        result = glyph_data_for_unicode(0x0152)
        self.assertEqual(result, "OE-lat")

    def test_latin_small_ligature_oe(self):
        """Test: LATIN SMALL LETTER OE -> oe-lat"""
        # U+0153 LATIN SMALL LETTER OE
        result = glyph_data_for_unicode(0x0153)
        self.assertEqual(result, "oe-lat")

    def test_latin_capital_ligature_ij(self):
        """Test: LATIN CAPITAL LETTER IJ -> IJ-lat"""
        # U+0132 LATIN CAPITAL LETTER IJ
        result = glyph_data_for_unicode(0x0132)
        self.assertEqual(result, "IJ-lat")

    def test_latin_small_ligature_ij(self):
        """Test: LATIN SMALL LETTER IJ -> ij-lat"""
        # U+0133 LATIN SMALL LETTER IJ
        result = glyph_data_for_unicode(0x0133)
        self.assertEqual(result, "ij-lat")


if __name__ == "__main__":
    unittest.main()
