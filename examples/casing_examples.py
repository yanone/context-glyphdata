"""Comprehensive examples of the new casing behavior."""

from context_glyphdata import glyph_data_for_unicode

print("=" * 70)
print("Context Glyph Data - Comprehensive Casing Examples")
print("=" * 70)

# Single-letter capital letters
print("\n### Single-Letter Capital Letters ###")
examples = [
    (0x0041, "LATIN CAPITAL LETTER A"),
    (0x0042, "LATIN CAPITAL LETTER B"),
    (0x005A, "LATIN CAPITAL LETTER Z"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Single-letter small letters
print("\n### Single-Letter Small Letters ###")
examples = [
    (0x0061, "LATIN SMALL LETTER A"),
    (0x0062, "LATIN SMALL LETTER B"),
    (0x007A, "LATIN SMALL LETTER Z"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Multi-word capital letters
print("\n### Multi-Word Capital Letter Names ###")
examples = [
    (0x0391, "GREEK CAPITAL LETTER ALPHA"),
    (0x0392, "GREEK CAPITAL LETTER BETA"),
    (0x03A9, "GREEK CAPITAL LETTER OMEGA"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Multi-word small letters
print("\n### Multi-Word Small Letter Names ###")
examples = [
    (0x03B1, "GREEK SMALL LETTER ALPHA"),
    (0x03B2, "GREEK SMALL LETTER BETA"),
    (0x03C9, "GREEK SMALL LETTER OMEGA"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Multi-letter ligatures (capital)
print("\n### Multi-Letter Ligatures (Capital) ###")
examples = [
    (0x00C6, "LATIN CAPITAL LETTER AE"),
    (0x0152, "LATIN CAPITAL LETTER OE"),
    (0x0132, "LATIN CAPITAL LETTER IJ"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Multi-letter ligatures (small)
print("\n### Multi-Letter Ligatures (Small) ###")
examples = [
    (0x00E6, "LATIN SMALL LETTER AE"),
    (0x0153, "LATIN SMALL LETTER OE"),
    (0x0133, "LATIN SMALL LETTER IJ"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# No case indicator (Arabic)
print("\n### Characters Without Case Indicators ###")
examples = [
    (0x0627, "ARABIC LETTER ALEF"),
    (0x0628, "ARABIC LETTER BEH"),
    (0x0633, "ARABIC LETTER SEEN"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Multi-part Arabic names
print("\n### Multi-Part Arabic Names ###")
examples = [
    (0x0622, "ARABIC LETTER ALEF WITH MADDA ABOVE"),
    (0x0623, "ARABIC LETTER ALEF WITH HAMZA ABOVE"),
    (0x0625, "ARABIC LETTER ALEF WITH HAMZA BELOW"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

# Symbols
print("\n### Symbols (No Case) ###")
examples = [
    (0x0026, "AMPERSAND"),
    (0x0040, "COMMERCIAL AT"),
    (0x002B, "PLUS SIGN"),
    (0x003D, "EQUALS SIGN"),
]
for cp, desc in examples:
    print(f"{chr(cp)} U+{cp:04X} {desc:40s} -> {glyph_data_for_unicode(cp)}")

print("\n" + "=" * 70)
