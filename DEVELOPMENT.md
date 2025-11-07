# Development Guide

## Installation for Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/context-glyphdata.git
cd context-glyphdata
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in editable mode:
```bash
pip install -e .
```

## Running Tests

Run all unit tests:
```bash
python -m unittest discover tests
```

Run a specific test:
```bash
python -m unittest tests.test_glyph_names.TestGlyphNameGeneration.test_arabic_letter_alef
```

## Building for Distribution

1. Install build tools:
```bash
pip install build twine
```

2. Build the distribution packages:
```bash
python -m build
```

This will create both wheel and source distributions in the `dist/` directory.

## Publishing to PyPI

### TestPyPI (for testing)

1. Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

2. Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ context-glyphdata
```

### Production PyPI

1. Upload to PyPI:
```bash
twine upload dist/*
```

2. Install from PyPI:
```bash
pip install context-glyphdata
```

## Code Style

This project follows PEP 8 guidelines. You can check your code with:

```bash
pip install flake8
flake8 src/ tests/
```

## Adding New Script Mappings

To add support for new writing scripts, edit `src/context_glyphdata/core.py` and add entries to the `SCRIPT_SUFFIXES` dictionary:

```python
SCRIPT_SUFFIXES = {
    "ARABIC": "-ar",
    "LATIN": "-lat",
    # Add your new script here
    "NEWSCRIPT": "-new",
}
```

Then add corresponding test cases in `tests/test_glyph_names.py`.
