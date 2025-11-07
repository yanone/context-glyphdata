"""Command-line interface for context-glyphdata."""

import sys
import argparse
import youseedee
from .core import glyph_data_for_unicode


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate glyph names from Unicode characters"
    )
    parser.add_argument("character", help="A single character to analyze")

    args = parser.parse_args()

    if len(args.character) != 1:
        print("Error: Please provide exactly one character", file=sys.stderr)
        sys.exit(1)

    char = args.character
    codepoint = ord(char)

    # Get Unicode data
    ucd = youseedee.ucd_data(codepoint)

    # Print Unicode information
    print(f"Character: {char}")
    print(f"Unicode: U+{codepoint:04X} (decimal: {codepoint})")

    if ucd:
        if "Name" in ucd:
            print(f"Name: {ucd['Name']}")
        if "General_Category" in ucd:
            print(f"Category: {ucd['General_Category']}")
        if "Script" in ucd:
            print(f"Script: {ucd['Script']}")
        if "Block" in ucd:
            print(f"Block: {ucd['Block']}")

    # Generate and print glyph name
    glyph_name = glyph_data_for_unicode(codepoint)
    print(f"\nGenerated glyph name: {glyph_name}")


if __name__ == "__main__":
    main()
