"""
Test script coverage to ensure SCRIPT_SUFFIXES stays up-to-date with Unicode.

This test module performs automated checks to help maintain SCRIPT_SUFFIXES
after Unicode version updates:

1. **test_script_coverage_in_unicode_names**: Samples Unicode character names
   to detect commonly-used scripts that are missing from SCRIPT_SUFFIXES.
   - Fails if >30 scripts are missing or any script appears >50 times
   - Otherwise prints warnings for review

2. **test_all_defined_scripts_are_used**: Verifies that scripts defined in
   SCRIPT_SUFFIXES actually exist in Unicode character names.
   - Catches typos or obsolete script names
   - Fails if >10 defined scripts are never found in character names

3. **test_no_duplicate_glyph_names**: Checks entire Unicode catalog for
   duplicate glyph name outputs.
   - Ensures uniqueness of generated glyph names
   - Fails if any duplicates are found

These tests help ensure comprehensive script coverage as Unicode evolves.
"""

import unittest
from collections import Counter, defaultdict
import youseedee
from context_glyphdata.core import SCRIPT_SUFFIXES, DROP_CATEGORIES
from context_glyphdata import glyph_data_for_unicode


class TestScriptCoverage(unittest.TestCase):
    """Test that SCRIPT_SUFFIXES covers all commonly used scripts."""

    def test_no_duplicate_script_suffixes(self):
        """
        Verify that no two scripts share the same suffix.

        Each script must have a unique suffix to avoid ambiguity in glyph names.
        """
        suffix_to_scripts = {}
        duplicates = {}

        for script, suffix in SCRIPT_SUFFIXES.items():
            if suffix in suffix_to_scripts:
                # Found a duplicate
                if suffix not in duplicates:
                    duplicates[suffix] = [suffix_to_scripts[suffix]]
                duplicates[suffix].append(script)
            else:
                suffix_to_scripts[suffix] = script

        if duplicates:
            msg_lines = ["\nDuplicate script suffixes detected:"]
            for suffix, scripts in sorted(duplicates.items()):
                msg_lines.append(f"  '{suffix}' used by: {', '.join(sorted(scripts))}")
            msg_lines.append(
                "\nEach script must have a unique suffix. "
                "Please update SCRIPT_SUFFIXES."
            )
            self.fail("\n".join(msg_lines))

    def test_no_duplicate_glyph_names(self):
        """
        Check entire Unicode catalog for duplicate glyph name outputs.

        This test scans all Unicode codepoints and ensures that the
        transformation produces unique glyph names. Any duplicates indicate
        a problem with the transformation logic or missing script suffixes.

        Also checks that no glyph names contain underscores.
        """
        glyph_name_to_codepoints = defaultdict(list)
        glyph_names_with_underscores = []
        total_chars = 0

        # Scan entire Unicode range (0x0000 to 0x10FFFF)
        # We'll check every codepoint that has a name
        print("\nScanning Unicode catalog for duplicate glyph names...")

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
                    glyph_name_to_codepoints[glyph_name].append((codepoint, name))
                    total_chars += 1

                    # Check for underscores
                    if "_" in glyph_name:
                        glyph_names_with_underscores.append(
                            (codepoint, name, glyph_name)
                        )

            except Exception:
                # Skip characters that cause errors
                continue

        # Find duplicates
        duplicates = {
            glyph_name: codepoints
            for glyph_name, codepoints in glyph_name_to_codepoints.items()
            if len(codepoints) > 1
        }

        print(f"Scanned {total_chars} named characters")

        # Check for underscores first
        if glyph_names_with_underscores:
            msg_lines = [
                f"\nFound {len(glyph_names_with_underscores)} glyph names "
                "with underscores:",
                "",
            ]

            # Show first 20
            for cp, unicode_name, glyph_name in glyph_names_with_underscores[:20]:
                msg_lines.append(f"  U+{cp:04X} {unicode_name} -> '{glyph_name}'")

            if len(glyph_names_with_underscores) > 20:
                msg_lines.append(
                    f"  ... and {len(glyph_names_with_underscores) - 20} more"
                )

            msg_lines.append("")
            msg_lines.append(
                "Glyph names must not contain underscores "
                "(underscores have special meaning in font editing)."
            )

            self.fail("\n".join(msg_lines))

        if duplicates:
            msg_lines = [
                f"\nFound {len(duplicates)} duplicate glyph names:",
                "",
            ]

            # Sort by number of duplicates (most problematic first)
            sorted_duplicates = sorted(
                duplicates.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )

            # Show first 20 most problematic duplicates
            for glyph_name, codepoints in sorted_duplicates[:20]:
                msg_lines.append(f"  '{glyph_name}' ({len(codepoints)} occurrences):")
                for cp, unicode_name in codepoints[:5]:  # Show first 5
                    msg_lines.append(f"    U+{cp:04X} {unicode_name}")
                if len(codepoints) > 5:
                    msg_lines.append(f"    ... and {len(codepoints) - 5} more")
                msg_lines.append("")

            if len(duplicates) > 20:
                msg_lines.append(f"  ... and {len(duplicates) - 20} more duplicates")
                msg_lines.append("")

            msg_lines.append("Each Unicode character must produce a unique glyph name.")
            msg_lines.append(
                "Fix by adding missing script suffixes or adjusting "
                "transformation logic."
            )

            self.fail("\n".join(msg_lines))
        else:
            print(f"✓ All {total_chars} glyph names are unique")
            print(f"✓ All {total_chars} glyph names are underscore-free")

    def test_script_coverage_in_unicode_names(self):
        """
        Analyze Unicode character names to find potential missing scripts.

        This test samples Unicode codepoints and extracts script names from
        character names, then checks if they're defined in SCRIPT_SUFFIXES.
        It allows for some scripts to be missing (very rare or specialized
        scripts), but alerts if commonly used scripts are missing.
        """
        # Sample ranges to check (covers most named characters)
        sample_ranges = [
            (0x0000, 0x0FFF),  # Basic Multilingual Plane start
            (0x1000, 0x1FFF),  # Extended scripts
            (0x2000, 0x2FFF),  # Symbols and additional scripts
            (0x3000, 0x9FFF),  # CJK and additional scripts
            (0xA000, 0xAFFF),  # Yi and other scripts
            (0x10000, 0x10FFF),  # Linear B, Aegean, Old Italic, etc.
            (0x11000, 0x11FFF),  # Brahmi, Kaithi, etc.
            (0x12000, 0x12FFF),  # Cuneiform
            (0x13000, 0x13FFF),  # Egyptian Hieroglyphs
            (0x16000, 0x16FFF),  # Runic, Ogham, etc.
        ]

        # Extract script names from character names
        script_counter = Counter()
        total_chars_checked = 0

        for start, end in sample_ranges:
            # Sample every 16th character to keep test fast
            for codepoint in range(start, end, 16):
                try:
                    ucd = youseedee.ucd_data(codepoint)
                    if not ucd or "Name" not in ucd:
                        continue

                    name = ucd["Name"]
                    if not name or name.startswith("<"):
                        continue

                    total_chars_checked += 1
                    parts = name.split()

                    # Look for potential script names
                    # Script names typically appear before category words
                    for i, part in enumerate(parts):
                        # Skip if it's a category word
                        if part in DROP_CATEGORIES:
                            continue

                        # Check if this could be a script name
                        # Script names are typically ALL CAPS words before
                        # the category
                        if part.isupper() and len(part) > 2:
                            # Check if it's followed by a category word
                            # or if it's in a known position for script names
                            if i + 1 < len(parts) and parts[i + 1] in DROP_CATEGORIES:
                                script_counter[part] += 1
                            # Multi-word scripts
                            elif (
                                i + 1 < len(parts)
                                and parts[i + 1].isupper()
                                and len(parts[i + 1]) > 2
                            ):
                                multi_word = f"{part} {parts[i + 1]}"
                                script_counter[multi_word] += 1
                except Exception:
                    # Skip characters that cause errors
                    continue

        # Now check which scripts appear frequently but aren't in
        # SCRIPT_SUFFIXES
        missing_scripts = {}
        threshold = 5  # Scripts must appear at least 5 times to be considered

        for script, count in script_counter.items():
            if count < threshold:
                continue

            # Check if this script is in SCRIPT_SUFFIXES
            # (either as-is or as part of it)
            found = False

            # Check exact match
            if script in SCRIPT_SUFFIXES:
                found = True
            else:
                # Check if any defined script is a substring
                # (handles multi-word scripts)
                for defined_script in SCRIPT_SUFFIXES.keys():
                    if defined_script in script or script in defined_script:
                        found = True
                        break

            if not found:
                missing_scripts[script] = count

        # Filter out known exceptions (these are not script names)
        known_exceptions = {
            "VERTICAL",
            "HORIZONTAL",
            "COMBINING",
            "SPACING",
            "MODIFIER",
            "DOUBLE",
            "TRIPLE",
            "SINGLE",
            "FINAL",
            "INITIAL",
            "MEDIAL",
            "ISOLATED",
            "PRESENTATION",
            "COMPATIBILITY",
            "FULLWIDTH",
            "HALFWIDTH",
            "SMALL",
            "CAPITAL",
            "SQUARED",
            "CIRCLED",
            "PARENTHESIZED",
            "MATHEMATICAL",
            "SANS-SERIF",
            "BOLD",
            "ITALIC",
            "SCRIPT",
            "FRAKTUR",
            "MONOSPACE",
            "BLACK",
            "WHITE",
            "HEAVY",
            "LIGHT",
            "DASHED",
            "DOTTED",
            "VOWEL",
            "BRAILLE",
            "KANGXI",
            "WITH",
            "DOT",
            "SYLLABICS",
            "PSILI",
            "NUMERIC",
            "ARROW",
            "BOX",
            "CJK",
            "DRAWINGS",
            "CARRIER",
            "PATTERN",
            "ABOVE",
            "BELOW",
        }

        missing_scripts = {
            script: count
            for script, count in missing_scripts.items()
            if not any(exc in script for exc in known_exceptions)
        }

        # Generate informative message
        if missing_scripts:
            sorted_missing = sorted(
                missing_scripts.items(), key=lambda x: x[1], reverse=True
            )
            msg_lines = [
                "\nPotentially missing scripts in SCRIPT_SUFFIXES:",
                f"(Checked {total_chars_checked} characters)",
                "",
            ]
            for script, count in sorted_missing[:20]:  # Show top 20
                msg_lines.append(f"  {script}: {count} occurrences")

            msg_lines.append("")
            msg_lines.append(
                "Note: Some of these may be intentionally excluded "
                "(rare/historical scripts)."
            )
            msg_lines.append("Review and add commonly used scripts to SCRIPT_SUFFIXES.")

            # This is a warning, not a failure
            # Only fail if there are MANY missing scripts (>30)
            # or if any single script appears very frequently (>50 times)
            # This catches major omissions after Unicode updates
            high_frequency_scripts = [(s, c) for s, c in sorted_missing if c > 50]

            if len(missing_scripts) > 30 or high_frequency_scripts:
                if high_frequency_scripts:
                    msg_lines.insert(
                        0,
                        "\nWARNING: High-frequency potentially missing "
                        "scripts detected!",
                    )
                self.fail("\n".join(msg_lines))
            else:
                # Just print a warning for future consideration
                print("\n".join(msg_lines))

    def test_all_defined_scripts_are_used(self):
        """
        Verify that scripts defined in SCRIPT_SUFFIXES actually exist
        in Unicode character names.

        This catches typos or obsolete script names in SCRIPT_SUFFIXES.
        """
        # Sample ranges (same as above)
        sample_ranges = [
            (0x0000, 0x0FFF),
            (0x1000, 0x1FFF),
            (0x2000, 0x2FFF),
            (0x3000, 0x9FFF),
            (0xA000, 0xAFFF),
            (0x10000, 0x10FFF),
            (0x11000, 0x11FFF),
            (0x12000, 0x12FFF),
            (0x13000, 0x13FFF),
            (0x16000, 0x16FFF),
        ]

        # Find which defined scripts appear in character names
        found_scripts = set()

        for start, end in sample_ranges:
            for codepoint in range(start, end, 8):  # Sample every 8th
                try:
                    ucd = youseedee.ucd_data(codepoint)
                    if not ucd or "Name" not in ucd:
                        continue

                    name = ucd["Name"]
                    if not name or name.startswith("<"):
                        continue

                    # Check which defined scripts appear in this name
                    for script in SCRIPT_SUFFIXES.keys():
                        if script in name:
                            found_scripts.add(script)

                except Exception:
                    continue

        # Find scripts that are defined but never found
        unused_scripts = set(SCRIPT_SUFFIXES.keys()) - found_scripts

        # Some scripts are prefix/generic patterns and won't be found directly
        # These are OK to not find in actual character names
        allowed_unused = {
            "TAI",  # Prefix for Tai Le, Tai Tham, etc.
            "OLD",  # Prefix for Old Italic, Old Persian, etc.
            "HAN",  # CJK ideographs use different naming
        }

        unused_scripts = unused_scripts - allowed_unused

        if unused_scripts:
            # This is informational - some scripts may be rare
            # Only fail if there are many unused (>10)
            if len(unused_scripts) > 10:
                sorted_unused = sorted(unused_scripts)
                msg = (
                    f"\n{len(unused_scripts)} scripts defined in "
                    "SCRIPT_SUFFIXES but not found in sampled "
                    "character names:\n  "
                    + "\n  ".join(sorted_unused)
                    + "\n\nThis may indicate typos or scripts that don't "
                    "appear in Unicode character names."
                )
                self.fail(msg)
            else:
                # Just print info for rare scripts
                print(
                    f"\nInfo: {len(unused_scripts)} rarely used scripts: "
                    f"{sorted(unused_scripts)}"
                )


if __name__ == "__main__":
    unittest.main()
