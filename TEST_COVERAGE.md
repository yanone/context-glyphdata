# Test Coverage Summary

## Total Tests: 36

### Test Categories

#### 1. Lowercase Letters (5 tests)
- Latin small letters (a, z)
- Greek small letters (alpha, omega)
- Cyrillic small letter (a)

**Examples:**
- `LATIN SMALL LETTER A` → `smallA-lat`
- `GREEK SMALL LETTER ALPHA` → `smallAlpha-gr`
- `CYRILLIC SMALL LETTER A` → `smallA-cyr`

#### 2. Symbols (7 tests)
- Mathematical operators (+, =, *, %)
- Currency symbols ($)
- Special characters (@, &)

**Examples:**
- `PLUS SIGN` → `plus`
- `COMMERCIAL AT` → `commercialAt`
- `DOLLAR SIGN` → `dollar`
- `AMPERSAND` → `ampersand`

#### 3. Arabic Characters (15 tests)

##### Simple Arabic Letters:
- Basic consonants (alef, beh, hah, seen, ain, qaf, lam, noon, heh, yeh)
- Special letters (hamza, teh marbuta)

**Examples:**
- `ARABIC LETTER ALEF` → `alef-ar`
- `ARABIC LETTER TEH MARBUTA` → `tehMarbuta-ar`
- `ARABIC LETTER HAMZA` → `hamza-ar`

##### Multi-Part Arabic Names (combining forms):
- Alef with modifiers (madda above, hamza above, hamza below)
- Waw with hamza above
- Yeh with hamza above

**Examples:**
- `ARABIC LETTER ALEF WITH MADDA ABOVE` → `alefMaddaAbove-ar`
- `ARABIC LETTER ALEF WITH HAMZA ABOVE` → `alefHamzaAbove-ar`
- `ARABIC LETTER ALEF WITH HAMZA BELOW` → `alefHamzaBelow-ar`
- `ARABIC LETTER WAW WITH HAMZA ABOVE` → `wawHamzaAbove-ar`
- `ARABIC LETTER YEH WITH HAMZA ABOVE` → `yehHamzaAbove-ar`

#### 4. Other Scripts (9 tests)
- Latin capital letters
- Greek capital letters
- Cyrillic capital letters
- Hebrew letters
- Thai characters
- Devanagari letters
- Fallback scenarios

## Test Results

All 36 tests pass successfully! ✓

### Test Execution Time
- Average: ~0.14 seconds for full suite
- Per test: ~4ms average

## Unicode Coverage

The tests cover a wide range of Unicode blocks:
- **Basic Latin**: U+0020-U+007F (symbols and lowercase letters)
- **Arabic**: U+0621-U+064A (basic letters and combining forms)
- **Greek**: U+0391-U+03C9 (capital and small letters)
- **Cyrillic**: U+0410-U+0430 (capital and small letters)
- **Hebrew**: U+05D0 (letters)
- **Thai**: U+0E01 (characters)
- **Devanagari**: U+0915 (letters)

## Key Test Features

1. **Lowercase Letter Handling**: Verifies proper camelCase conversion for small letters
2. **Symbol Processing**: Tests removal of category words (SIGN, SYMBOL)
3. **Multi-Word Names**: Confirms proper camelCase for complex names like "ALEF WITH HAMZA ABOVE"
4. **Script Detection**: Validates script suffix assignment across multiple writing systems
5. **Edge Cases**: Includes fallback scenarios for characters without clear script indicators

## Running the Tests

```bash
# Run all tests
python -m unittest discover tests

# Run with verbose output
python -m unittest tests.test_glyph_names -v

# Run a specific test
python -m unittest tests.test_glyph_names.TestGlyphNameGeneration.test_arabic_letter_alef_with_hamza_above
```
