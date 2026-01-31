#!/usr/bin/env python3
"""
SVG Glyph Generation Demo

This script demonstrates the SVG path-based glyph generation system.
It shows various ways to create, combine, and export glyphs as SVG files.

Usage:
    python svg_demo.py [command]

Commands:
    single    - Generate a single random glyph
    grid      - Generate a grid of 30 glyphs
    string    - Generate a string of 5 characters
    variants  - Generate variant sheets for all radical types
    specimen  - Generate a specimen sheet
    all       - Run all demos

If no command is specified, runs all demos.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from svg_glyph_gen import SVGGlyphGenerator, SVGGlyphRenderer
from svg_path_combiner import SVGPathCombiner, GlyphFontGenerator, PathTransform
from svg_radicals import list_radicals, get_radical_info


def demo_single_glyph():
    """Generate a single random glyph."""
    print("\n" + "=" * 50)
    print("DEMO: Single Glyph Generation")
    print("=" * 50)

    gen = SVGGlyphGenerator("svg_output")

    # Random glyph
    glyph = gen.generate_random_glyph()
    print(f"\nGenerated radical combination: {glyph}")

    path = gen.save_glyph(glyph, size=300)
    print(f"Saved to: {path}")

    # Also try PNG rendering if available
    renderer = SVGGlyphRenderer()
    if renderer.available:
        png_path = renderer.render_to_png(path, scale=2)
        print(f"PNG rendered to: {png_path}")

    return path


def demo_glyph_grid():
    """Generate a grid of multiple glyphs."""
    print("\n" + "=" * 50)
    print("DEMO: Glyph Grid Generation")
    print("=" * 50)

    gen = SVGGlyphGenerator("svg_output")

    # Generate 30 unique glyphs
    glyphs = gen.generate_unique_glyphs(30)
    print(f"\nGenerated {len(glyphs)} unique glyphs")

    path = gen.save_glyph_grid(
        glyphs,
        filename="glyph_grid_30.svg",
        cols=6,
        cell_size=100
    )
    print(f"Saved grid to: {path}")

    return path


def demo_character_string():
    """Generate characters arranged as a string/word."""
    print("\n" + "=" * 50)
    print("DEMO: Character String Generation")
    print("=" * 50)

    gen = SVGGlyphGenerator("svg_output")

    # Generate a "word" of 5 characters
    glyphs = gen.generate_unique_glyphs(5)
    print(f"\nGenerated {len(glyphs)} characters for the string")
    for i, g in enumerate(glyphs):
        print(f"  Character {i+1}: {g}")

    path = gen.save_character_string(
        glyphs,
        filename="character_string.svg",
        char_size=80,
        spacing=15
    )
    print(f"Saved string to: {path}")

    return path


def demo_radical_variants():
    """Show all variants for each radical type."""
    print("\n" + "=" * 50)
    print("DEMO: Radical Variant Sheets")
    print("=" * 50)

    combiner = SVGPathCombiner("svg_output")

    # List available radicals
    print("\nAvailable radicals:")
    print(f"  Left (l):   {list_radicals('l')}")
    print(f"  Top (t):    {list_radicals('t')}")
    print(f"  Bottom (b): {list_radicals('b')}")

    # Create variant sheets
    paths = []
    for rad_type in ['l', 't', 'b']:
        path = combiner.create_variant_grid('l0', rad_type, size=100, cols=5)
        paths.append(path)
        print(f"\nSaved {rad_type} variants to: {path}")

    return paths


def demo_transformations():
    """Demonstrate path transformations."""
    print("\n" + "=" * 50)
    print("DEMO: Path Transformations")
    print("=" * 50)

    combiner = SVGPathCombiner("svg_output")

    # Original glyph
    original = ('l3', 't2', 'b4')
    path1 = combiner.save_combined_glyph(
        original,
        filename="original_glyph.svg",
        size=200
    )
    print(f"\nOriginal glyph {original} saved to: {path1}")

    # Transformed version - shift the top radical up
    transforms = {
        'l3': PathTransform(scale_x=1.1, translate_x=-0.5),
        't2': PathTransform(translate_y=-2, scale_y=0.9),
        'b4': PathTransform(translate_y=2, scale_x=1.1)
    }

    path2 = combiner.save_combined_glyph(
        original,
        filename="transformed_glyph.svg",
        transforms=transforms,
        size=200
    )
    print(f"Transformed glyph saved to: {path2}")

    return [path1, path2]


def demo_specimen_sheet():
    """Generate a specimen sheet for all glyphs."""
    print("\n" + "=" * 50)
    print("DEMO: Specimen Sheet")
    print("=" * 50)

    font_gen = GlyphFontGenerator("svg_output")

    path = font_gen.create_specimen_sheet(
        sample_size=64,
        filename="specimen_sheet_64.svg"
    )
    print(f"\nSpecimen sheet saved to: {path}")

    return path


def demo_styled_glyphs():
    """Demonstrate different styling options."""
    print("\n" + "=" * 50)
    print("DEMO: Styled Glyphs")
    print("=" * 50)

    gen = SVGGlyphGenerator("svg_output")
    glyph = ('l5', 't3', 'b2')

    # Style 1: Dark theme
    gen.set_style(
        stroke_color="#e0e0e0",
        stroke_width=2.5,
        background_color="#2a2a2a"
    )
    path1 = gen.save_glyph(glyph, filename="styled_dark.svg", size=200)
    print(f"\nDark themed glyph saved to: {path1}")

    # Style 2: Warm theme
    gen.set_style(
        stroke_color="#8b4513",
        stroke_width=3,
        background_color="#f5e6d3"
    )
    path2 = gen.save_glyph(glyph, filename="styled_warm.svg", size=200)
    print(f"Warm themed glyph saved to: {path2}")

    # Style 3: Minimal
    gen.set_style(
        stroke_color="#000000",
        stroke_width=1.5,
        background_color="#ffffff"
    )
    path3 = gen.save_glyph(glyph, filename="styled_minimal.svg", size=200)
    print(f"Minimal glyph saved to: {path3}")

    return [path1, path2, path3]


def demo_radical_info():
    """Show information about available radicals."""
    print("\n" + "=" * 50)
    print("DEMO: Radical Information")
    print("=" * 50)

    print("\nLeft Radicals (l0-l9):")
    for rad_id in list_radicals('l'):
        info = get_radical_info(rad_id)
        print(f"  {rad_id}: {info['description']}")

    print("\nTop Radicals (t0-t5):")
    for rad_id in list_radicals('t'):
        info = get_radical_info(rad_id)
        print(f"  {rad_id}: {info['description']}")

    print("\nBottom Radicals (b0-b7):")
    for rad_id in list_radicals('b'):
        info = get_radical_info(rad_id)
        print(f"  {rad_id}: {info['description']}")


def run_all_demos():
    """Run all demonstration functions."""
    print("\n" + "#" * 60)
    print("# SVG Glyph Generator - Complete Demo Suite")
    print("#" * 60)

    demo_radical_info()
    demo_single_glyph()
    demo_glyph_grid()
    demo_character_string()
    demo_radical_variants()
    demo_transformations()
    demo_styled_glyphs()
    demo_specimen_sheet()

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("Check the 'svg_output' directory for generated files.")
    print("=" * 60)


def print_help():
    """Print usage information."""
    print(__doc__)


def main():
    """Main entry point."""
    commands = {
        'single': demo_single_glyph,
        'grid': demo_glyph_grid,
        'string': demo_character_string,
        'variants': demo_radical_variants,
        'specimen': demo_specimen_sheet,
        'styled': demo_styled_glyphs,
        'transforms': demo_transformations,
        'info': demo_radical_info,
        'all': run_all_demos,
        'help': print_help,
        '-h': print_help,
        '--help': print_help,
    }

    if len(sys.argv) < 2:
        run_all_demos()
    else:
        cmd = sys.argv[1].lower()
        if cmd in commands:
            commands[cmd]()
        else:
            print(f"Unknown command: {cmd}")
            print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
