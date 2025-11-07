# Context Glyph Data

A Python package that converts Unicode character descriptions to short camelCase glyph names.

## Features

- Converts official Unicode character descriptions to concise camelCase glyph names
- Adds script-specific suffixes (e.g., `-ar` for Arabic, `-lat` for Latin)
- Removes category words (LETTER, SYMBOL, etc.) for cleaner names
- Provides both a Python API and command-line tool
- Built on top of the `youseedee` Unicode database library

## Installation

```bash
pip install context-glyphdata
```

## Usage

### Python API

```python
from context_glyphdata import glyph_data_for_unicode

# Example: ARABIC LETTER ALEF (U+0627)
glyph_name = glyph_data_for_unicode(0x0627)
print(glyph_name)  # Output: alef-ar

# Example: GREEK CAPITAL LETTER ALPHA (U+0391)
glyph_name = glyph_data_for_unicode(0x0391)
print(glyph_name)  # Output: capitalAlpha-gr
```

### Command-Line Tool

```bash
# Analyze a character
context-glyphdata ا

# Output:
# Character: ا
# Unicode: U+0627 (decimal: 1575)
# Name: ARABIC LETTER ALEF
# Category: Lo
# Script: Arabic
# Block: Arabic
#
# Generated glyph name: alef-ar
```

## Name Transformation Rules

1. **Script Detection**: Recognizes writing scripts (Arabic, Latin, Greek, etc.) and converts them to short suffixes
   - `ARABIC` → `-ar`
   - `LATIN` → `-lat`
   - `GREEK` → `-gr`
   - And many more...

2. **Category Removal**: Drops generic category words like LETTER, SYMBOL, MARK, etc.

3. **camelCase Conversion**: Converts the remaining words to camelCase format

### Examples

- `ARABIC LETTER ALEF` → `alef-ar`
- `GREEK CAPITAL LETTER ALPHA` → `capitalAlpha-gr`
- `LATIN CAPITAL LETTER A` → `capitalA-lat`
- `HEBREW LETTER ALEF` → `alef-he`

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/context-glyphdata.git
cd context-glyphdata

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Built on top of [youseedee](https://github.com/simoncozens/youseedee) for Unicode character data.
