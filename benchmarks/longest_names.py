#!/usr/bin/env python3
"""
Script to find and display longest glyph names from Unicode characters.

This script scans all Unicode codepoints (0x0000 to 0x10FFFF),
generates glyph names using the context-glyphdata transformation logic,
and displays the top 1000 longest names in descending order
along with their lengths.
"""

from context_glyphdata.core import glyph_data_for_unicode
import youseedee


def main():
    print("Scanning all Unicode characters...")
    print("This may take a while...\n")

    # Collect all glyph names with their lengths
    glyph_names = []

    for codepoint in range(0x0000, 0x110000):
        try:
            ucd = youseedee.ucd_data(codepoint)
            if not ucd or "Name" not in ucd:
                continue

            name = ucd["Name"]
            if not name or name.startswith("<"):
                continue

            # Generate glyph name
            glyph_name = glyph_data_for_unicode(codepoint)
            if glyph_name:
                glyph_names.append((len(glyph_name), glyph_name, codepoint, name))
        except Exception:
            # Skip characters that cause errors
            continue

    # Sort by length (descending)
    glyph_names.sort(reverse=True)

    # Print top 1000
    print("Top 1000 longest glyph names:\n")
    print(f"{'Rank':<6} {'Len':<4} " f"{'Glyph Name':<50} {'Code':<8} Unicode Name")
    print("=" * 140)

    for i, (length, glyph_name, codepoint, unicode_name) in enumerate(
        glyph_names[:1000], 1
    ):
        print(
            f"{i:<6} {length:<4} {glyph_name:<50} " f"U+{codepoint:04X}  {unicode_name}"
        )

    print(f"\n{'=' * 140}")
    print(f"Total characters analyzed: {len(glyph_names):,}")
    print(f"Longest name: {glyph_names[0][0]} characters")
    print(f"Shortest name: {glyph_names[-1][0]} characters")
    avg_length = sum(length for length, *_ in glyph_names)
    avg_length = avg_length / len(glyph_names)
    print(f"Average name length: {avg_length:.1f} characters")


if __name__ == "__main__":
    main()
