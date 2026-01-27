# CLAUDE.md - AI Assistant Guide for GlyphGen

## Project Overview

GlyphGen is a Python-based procedural glyph generator that combines different radical components (left, top, bottom) to create unique visual glyphs. It uses Pygame for real-time graphical rendering and can generate hundreds of unique combinations by mixing radical variations.

**Author:** Frank Gallo
**License:** MIT
**Language:** Python 3.x

## Tech Stack & Dependencies

| Dependency | Purpose |
|------------|---------|
| **Pygame** | 2D graphics rendering and display management |
| **NumPy** | Imported but currently unused (legacy) |
| **Python stdlib** | `random`, `sys`, `os` for core functionality |

### Installation

```bash
pip install pygame numpy
```

## Directory Structure

```
GlyphGen/
├── glyphGen.py          # Main application (single-file architecture)
├── radsheet1.png        # Legacy combined spritesheet (1000x600px, unused)
├── radsheets/           # Current radical spritesheets (20x20px base)
│   ├── lrad0.png        # Left radicals (10 variations: l0-l9)
│   ├── trad0.png        # Top radicals (6 variations: t0-t5)
│   └── brad0.png        # Bottom radicals (8 variations: b0-b7)
├── README.md            # User documentation
├── LICENSE              # MIT License
└── .gitignore           # Excludes __pycache__/ and *.pyc
```

## Architecture

### Core Class: `GlyphGenerator`

The entire application is contained in a single class in `glyphGen.py`:

- **`__init__()`** - Initializes Pygame, loads spritesheets, sets up radical dictionaries
- **`get_sprite(row, col, target_size, rad_type)`** - Extracts and scales sprites from sheets
- **`draw_glyph(size)`** - Generates and displays a single random glyph
- **`character_gen(char_amount)`** - Generates unique glyph combinations (collision-free)
- **`draw_glyph_at_pos(rad_tuple, position, size)`** - Renders glyph at specific position
- **`draw_glyph_grid(amount, out, num_glyphs)`** - Renders a grid of glyphs

### Data Model

Glyphs are represented as tuples of three radical identifiers:

```python
glyph = ('l0', 't2', 'b4')  # (left_radical, top_radical, bottom_radical)
```

Radical positions are stored in dictionaries mapping identifiers to spritesheet coordinates:

```python
self.lrad_pos = {'l0': (0,0), 'l1': (0,1), ...}  # (row, col)
self.trad_pos = {'t0': (0,0), 't1': (0,1), ...}
self.brad_pos = {'b0': (0,0), 'b1': (0,1), ...}
```

### Radical System

| Type | Prefix | Count | Sheet | Dictionary |
|------|--------|-------|-------|------------|
| Left | `l` | 10 (l0-l9) | `radsheets/lrad0.png` | `self.lrad_pos` |
| Top | `t` | 6 (t0-t5) | `radsheets/trad0.png` | `self.trad_pos` |
| Bottom | `b` | 8 (b0-b7) | `radsheets/brad0.png` | `self.brad_pos` |

**Total unique combinations:** 10 x 6 x 8 = 480 glyphs

## Code Conventions

### Naming

- **Radical prefixes:** `l` (left), `t` (top), `b` (bottom)
- **Abbreviations:** `rad` (radical), `sh` (sheet), `pos` (position), `loc` (location)
- **Variables:** snake_case for all variables and methods
- **Class:** PascalCase (`GlyphGenerator`)

### Constants (hardcoded in `__init__`)

```python
self.screen_width = 600        # Display window width
self.screen_height = 600       # Display window height
self.sprite_width = 20         # Base sprite size
self.sprite_height = 20        # Base sprite size
self.current_size = (200, 200) # Default glyph render size
```

### Background Color

```python
self.screen.fill((103, 105, 124))  # "din gray"
```

## Running the Application

```bash
python glyphGen.py
```

### Interactive Commands

| Command | Action |
|---------|--------|
| `new` | Generate and display a new random glyph |
| `grid` | Display a 6-column grid of 30 random glyphs |
| `size` | Set custom glyph size (50-600px range) |
| `quit` | Exit the program |

## Development Workflow

### Adding New Radicals

1. Add sprite to appropriate sheet in `radsheets/` directory
2. Update the corresponding position dictionary (`lrad_pos`, `trad_pos`, or `brad_pos`)
3. Update the `locs*` count variable (`locsL`, `locsT`, or `locsB`)

### Modifying Sprite Sheets

- Sprite dimensions are 20x20px
- Sprites are arranged in rows and columns
- Position dictionaries use `(row, col)` format (0-indexed)

### Key Files to Modify

| Task | File | Location |
|------|------|----------|
| Add radicals | `glyphGen.py` | Lines 51-67 (dictionaries), Lines 39-41 (counts) |
| Change display settings | `glyphGen.py` | Lines 14-15 (screen size), Line 43 (default glyph size) |
| Modify grid layout | `glyphGen.py` | Lines 199-203 (`draw_glyph_grid` method) |
| Add new commands | `glyphGen.py` | Lines 229-255 (main loop) |

## Common AI Assistant Tasks

### When asked to add new radical types:
1. Create/modify the spritesheet PNG in `radsheets/`
2. Add entries to the appropriate `*rad_pos` dictionary
3. Update the corresponding `locs*` count

### When asked to modify glyph rendering:
1. Check `get_sprite()` for sprite extraction logic
2. Check `draw_glyph()` or `draw_glyph_at_pos()` for rendering logic

### When asked to add new commands:
1. Add a new `elif` block in the main loop (line 229+)
2. Follow existing pattern: `elif writing.lower() == 'command':`

### When asked to export/save glyphs:
- Use `pygame.image.save(surface, filename)`
- Create a new surface with the glyph, then save it

## Known Issues / Technical Debt

1. **NumPy imported but unused** - Can be removed unless planned for future use
2. **Legacy spritesheet** - `radsheet1.png` and `self.rad_pos` dictionary are no longer used
3. **Magic numbers** - Screen size, margins, grid layout are hardcoded
4. **Comments** - Some comments reference wrong radical type (lines 25-26 say "L radical" for T and B)
5. **Size validation** - Size limits (50-600) are checked but not enforced (glyph still renders)

## Testing

No automated tests exist. Manual testing workflow:

1. Run `python glyphGen.py`
2. Test `new` command - verify glyph renders
3. Test `grid` command - verify grid of 30 glyphs renders
4. Test `size` command - verify custom sizes work
5. Test window close - verify clean exit

## Git Workflow

- Main development happens on feature branches prefixed with `claude/`
- Commits should follow conventional commit format: `feat:`, `fix:`, `refactor:`
- The `.gitignore` excludes `__pycache__/` and `*.pyc` files

## Quick Reference

```python
# Create generator instance
glyph = GlyphGenerator()

# Generate a single glyph (random)
glyph.draw_glyph(size=(200, 200))

# Generate unique characters
characters = glyph.character_gen(15)  # Returns list of tuples

# Draw specific glyph at position
glyph.draw_glyph_at_pos(('l0', 't2', 'b4'), (100, 100), (100, 100))

# Draw grid of glyphs
glyph.draw_glyph_grid(amount=15, out=30)  # 15 unique, display 30
```
