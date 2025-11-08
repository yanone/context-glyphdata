#!/usr/bin/env python3
"""
Script to find and display glyph names that contain hyphens.

This script scans all Unicode codepoints and identifies glyph names
that contain hyphens (excluding the script suffix which starts with hyphen).
"""

import youseedee
from context_glyphdata import glyph_data_for_unicode


def main():
    print("Scanning all Unicode characters for glyph names with hyphens...")
    print("This may take a while...\n")

    # Collect all glyph names with hyphens
    glyph_names_with_hyphens = []

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
                # Check for hyphens (excluding script suffix)
                # Script suffixes start with hyphen (e.g., "-lat", "-ar")
                if "-" in glyph_name:
                    # Find the last hyphen (script suffix)
                    last_hyphen_idx = glyph_name.rfind("-")
                    # Check if there are any hyphens before the last one
                    prefix = glyph_name[:last_hyphen_idx]
                    if "-" in prefix:
                        glyph_names_with_hyphens.append((codepoint, name, glyph_name))

        except Exception:
            # Skip characters that cause errors
            continue

    # Sort by glyph name
    glyph_names_with_hyphens.sort(key=lambda x: x[2])

    # Print results
    print(f"Found {len(glyph_names_with_hyphens)} glyph names with hyphens:\n")
    print(f"{'Code':<8} {'Glyph Name':<50} Unicode Name")
    print("=" * 120)

    for codepoint, unicode_name, glyph_name in glyph_names_with_hyphens:
        # Truncate unicode name if too long
        if len(unicode_name) > 60:
            unicode_name = unicode_name[:57] + "..."
        print(f"U+{codepoint:04X}  {glyph_name:<50} {unicode_name}")

    print(f"\n{'=' * 120}")
    print(f"Total: {len(glyph_names_with_hyphens)} glyph names contain hyphens")


if __name__ == "__main__":
    main()
