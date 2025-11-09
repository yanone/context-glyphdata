"""Command-line interface for context-glyphdata."""

import sys
import argparse
import youseedee
from .core import glyph_data_for_unicode


def char_command(character):
    """Analyze a single character."""
    if len(character) != 1:
        print("Error: Please provide exactly one character", file=sys.stderr)
        sys.exit(1)

    char = character
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


def render_command():
    """Render all Unicode characters with their names and glyph names."""
    # Scan entire Unicode range
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

            # Print in format: U+XXXX UNICODE_NAME -> glyph_name
            print(f"U+{codepoint:04X} {name:60} -> {glyph_name}")

        except Exception:
            # Skip characters that cause errors
            continue


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate glyph names from Unicode characters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  char <character>    Analyze a single character
  render              Render all Unicode characters with names (pipe to grep to filter)

Examples:
  context-glyphdata char A
  context-glyphdata char Ω
  context-glyphdata render | grep ARABIC
  context-glyphdata render | grep -i "letter a"
        """,
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="Command to execute (char or render). If omitted, assumes 'char'",
    )
    parser.add_argument(
        "argument", nargs="?", help="Argument for the command (character for 'char')"
    )

    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Determine which command to run
    if args.command == "render":
        render_command()
    elif args.command == "char":
        if not args.argument:
            print("Error: 'char' command requires a character argument", file=sys.stderr)
            sys.exit(1)
        char_command(args.argument)
    else:
        # Assume the command is actually a character (backward compatibility)
        char_command(args.command)


if __name__ == "__main__":
    main()
