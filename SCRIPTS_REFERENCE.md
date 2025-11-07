# Script Suffix Reference

## Source

The `SCRIPT_SUFFIXES` dictionary in `core.py` was compiled through analysis of actual Unicode character names using the `youseedee` library. The script names were discovered by:

1. Sampling Unicode codepoints across the entire range (U+0000 to U+2FFFF+)
2. Parsing character names to find script identifiers (words that appear before "LETTER", "CHARACTER", "DIGIT", etc.)
3. Filtering to commonly-used scripts (appearing in 5+ characters)
4. Cross-referencing with the Unicode Script property

## Coverage

The current list covers **~80 scripts**, including:

### Major World Scripts (Most Common)
- Arabic, Latin, Greek, Cyrillic, Hebrew, Armenian

### Indic/Brahmic Scripts (~15 scripts)
- Devanagari, Bengali, Tamil, Telugu, Gujarati, etc.
- Historical: Brahmi, Grantha, Kaithi, Sharada

### Southeast Asian Scripts (~10 scripts)
- Thai, Lao, Myanmar, Khmer, Javanese, Balinese, Cham

### East Asian Scripts
- Han (CJK), Hangul (Korean), Hiragana, Katakana, Bopomofo, Yi

### African Scripts
- Ethiopic, Vai, Bamum, Adlam, N'Ko, Tifinagh, Osmanya

### American Scripts
- Cherokee, Canadian Aboriginal Syllabics, Deseret, Osage

### Historical & Ancient Scripts (~20 scripts)
- Cuneiform, Egyptian Hieroglyphs, Linear A/B, Phoenician
- Gothic, Glagolitic, Coptic, Ogham, Runic
- Cypriot, Aramaic, Avestan, Ugaritic, Anatolian

### Other Scripts
- Duployan, Mende Kikakui, Miao (Pollard), Tangut, Nushu
- Saurashtra, Hentaigana (Japanese kana variants)

## Suffix Conventions

Where possible, suffixes follow these conventions:

1. **ISO 15924 codes**: For well-known scripts (e.g., `-xsux` for Cuneiform)
2. **Short abbreviations**: 2-4 letter codes (e.g., `-ar` for Arabic, `-dev` for Devanagari)
3. **Descriptive**: Based on the script name (e.g., `-glag` for Glagolitic)

## Scripts Not Included

The Unicode Standard defines **174 official scripts** (via the Script property), but many are:
- Rare or specialized (e.g., Kawi, Kirat Rai, Todhri)
- Recently added with few encoded characters
- Not typically included in character names

Scripts are added to the list when:
- They appear in character names (not just the Script property)
- Multiple characters use that script identifier
- They're likely to be encountered in practical use

## Updating the List

To find new scripts that should be added:

```python
import youseedee

# Sample Unicode to find script names in character names
for cp in range(0x0, 0x30000, 10):
    ucd = youseedee.ucd_data(cp)
    if ucd and 'Name' in ucd:
        name = ucd['Name']
        # Look for patterns like "SCRIPTNAME LETTER X"
```

## References

- Unicode Character Database: https://www.unicode.org/ucd/
- ISO 15924 Script Codes: https://unicode.org/iso15924/
- youseedee library: https://github.com/simoncozens/youseedee
