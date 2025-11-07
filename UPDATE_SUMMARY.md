# Update Summary: Intelligent Casing for Glyph Names

## Changes Made

### Core Functionality (`core.py`)

1. **Added `CASE_INDICATORS` set** containing "CAPITAL" and "SMALL" tokens
2. **Enhanced casing logic** to detect case before removing indicators
3. **Implemented smart casing rules**:
   - Capital single letters: Uppercase (A, B, C)
   - Capital multi-word names: Title case (Alpha, Beta, Gamma)
   - Small letters: Lowercase (a, b, c, alpha, beta)
   - Multi-letter ligatures: Preserve case (AE, OE, IJ vs ae, oe, ij)
   - No case indicator: Lowercase (alef, beh, seen)

### Test Suite (`test_glyph_names.py`)

**Total Tests: 42** (all passing ✓)

#### Updated Tests
- Latin capital/small letters: Now expect `A-lat` / `a-lat` instead of `capitalA-lat` / `smallA-lat`
- Greek capital/small letters: Now expect `Alpha-gr` / `alpha-gr` instead of `capitalAlpha-gr` / `smallAlpha-gr`
- Cyrillic capital/small letters: Now expect `A-cyr` / `a-cyr`

#### New Tests Added (6 tests)
1. `test_latin_capital_ligature_ae` - Tests `AE-lat`
2. `test_latin_small_ligature_ae` - Tests `ae-lat`
3. `test_latin_capital_ligature_oe` - Tests `OE-lat`
4. `test_latin_small_ligature_oe` - Tests `oe-lat`
5. `test_latin_capital_ligature_ij` - Tests `IJ-lat`
6. `test_latin_small_ligature_ij` - Tests `ij-lat`

## Transformation Examples

### Before vs After

| Unicode Name | Old Result | New Result | Improvement |
|--------------|-----------|------------|-------------|
| LATIN CAPITAL LETTER A | capitalA-lat | **A-lat** | Shorter, clearer |
| LATIN SMALL LETTER A | smallA-lat | **a-lat** | Shorter, clearer |
| GREEK CAPITAL LETTER ALPHA | capitalAlpha-gr | **Alpha-gr** | Shorter, clearer |
| GREEK SMALL LETTER ALPHA | smallAlpha-gr | **alpha-gr** | Shorter, clearer |
| LATIN CAPITAL LETTER AE | capitalAE-lat | **AE-lat** | Preserves ligature |
| LATIN SMALL LETTER AE | smallAe-lat | **ae-lat** | Consistent lowercase |
| ARABIC LETTER ALEF | alef-ar | alef-ar | No change (correct) |

### Special Cases Handled

1. **Multi-letter ligatures (≤3 chars, all letters)**
   - Capital: `AE`, `OE`, `IJ` - all letters stay uppercase
   - Small: `ae`, `oe`, `ij` - all letters stay lowercase

2. **Single-letter names**
   - Capital: `A`, `B`, `Z` - single uppercase letter
   - Small: `a`, `b`, `z` - single lowercase letter

3. **Multi-word names**
   - Capital: `Alpha`, `Beta`, `Omega` - first letter capitalized
   - Small: `alpha`, `beta`, `omega` - all lowercase

4. **Scripts without case**
   - Arabic, Hebrew, Devanagari, etc. - always lowercase
   - Example: `alef-ar`, `ka-dev`, `alef-he`

## Documentation Updates

1. **README.md** - Updated examples to show new casing
2. **CASING_RULES.md** - New comprehensive guide to casing logic
3. **TEST_COVERAGE.md** - Would need update to reflect new test count

## Benefits

1. ✓ **Shorter names** - Removes redundant "capital" and "small" tokens
2. ✓ **More intuitive** - Casing itself conveys the information
3. ✓ **Industry standard** - Matches common glyph naming conventions
4. ✓ **Better readability** - `A-lat` vs `capitalA-lat`
5. ✓ **Handles edge cases** - Multi-letter ligatures preserved correctly

## Test Results

```
Ran 42 tests in 0.140s
OK
```

All tests passing! ✓

## Files Modified

- `src/context_glyphdata/core.py` - Core casing logic
- `tests/test_glyph_names.py` - Updated expectations + new ligature tests
- `README.md` - Updated examples
- `CASING_RULES.md` - New documentation (created)

## Backwards Compatibility

⚠️ **Breaking Change**: This update changes the output format for glyph names.

Users upgrading from previous versions will see different glyph names for:
- All capital letters (e.g., `capitalA-lat` → `A-lat`)
- All small letters (e.g., `smallA-lat` → `a-lat`)

This is an intentional improvement to the naming scheme.
