# Glyph Name Casing Rules

## Overview

The `context-glyphdata` package uses intelligent casing rules to generate glyph names that reflect the character's case through the name itself, rather than using explicit "capital" or "small" tokens.

## Rules

### 1. Capital Letters (Single Letter Names)
**Unicode Pattern:** `LATIN CAPITAL LETTER A`  
**Transformation:** First letter uppercase, rest lowercase  
**Result:** `A-lat`

The word "CAPITAL" is removed, and the letter name is capitalized.

### 2. Small/Lowercase Letters
**Unicode Pattern:** `LATIN SMALL LETTER A`  
**Transformation:** All lowercase  
**Result:** `a-lat`

The word "SMALL" is removed, and the letter name is kept lowercase.

### 3. Capital Letters (Multi-Word Names)
**Unicode Pattern:** `GREEK CAPITAL LETTER ALPHA`  
**Transformation:** Capitalize first letter of the name  
**Result:** `Alpha-gr`

For longer names, "CAPITAL" is removed and the name is capitalized (title case).

### 4. Small Letters (Multi-Word Names)
**Unicode Pattern:** `GREEK SMALL LETTER ALPHA`  
**Transformation:** All lowercase  
**Result:** `alpha-gr`

For longer names, "SMALL" is removed and the name is kept lowercase.

### 5. Multi-Letter Ligatures (Capital)
**Unicode Pattern:** `LATIN CAPITAL LETTER AE`  
**Transformation:** Keep all letters uppercase  
**Result:** `AE-lat`

Special case for ligatures composed of multiple letters (AE, OE, IJ, etc.) - all letters remain uppercase when capital.

### 6. Multi-Letter Ligatures (Small)
**Unicode Pattern:** `LATIN SMALL LETTER AE`  
**Transformation:** All lowercase  
**Result:** `ae-lat`

Same ligatures in lowercase form remain all lowercase.

### 7. Characters Without Case Indicators
**Unicode Pattern:** `ARABIC LETTER ALEF`  
**Transformation:** All lowercase (no CAPITAL/SMALL indicator)  
**Result:** `alef-ar`

Characters from scripts that don't distinguish case are treated as lowercase.

### 8. Symbols
**Unicode Pattern:** `COMMERCIAL AT`  
**Transformation:** camelCase (first word lowercase)  
**Result:** `commercialAt`

Symbols have no case indicators and use standard camelCase rules.

## Examples

| Unicode Name | Old Behavior | New Behavior |
|--------------|--------------|--------------|
| LATIN CAPITAL LETTER A | capitalA-lat | **A-lat** |
| LATIN SMALL LETTER A | smallA-lat | **a-lat** |
| GREEK CAPITAL LETTER ALPHA | capitalAlpha-gr | **Alpha-gr** |
| GREEK SMALL LETTER ALPHA | smallAlpha-gr | **alpha-gr** |
| LATIN CAPITAL LETTER AE | capitalAE-lat | **AE-lat** |
| LATIN SMALL LETTER AE | smallAe-lat | **ae-lat** |
| LATIN CAPITAL LETTER IJ | capitalIJ-lat | **IJ-lat** |
| LATIN SMALL LETTER IJ | smallIj-lat | **ij-lat** |
| ARABIC LETTER ALEF | alef-ar | alef-ar (unchanged) |
| COMMERCIAL AT | commercialAt | commercialAt (unchanged) |

## Multi-Part Names with Case

### Arabic Multi-Part Names (No Case)
**Unicode Pattern:** `ARABIC LETTER ALEF WITH HAMZA ABOVE`  
**Result:** `alefHamzaAbove-ar`

Subsequent words in multi-part names are always title-cased, regardless of the first word's casing.

### Latin Multi-Part Names (Capital)
**Unicode Pattern:** `LATIN CAPITAL LETTER A WITH ACUTE`  
**Result:** `AWithAcute-lat` → `AWithAcute-lat` (after removing "WITH") → `AAcute-lat`

## Implementation Details

The casing logic in `core.py`:

1. **Detect case indicators** before removing them (`CAPITAL` or `SMALL`)
2. **Remove case indicators** from the word list
3. **Apply casing rules** based on detected indicators:
   - Multi-letter acronyms (≤3 chars, all alpha, capital): keep uppercase
   - Capital letters: capitalize first letter only
   - Everything else: lowercase
4. **Subsequent words**: always title case (capitalize)

## Benefits

1. **More intuitive**: `A-lat` is clearer than `capitalA-lat`
2. **Shorter names**: Removes redundant "capital" and "small" tokens
3. **Better readability**: The casing itself conveys the information
4. **Consistent with standards**: Matches common glyph naming conventions
