# Context Glyph Data - Package Overview

## Package Structure

```
context-glyphdata/
├── src/
│   └── context_glyphdata/
│       ├── __init__.py       # Package initialization
│       ├── core.py           # Main glyph name generation logic
│       └── cli.py            # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_glyph_names.py   # Unit tests
├── examples/
│   └── basic_usage.py        # Example script
├── dist/                      # Built distributions (created by build)
├── pyproject.toml            # Package metadata and configuration
├── setup.py                  # Legacy setup file
├── MANIFEST.in               # Distribution file inclusion rules
├── README.md                 # User documentation
├── DEVELOPMENT.md            # Developer guide
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore rules
```

## Key Features

1. **Python API**: `glyph_data_for_unicode(decimal_unicode)` function
2. **CLI Tool**: `context-glyphdata` command-line utility
3. **Unicode Integration**: Uses `youseedee` library for Unicode data
4. **Comprehensive Testing**: Unit tests with multiple script examples
5. **PyPI Ready**: Fully configured for PyPI publishing

## Installation

```bash
pip install context-glyphdata
```

## Quick Start

### Python API
```python
from context_glyphdata import glyph_data_for_unicode

# ARABIC LETTER ALEF
name = glyph_data_for_unicode(0x0627)
print(name)  # Output: alef-ar
```

### Command Line
```bash
context-glyphdata ا
# Outputs Unicode information and generated glyph name
```

## Test Results

All 9 unit tests pass successfully, covering:
- Arabic letters (alef, beh)
- Latin letters
- Greek letters (alpha)
- Cyrillic letters
- Hebrew letters
- Thai characters
- Devanagari letters
- Fallback scenarios

## Publishing to PyPI

### Build the package:
```bash
python -m build
```

### Upload to PyPI:
```bash
pip install twine
twine upload dist/*
```

### Upload to TestPyPI (for testing):
```bash
twine upload --repository testpypi dist/*
```

## Development

### Install in editable mode:
```bash
pip install -e .
```

### Run tests:
```bash
python -m unittest discover tests
```

### Run example:
```bash
python examples/basic_usage.py
```

## Supported Scripts

The package currently supports these writing scripts:
- Arabic (-ar)
- Latin (-lat)
- Greek (-gr)
- Cyrillic (-cyr)
- Hebrew (-he)
- Devanagari (-dev)
- Bengali (-bn)
- Thai (-th)
- And many more...

See `src/context_glyphdata/core.py` for the complete list.

## Name Transformation Examples

| Unicode Name | Generated Glyph Name |
|-------------|---------------------|
| ARABIC LETTER ALEF | alef-ar |
| ARABIC LETTER BEH | beh-ar |
| GREEK CAPITAL LETTER ALPHA | capitalAlpha-gr |
| LATIN CAPITAL LETTER A | capitalA-lat |
| HEBREW LETTER ALEF | alef-he |
| DEVANAGARI LETTER KA | ka-dev |

## License

MIT License - See LICENSE file for details.
