"""
SVG Path Combiner

Advanced path manipulation using svgpathtools for combining and transforming
radical paths into complete glyph characters.
"""

import os
from typing import List, Tuple, Optional, Dict
from pathlib import Path
from dataclasses import dataclass
import math

try:
    from svgpathtools import (
        parse_path, Path as SVGToolPath, Line, CubicBezier, QuadraticBezier, Arc,
        wsvg, svg2paths, disvg
    )
except ImportError:
    raise ImportError("svgpathtools is required. Install with: pip install svgpathtools")

try:
    import svgwrite
    from svgwrite import Drawing
except ImportError:
    raise ImportError("svgwrite is required. Install with: pip install svgwrite")

from svg_radicals import get_radical_path, list_radicals


@dataclass
class PathTransform:
    """Transformation parameters for SVG paths."""
    translate_x: float = 0.0
    translate_y: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotate: float = 0.0  # degrees
    origin_x: float = 0.0
    origin_y: float = 0.0


class SVGPathCombiner:
    """
    Combines and transforms SVG path elements using svgpathtools.
    Provides advanced path manipulation beyond simple overlay.
    """

    def __init__(self, output_dir: str = "svg_output"):
        """
        Initialize the path combiner.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_size = 20

    def parse_radical_paths(
        self,
        radical_ids: List[str]
    ) -> Dict[str, List[SVGToolPath]]:
        """
        Parse radical path strings into svgpathtools Path objects.

        Args:
            radical_ids: List of radical identifiers

        Returns:
            Dictionary mapping radical IDs to parsed Path objects
        """
        parsed = {}
        for rad_id in radical_ids:
            path_str = get_radical_path(rad_id)
            # Split by M commands to handle multiple subpaths
            subpaths = self._split_path_string(path_str)
            parsed[rad_id] = [parse_path(sp) for sp in subpaths if sp.strip()]
        return parsed

    def _split_path_string(self, path_str: str) -> List[str]:
        """
        Split a path string with multiple M commands into separate paths.

        Args:
            path_str: SVG path data string

        Returns:
            List of individual path strings
        """
        # Handle paths with multiple M (moveto) commands
        parts = []
        current = ""
        tokens = path_str.replace(',', ' ').split()

        for token in tokens:
            if token == 'M' and current:
                parts.append(current.strip())
                current = "M"
            else:
                current += " " + token

        if current:
            parts.append(current.strip())

        return parts

    def transform_path(
        self,
        path: SVGToolPath,
        transform: PathTransform
    ) -> SVGToolPath:
        """
        Apply transformation to a path.

        Args:
            path: SVGToolPath to transform
            transform: Transformation parameters

        Returns:
            Transformed path
        """
        # Create transformation as complex number operations
        # svgpathtools uses complex numbers for 2D points

        transformed = path

        # Apply scaling
        if transform.scale_x != 1.0 or transform.scale_y != 1.0:
            # Scale around origin
            origin = complex(transform.origin_x, transform.origin_y)

            def scale_point(p):
                centered = p - origin
                scaled = complex(
                    centered.real * transform.scale_x,
                    centered.imag * transform.scale_y
                )
                return scaled + origin

            transformed = self._transform_path_points(transformed, scale_point)

        # Apply rotation
        if transform.rotate != 0:
            origin = complex(transform.origin_x, transform.origin_y)
            angle_rad = math.radians(transform.rotate)
            rotation = complex(math.cos(angle_rad), math.sin(angle_rad))

            def rotate_point(p):
                centered = p - origin
                rotated = centered * rotation
                return rotated + origin

            transformed = self._transform_path_points(transformed, rotate_point)

        # Apply translation
        if transform.translate_x != 0 or transform.translate_y != 0:
            translation = complex(transform.translate_x, transform.translate_y)
            transformed = transformed.translated(translation)

        return transformed

    def _transform_path_points(self, path: SVGToolPath, transform_func) -> SVGToolPath:
        """
        Apply a point transformation function to all points in a path.

        Args:
            path: Path to transform
            transform_func: Function that transforms a complex point

        Returns:
            New transformed path
        """
        new_segments = []

        for segment in path:
            if isinstance(segment, Line):
                new_segments.append(Line(
                    transform_func(segment.start),
                    transform_func(segment.end)
                ))
            elif isinstance(segment, CubicBezier):
                new_segments.append(CubicBezier(
                    transform_func(segment.start),
                    transform_func(segment.control1),
                    transform_func(segment.control2),
                    transform_func(segment.end)
                ))
            elif isinstance(segment, QuadraticBezier):
                new_segments.append(QuadraticBezier(
                    transform_func(segment.start),
                    transform_func(segment.control),
                    transform_func(segment.end)
                ))
            elif isinstance(segment, Arc):
                # Arcs are more complex - simplified approach
                new_segments.append(Arc(
                    transform_func(segment.start),
                    segment.radius,
                    segment.rotation,
                    segment.large_arc,
                    segment.sweep,
                    transform_func(segment.end)
                ))

        return SVGToolPath(*new_segments)

    def combine_radicals_advanced(
        self,
        radical_tuple: Tuple[str, str, str],
        transforms: Dict[str, PathTransform] = None
    ) -> List[SVGToolPath]:
        """
        Combine radicals with optional transformations.

        Args:
            radical_tuple: (left, top, bottom) radical IDs
            transforms: Optional dict mapping radical IDs to transforms

        Returns:
            List of combined path objects
        """
        if transforms is None:
            transforms = {}

        all_paths = []
        parsed = self.parse_radical_paths(list(radical_tuple))

        for rad_id in radical_tuple:
            paths = parsed.get(rad_id, [])
            transform = transforms.get(rad_id, PathTransform())

            for path in paths:
                transformed = self.transform_path(path, transform)
                all_paths.append(transformed)

        return all_paths

    def paths_to_svg_string(
        self,
        paths: List[SVGToolPath],
        size: int = 200,
        stroke_color: str = "#000000",
        stroke_width: float = 2,
        background: str = "#f5f5f5"
    ) -> str:
        """
        Convert path objects to an SVG string.

        Args:
            paths: List of SVGToolPath objects
            size: Output size in pixels
            stroke_color: Stroke color
            stroke_width: Stroke width
            background: Background color

        Returns:
            SVG content as string
        """
        dwg = svgwrite.Drawing(
            size=(f"{size}px", f"{size}px"),
            viewBox=f"0 0 {self.base_size} {self.base_size}"
        )

        # Background
        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(self.base_size, self.base_size),
            fill=background
        ))

        # Path group
        group = dwg.g(
            stroke=stroke_color,
            stroke_width=stroke_width / (size / self.base_size),
            fill="none",
            stroke_linecap="round",
            stroke_linejoin="round"
        )

        for path in paths:
            path_d = path.d()
            group.add(dwg.path(d=path_d))

        dwg.add(group)
        return dwg.tostring()

    def save_combined_glyph(
        self,
        radical_tuple: Tuple[str, str, str],
        filename: str = None,
        transforms: Dict[str, PathTransform] = None,
        size: int = 200,
        **style_kwargs
    ) -> str:
        """
        Combine radicals and save as SVG.

        Args:
            radical_tuple: (left, top, bottom) radical IDs
            filename: Output filename
            transforms: Optional transformations
            size: Output size
            **style_kwargs: Additional style parameters

        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"combined_{'_'.join(radical_tuple)}.svg"

        paths = self.combine_radicals_advanced(radical_tuple, transforms)
        svg_content = self.paths_to_svg_string(paths, size, **style_kwargs)

        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            f.write(svg_content)

        return str(filepath)

    def create_variant_grid(
        self,
        base_radical: str,
        radical_type: str,
        size: int = 100,
        cols: int = 5
    ) -> str:
        """
        Create a grid showing all variants of a radical type.

        Args:
            base_radical: Base radical to combine with variants
            radical_type: 'l', 't', or 'b' for the varying component
            size: Size of each glyph
            cols: Columns in grid

        Returns:
            Path to saved SVG
        """
        variants = list_radicals(radical_type)
        rows = (len(variants) + cols - 1) // cols
        padding = 10

        total_width = cols * size + (cols + 1) * padding
        total_height = rows * size + (rows + 1) * padding

        dwg = svgwrite.Drawing(
            size=(f"{total_width}px", f"{total_height}px")
        )

        dwg.add(dwg.rect(
            insert=(0, 0),
            size=(total_width, total_height),
            fill="#404040"
        ))

        for i, variant in enumerate(variants):
            row = i // cols
            col = i % cols

            x = padding + col * (size + padding)
            y = padding + row * (size + padding)

            # Build radical tuple based on type
            if radical_type in ['l', 'left']:
                radical_tuple = (variant, 't0', 'b0')
            elif radical_type in ['t', 'top']:
                radical_tuple = ('l0', variant, 'b0')
            else:
                radical_tuple = ('l0', 't0', variant)

            paths = self.combine_radicals_advanced(radical_tuple)

            # Nested SVG
            nested = dwg.svg(
                insert=(x, y),
                size=(size, size),
                viewBox=f"0 0 {self.base_size} {self.base_size}"
            )

            nested.add(dwg.rect(
                insert=(0, 0),
                size=(self.base_size, self.base_size),
                fill="#f5f5f5"
            ))

            group = dwg.g(
                stroke="#000000",
                stroke_width=2 / (size / self.base_size),
                fill="none",
                stroke_linecap="round",
                stroke_linejoin="round"
            )

            for path in paths:
                group.add(dwg.path(d=path.d()))

            nested.add(group)

            # Label
            label = dwg.text(
                variant,
                insert=(x + size/2, y + size + 8),
                fill="white",
                font_size="10px",
                text_anchor="middle"
            )
            dwg.add(nested)
            dwg.add(label)

        filename = f"variants_{radical_type}.svg"
        filepath = self.output_dir / filename
        dwg.saveas(str(filepath))
        return str(filepath)


class GlyphFontGenerator:
    """
    Generate a collection of glyphs suitable for use as a custom font or symbol set.
    """

    def __init__(self, output_dir: str = "svg_font"):
        """Initialize the font generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.combiner = SVGPathCombiner(output_dir)

    def generate_full_set(
        self,
        include_all: bool = False
    ) -> Dict[str, str]:
        """
        Generate a complete set of glyph SVGs.

        Args:
            include_all: If True, generate all possible combinations

        Returns:
            Dictionary mapping glyph names to file paths
        """
        from svg_radicals import LEFT_RADICALS, TOP_RADICALS, BOTTOM_RADICALS

        generated = {}

        if include_all:
            # Generate all combinations
            for l_key in LEFT_RADICALS:
                for t_key in TOP_RADICALS:
                    for b_key in BOTTOM_RADICALS:
                        radical_tuple = (l_key, t_key, b_key)
                        name = f"glyph_{l_key}_{t_key}_{b_key}"
                        filepath = self.combiner.save_combined_glyph(
                            radical_tuple,
                            filename=f"{name}.svg"
                        )
                        generated[name] = filepath
        else:
            # Generate a representative sample
            import random
            for i in range(50):
                l_idx = random.randint(0, len(LEFT_RADICALS) - 1)
                t_idx = random.randint(0, len(TOP_RADICALS) - 1)
                b_idx = random.randint(0, len(BOTTOM_RADICALS) - 1)

                radical_tuple = (f"l{l_idx}", f"t{t_idx}", f"b{b_idx}")
                name = f"glyph_{i:03d}"
                filepath = self.combiner.save_combined_glyph(
                    radical_tuple,
                    filename=f"{name}.svg"
                )
                generated[name] = filepath

        return generated

    def create_specimen_sheet(
        self,
        sample_size: int = 48,
        filename: str = "specimen_sheet.svg"
    ) -> str:
        """
        Create a specimen sheet showing sample glyphs.

        Args:
            sample_size: Number of glyphs to include
            filename: Output filename

        Returns:
            Path to saved file
        """
        from svg_glyph_gen import SVGGlyphGenerator

        gen = SVGGlyphGenerator(str(self.output_dir))
        glyphs = gen.generate_unique_glyphs(sample_size)

        filepath = gen.save_glyph_grid(
            glyphs,
            filename=filename,
            cols=8,
            cell_size=80,
            padding=5
        )

        return filepath


def demo():
    """Demonstrate the path combiner capabilities."""
    print("SVG Path Combiner Demo")
    print("=" * 40)

    combiner = SVGPathCombiner("svg_output")

    # Basic combination
    print("\n1. Basic radical combination...")
    path = combiner.save_combined_glyph(('l2', 't3', 'b1'))
    print(f"   Saved: {path}")

    # With transformations
    print("\n2. Combination with transformations...")
    transforms = {
        'l2': PathTransform(translate_x=1, scale_x=0.9),
        't3': PathTransform(translate_y=-1),
        'b1': PathTransform(scale_y=1.1)
    }
    path = combiner.save_combined_glyph(
        ('l2', 't3', 'b1'),
        filename="transformed.svg",
        transforms=transforms
    )
    print(f"   Saved: {path}")

    # Variant grids
    print("\n3. Creating variant grids...")
    for rad_type in ['l', 't', 'b']:
        path = combiner.create_variant_grid('l0', rad_type)
        print(f"   {rad_type} variants: {path}")

    # Font generation
    print("\n4. Creating specimen sheet...")
    font_gen = GlyphFontGenerator("svg_font")
    path = font_gen.create_specimen_sheet(48)
    print(f"   Saved: {path}")

    print("\n" + "=" * 40)
    print("Demo complete!")


if __name__ == "__main__":
    demo()
