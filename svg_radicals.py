"""
SVG Radical Path Definitions

This module defines SVG path data for glyph radicals.
Each radical is defined as an SVG path string that can be combined
with other radicals to form complete characters.

Path definitions use a 20x20 unit viewBox to match the original sprite dimensions.
"""

# Left radicals (l0-l9) - vertical strokes and left-side elements
LEFT_RADICALS = {
    'l0': {
        'path': 'M 4 2 L 4 18 M 4 10 L 8 10',
        'description': 'Single vertical with mid tick'
    },
    'l1': {
        'path': 'M 3 2 L 3 18 M 6 2 L 6 18',
        'description': 'Double vertical bars'
    },
    'l2': {
        'path': 'M 4 2 L 4 18 M 4 6 L 10 6 M 4 14 L 10 14',
        'description': 'Vertical with two horizontal ticks'
    },
    'l3': {
        'path': 'M 2 4 Q 8 4 8 10 Q 8 16 2 16',
        'description': 'Left curve bracket'
    },
    'l4': {
        'path': 'M 4 2 L 4 10 L 8 18',
        'description': 'Vertical with diagonal kick'
    },
    'l5': {
        'path': 'M 6 2 L 2 10 L 6 18 M 6 10 L 10 10',
        'description': 'Zigzag with horizontal'
    },
    'l6': {
        'path': 'M 3 4 L 3 16 M 3 4 L 8 4 M 3 16 L 8 16',
        'description': 'E-shape left'
    },
    'l7': {
        'path': 'M 4 2 C 4 8 8 8 8 14 L 4 18',
        'description': 'S-curve vertical'
    },
    'l8': {
        'path': 'M 2 2 L 8 2 L 8 18 L 2 18 Z',
        'description': 'Left box outline'
    },
    'l9': {
        'path': 'M 4 2 L 4 8 M 4 12 L 4 18 M 2 10 L 6 10',
        'description': 'Broken vertical with cross'
    }
}

# Top radicals (t0-t5) - horizontal strokes and top elements
TOP_RADICALS = {
    't0': {
        'path': 'M 2 4 L 18 4 M 10 4 L 10 10',
        'description': 'Horizontal with down tick'
    },
    't1': {
        'path': 'M 2 3 L 18 3 M 2 6 L 18 6',
        'description': 'Double horizontal lines'
    },
    't2': {
        'path': 'M 4 2 L 16 2 L 16 8 L 4 8 Z',
        'description': 'Top box'
    },
    't3': {
        'path': 'M 2 6 L 10 2 L 18 6',
        'description': 'Roof/chevron'
    },
    't4': {
        'path': 'M 4 4 L 16 4 M 6 4 L 6 10 M 14 4 L 14 10',
        'description': 'Horizontal with two down legs'
    },
    't5': {
        'path': 'M 4 2 Q 10 8 16 2 M 10 6 L 10 10',
        'description': 'Curved top with stem'
    }
}

# Bottom radicals (b0-b7) - bottom elements and bases
BOTTOM_RADICALS = {
    'b0': {
        'path': 'M 2 16 L 18 16 M 10 10 L 10 16',
        'description': 'Horizontal base with up stem'
    },
    'b1': {
        'path': 'M 4 12 L 4 18 L 16 18 L 16 12',
        'description': 'U-shape base'
    },
    'b2': {
        'path': 'M 2 18 L 10 12 L 18 18',
        'description': 'V-shape base'
    },
    'b3': {
        'path': 'M 4 14 L 16 14 M 4 18 L 16 18',
        'description': 'Double horizontal base'
    },
    'b4': {
        'path': 'M 2 12 L 18 12 L 18 18 L 2 18 Z',
        'description': 'Bottom box'
    },
    'b5': {
        'path': 'M 4 12 Q 10 20 16 12',
        'description': 'Curved bottom'
    },
    'b6': {
        'path': 'M 6 12 L 6 18 M 14 12 L 14 18 M 4 18 L 16 18',
        'description': 'Two legs with base'
    },
    'b7': {
        'path': 'M 2 14 L 10 18 L 18 14 M 10 10 L 10 18',
        'description': 'Inverted chevron with stem'
    }
}

# Combined dictionary for easy access
ALL_RADICALS = {
    'left': LEFT_RADICALS,
    'top': TOP_RADICALS,
    'bottom': BOTTOM_RADICALS
}


def get_radical_path(radical_id: str) -> str:
    """
    Get the SVG path data for a radical by its ID.

    Args:
        radical_id: Radical identifier (e.g., 'l0', 't1', 'b2')

    Returns:
        SVG path data string

    Raises:
        KeyError: If radical_id is not found
    """
    prefix = radical_id[0]
    radical_map = {
        'l': LEFT_RADICALS,
        't': TOP_RADICALS,
        'b': BOTTOM_RADICALS
    }

    if prefix not in radical_map:
        raise KeyError(f"Unknown radical prefix: {prefix}")

    if radical_id not in radical_map[prefix]:
        raise KeyError(f"Unknown radical: {radical_id}")

    return radical_map[prefix][radical_id]['path']


def get_radical_info(radical_id: str) -> dict:
    """
    Get full information about a radical.

    Args:
        radical_id: Radical identifier (e.g., 'l0', 't1', 'b2')

    Returns:
        Dictionary with 'path' and 'description' keys
    """
    prefix = radical_id[0]
    radical_map = {
        'l': LEFT_RADICALS,
        't': TOP_RADICALS,
        'b': BOTTOM_RADICALS
    }

    if prefix not in radical_map:
        raise KeyError(f"Unknown radical prefix: {prefix}")

    if radical_id not in radical_map[prefix]:
        raise KeyError(f"Unknown radical: {radical_id}")

    return radical_map[prefix][radical_id]


def list_radicals(radical_type: str = None) -> list:
    """
    List available radical IDs.

    Args:
        radical_type: 'left', 'top', 'bottom', or None for all

    Returns:
        List of radical IDs
    """
    if radical_type is None:
        return (list(LEFT_RADICALS.keys()) +
                list(TOP_RADICALS.keys()) +
                list(BOTTOM_RADICALS.keys()))

    type_map = {
        'left': LEFT_RADICALS,
        'top': TOP_RADICALS,
        'bottom': BOTTOM_RADICALS,
        'l': LEFT_RADICALS,
        't': TOP_RADICALS,
        'b': BOTTOM_RADICALS
    }

    if radical_type not in type_map:
        raise ValueError(f"Unknown radical type: {radical_type}")

    return list(type_map[radical_type].keys())
