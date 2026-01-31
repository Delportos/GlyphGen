"""
SVG Glyph Generator

Generates glyphs as SVG files by combining radical path elements.
Uses svgwrite for SVG document creation and svgpathtools for path manipulation.
"""

import os
import random
from typing import List, Tuple, Optional
from pathlib import Path

try:
    import svgwrite
    from svgwrite import Drawing
    from svgwrite.path import Path as SVGPath
    from svgwrite.container import Group
except ImportError:
    raise ImportError("svgwrite is required. Install with: pip install svgwrite")

try:
    from svgpathtools import parse_path, Path as ToolPath, wsvg
except ImportError:
    raise ImportError("svgpathtools is required. Install with: pip install svgpathtools")

from svg_radicals import (
    LEFT_RADICALS, TOP_RADICALS, BOTTOM_RADICALS,
    get_radical_path, list_radicals
)


class SVGGlyphGenerator:
    """
    Generates SVG glyphs by combining left, top, and bottom radicals.
    """

    def __init__(self, output_dir: str = "svg_output"):
        """
        Initialize the SVG Glyph Generator.

        Args:
            output_dir: Directory for saving generated SVG files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Glyph dimensions (base unit size)
        self.base_size = 20
        self.default_scale = 10  # Scale factor for output
        self.stroke_width = 2
        self.stroke_color = "#000000"
        self.fill_color = "none"
        self.background_color = "#f5f5f5"

        # Radical counts for random generation
        self.num_left = len(LEFT_RADICALS)
        self.num_top = len(TOP_RADICALS)
        self.num_bottom = len(BOTTOM_RADICALS)

    def create_glyph_svg(
        self,
        radical_tuple: Tuple[str, str, str],
        size: int = 200,
        with_background: bool = True
    ) -> Drawing:
        """
        Create an SVG drawing for a single glyph.

        Args:
            radical_tuple: Tuple of (left_radical, top_radical, bottom_radical)
            size: Output size in pixels
            with_background: Whether to include a background rectangle

        Returns:
            svgwrite.Drawing object
        """
        left_rad, top_rad, bottom_rad = radical_tuple

        # Create SVG drawing
        dwg = svgwrite.Drawing(
            size=(f"{size}px", f"{size}px"),
            viewBox=f"0 0 {self.base_size} {self.base_size}"
        )

        # Add background if requested
        if with_background:
            dwg.add(dwg.rect(
                insert=(0, 0),
                size=(self.base_size, self.base_size),
                fill=self.background_color
            ))

        # Create a group for the glyph paths
        glyph_group = dwg.g(
            stroke=self.stroke_color,
            stroke_width=self.stroke_width / (size / self.base_size),
            fill=self.fill_color,
            stroke_linecap="round",
            stroke_linejoin="round"
        )

        # Add each radical path
        for rad_id in [left_rad, top_rad, bottom_rad]:
            path_data = get_radical_path(rad_id)
            path = dwg.path(d=path_data)
            glyph_group.add(path)

        dwg.add(glyph_group)
        return dwg

    def save_glyph(
        self,
        radical_tuple: Tuple[str, str, str],
        filename: str = None,
        size: int = 200,
        with_background: bool = True
    ) -> str:
        """
        Save a glyph as an SVG file.

        Args:
            radical_tuple: Tuple of (left_radical, top_radical, bottom_radical)
            filename: Output filename (auto-generated if None)
            size: Output size in pixels
            with_background: Whether to include a background

        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"glyph_{'_'.join(radical_tuple)}.svg"

        filepath = self.output_dir / filename
        dwg = self.create_glyph_svg(radical_tuple, size, with_background)
        dwg.saveas(str(filepath))
        return str(filepath)

    def generate_random_glyph(self) -> Tuple[str, str, str]:
        """
        Generate a random radical combination.

        Returns:
            Tuple of (left_radical, top_radical, bottom_radical)
        """
        left = f"l{random.randint(0, self.num_left - 1)}"
        top = f"t{random.randint(0, self.num_top - 1)}"
        bottom = f"b{random.randint(0, self.num_bottom - 1)}"
        return (left, top, bottom)

    def generate_unique_glyphs(self, count: int) -> List[Tuple[str, str, str]]:
        """
        Generate a list of unique random radical combinations.

        Args:
            count: Number of unique combinations to generate

        Returns:
            List of radical tuples
        """
        max_combinations = self.num_left * self.num_top * self.num_bottom
        if count > max_combinations:
            count = max_combinations

        glyphs = set()
        attempts = 0
        max_attempts = count * 10

        while len(glyphs) < count and attempts < max_attempts:
            glyph = self.generate_random_glyph()
            glyphs.add(glyph)
            attempts += 1

        return list(glyphs)

    def create_glyph_grid_svg(
        self,
        glyphs: List[Tuple[str, str, str]],
        cols: int = 6,
        cell_size: int = 100,
        padding: int = 10
    ) -> Drawing:
        """
        Create an SVG with a grid of multiple glyphs.

        Args:
            glyphs: List of radical tuples
            cols: Number of columns in the grid
            cell_size: Size of each cell in pixels
            padding: Padding between cells

        Returns:
            svgwrite.Drawing object
        """
        rows = (len(glyphs) + cols - 1) // cols
        total_width = cols * (cell_size + padding) + padding
        total_height = rows * (cell_size + padding) + padding

        dwg = svgwrite.Drawing(
            size=(f"{total_width}px", f"{total_height}px")
        )

        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(total_width, total_height),
            fill="#67696c"  # DIN gray from original
        ))

        # Add each glyph
        for i, glyph_tuple in enumerate(glyphs):
            row = i // cols
            col = i % cols

            x = padding + col * (cell_size + padding)
            y = padding + row * (cell_size + padding)

            # Create a nested SVG for each glyph
            glyph_svg = dwg.svg(
                insert=(x, y),
                size=(cell_size, cell_size),
                viewBox=f"0 0 {self.base_size} {self.base_size}"
            )

            # Add background for this glyph
            glyph_svg.add(dwg.rect(
                insert=(0, 0),
                size=(self.base_size, self.base_size),
                fill=self.background_color
            ))

            # Add radical paths
            glyph_group = dwg.g(
                stroke=self.stroke_color,
                stroke_width=self.stroke_width / (cell_size / self.base_size),
                fill=self.fill_color,
                stroke_linecap="round",
                stroke_linejoin="round"
            )

            for rad_id in glyph_tuple:
                path_data = get_radical_path(rad_id)
                path = dwg.path(d=path_data)
                glyph_group.add(path)

            glyph_svg.add(glyph_group)
            dwg.add(glyph_svg)

        return dwg

    def save_glyph_grid(
        self,
        glyphs: List[Tuple[str, str, str]],
        filename: str = "glyph_grid.svg",
        cols: int = 6,
        cell_size: int = 100,
        padding: int = 10
    ) -> str:
        """
        Save a grid of glyphs as an SVG file.

        Args:
            glyphs: List of radical tuples
            filename: Output filename
            cols: Number of columns
            cell_size: Size of each cell
            padding: Padding between cells

        Returns:
            Path to saved file
        """
        filepath = self.output_dir / filename
        dwg = self.create_glyph_grid_svg(glyphs, cols, cell_size, padding)
        dwg.saveas(str(filepath))
        return str(filepath)

    def get_combined_path_data(
        self,
        radical_tuple: Tuple[str, str, str]
    ) -> str:
        """
        Get combined path data for all radicals in a glyph.

        Args:
            radical_tuple: Tuple of (left_radical, top_radical, bottom_radical)

        Returns:
            Combined SVG path data string
        """
        paths = []
        for rad_id in radical_tuple:
            paths.append(get_radical_path(rad_id))
        return ' '.join(paths)

    def create_character_string_svg(
        self,
        glyph_list: List[Tuple[str, str, str]],
        char_size: int = 100,
        spacing: int = 20
    ) -> Drawing:
        """
        Create an SVG showing glyphs arranged horizontally like text.

        Args:
            glyph_list: List of radical tuples representing characters
            char_size: Size of each character
            spacing: Spacing between characters

        Returns:
            svgwrite.Drawing object
        """
        num_chars = len(glyph_list)
        total_width = num_chars * char_size + (num_chars - 1) * spacing + 40
        total_height = char_size + 40

        dwg = svgwrite.Drawing(
            size=(f"{total_width}px", f"{total_height}px")
        )

        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(total_width, total_height),
            fill="#ffffff"
        ))

        # Add each character
        for i, glyph_tuple in enumerate(glyph_list):
            x = 20 + i * (char_size + spacing)
            y = 20

            # Nested SVG for the character
            char_svg = dwg.svg(
                insert=(x, y),
                size=(char_size, char_size),
                viewBox=f"0 0 {self.base_size} {self.base_size}"
            )

            # Add radical paths
            char_group = dwg.g(
                stroke=self.stroke_color,
                stroke_width=self.stroke_width / (char_size / self.base_size),
                fill=self.fill_color,
                stroke_linecap="round",
                stroke_linejoin="round"
            )

            for rad_id in glyph_tuple:
                path_data = get_radical_path(rad_id)
                path = dwg.path(d=path_data)
                char_group.add(path)

            char_svg.add(char_group)
            dwg.add(char_svg)

        return dwg

    def save_character_string(
        self,
        glyph_list: List[Tuple[str, str, str]],
        filename: str = "character_string.svg",
        char_size: int = 100,
        spacing: int = 20
    ) -> str:
        """
        Save a horizontal string of characters as an SVG file.

        Args:
            glyph_list: List of radical tuples
            filename: Output filename
            char_size: Size of each character
            spacing: Spacing between characters

        Returns:
            Path to saved file
        """
        filepath = self.output_dir / filename
        dwg = self.create_character_string_svg(glyph_list, char_size, spacing)
        dwg.saveas(str(filepath))
        return str(filepath)

    def set_style(
        self,
        stroke_color: str = None,
        stroke_width: float = None,
        fill_color: str = None,
        background_color: str = None
    ):
        """
        Set styling options for generated SVGs.

        Args:
            stroke_color: Hex color for strokes
            stroke_width: Width of strokes
            fill_color: Fill color (or 'none')
            background_color: Background color
        """
        if stroke_color is not None:
            self.stroke_color = stroke_color
        if stroke_width is not None:
            self.stroke_width = stroke_width
        if fill_color is not None:
            self.fill_color = fill_color
        if background_color is not None:
            self.background_color = background_color


class SVGGlyphRenderer:
    """
    Renders SVG glyphs to PNG using CairoSVG.
    Optional component for when PNG output is needed.
    """

    def __init__(self):
        """Initialize the renderer, checking for CairoSVG availability."""
        try:
            import cairosvg
            self.cairosvg = cairosvg
            self.available = True
        except ImportError:
            self.cairosvg = None
            self.available = False
            print("Warning: cairosvg not installed. PNG rendering unavailable.")
            print("Install with: pip install cairosvg")

    def render_to_png(
        self,
        svg_path: str,
        output_path: str = None,
        scale: float = 1.0
    ) -> Optional[str]:
        """
        Render an SVG file to PNG.

        Args:
            svg_path: Path to input SVG file
            output_path: Path for output PNG (auto-generated if None)
            scale: Scale factor for output

        Returns:
            Path to output PNG, or None if rendering failed
        """
        if not self.available:
            print("CairoSVG not available. Cannot render to PNG.")
            return None

        if output_path is None:
            output_path = svg_path.replace('.svg', '.png')

        self.cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            scale=scale
        )
        return output_path

    def render_svg_string_to_png(
        self,
        svg_string: str,
        output_path: str,
        scale: float = 1.0
    ) -> Optional[str]:
        """
        Render an SVG string directly to PNG.

        Args:
            svg_string: SVG content as string
            output_path: Path for output PNG
            scale: Scale factor for output

        Returns:
            Path to output PNG, or None if rendering failed
        """
        if not self.available:
            print("CairoSVG not available. Cannot render to PNG.")
            return None

        self.cairosvg.svg2png(
            bytestring=svg_string.encode('utf-8'),
            write_to=output_path,
            scale=scale
        )
        return output_path


def main():
    """Demo the SVG glyph generator."""
    print("SVG Glyph Generator Demo")
    print("=" * 40)

    # Initialize generator
    gen = SVGGlyphGenerator(output_dir="svg_output")

    # Generate a single random glyph
    print("\n1. Generating single random glyph...")
    glyph = gen.generate_random_glyph()
    print(f"   Radical combination: {glyph}")
    path = gen.save_glyph(glyph)
    print(f"   Saved to: {path}")

    # Generate a grid of glyphs
    print("\n2. Generating grid of 30 unique glyphs...")
    glyphs = gen.generate_unique_glyphs(30)
    grid_path = gen.save_glyph_grid(glyphs, filename="demo_grid.svg")
    print(f"   Saved to: {grid_path}")

    # Generate a character string
    print("\n3. Generating character string (5 characters)...")
    char_glyphs = gen.generate_unique_glyphs(5)
    string_path = gen.save_character_string(
        char_glyphs,
        filename="demo_string.svg"
    )
    print(f"   Saved to: {string_path}")

    # Try to render to PNG
    print("\n4. Attempting PNG rendering...")
    renderer = SVGGlyphRenderer()
    if renderer.available:
        png_path = renderer.render_to_png(path)
        print(f"   PNG saved to: {png_path}")
    else:
        print("   Skipping PNG render (install cairosvg for this feature)")

    # Show style customization
    print("\n5. Generating styled glyph...")
    gen.set_style(
        stroke_color="#2a4858",
        stroke_width=3,
        background_color="#e8e4d9"
    )
    styled_glyph = ('l3', 't2', 'b5')
    styled_path = gen.save_glyph(styled_glyph, filename="styled_glyph.svg")
    print(f"   Saved to: {styled_path}")

    print("\n" + "=" * 40)
    print("Demo complete! Check the 'svg_output' folder for generated files.")


if __name__ == "__main__":
    main()
