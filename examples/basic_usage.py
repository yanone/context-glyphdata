"""Example usage of the context-glyphdata package."""

from context_glyphdata import glyph_data_for_unicode

# Example characters and their transformations
examples = [
    (0x0627, "ARABIC LETTER ALEF"),
    (0x0628, "ARABIC LETTER BEH"),
    (0x0391, "GREEK CAPITAL LETTER ALPHA"),
    (0x0041, "LATIN CAPITAL LETTER A"),
    (0x05D0, "HEBREW LETTER ALEF"),
    (0x0915, "DEVANAGARI LETTER KA"),
]

print("Context Glyph Data - Example Usage\n")
print("=" * 60)

for codepoint, description in examples:
    glyph_name = glyph_data_for_unicode(codepoint)
    char = chr(codepoint)
    print(f"\nCharacter: {char} (U+{codepoint:04X})")
    print(f"Description: {description}")
    print(f"Generated glyph name: {glyph_name}")

print("\n" + "=" * 60)
