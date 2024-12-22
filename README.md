# Glyph Generator

A Python application that procedurally generates unique glyphs by combining different radicals from a spritesheet. The generator can create up to 125 unique combinations using left, top, and bottom radical positions.


## Overview

> Real-time glyph generation using Pygame
> Combines three different radical positions (left, top, bottom)
> 5 different radical options for each position
> Simple command-line interface for generating new glyphs
> Total of 125 possible unique combinations


## Requirements

> Python 3.x
> Pygame
> Numpy

## Installation

### 1. Clone this repo:

```bash
git clone [repo-url]
cd glyph-gen
```
### 2. Install required packages (if needed)
```bash
pip install pygame numpy
```

### 3. Place the radical spritesheet(`radsheet1.png`) in the project directory of update the path in the code

If you are using your own spreadsheet, remember to update the radical dictionary and the self.locs as well as the sprite frame dimensions.

## Usage

### Run the program:

```bash
python glyph_generator.py
```


### Commands:


Type 'new' to generate a new glyph
Type 'quit' to exit the program
Close the window to exit

## Spritesheet Format
The spritesheet is currently formatted as follows:

Each sprite: 200px × 200px
Row 1: Left radicals (0-4)
Row 2: Top radicals (0-4)
Row 3: Bottom radicals (0-4)


## Project Structure

glyph-generator/
│
├── glyph_generator.py    # Main program file
├── radsheet1.png        # Spritesheet containing radicals
├── LICENSE             # MIT license
└── README.md           # This file

## How It Works
The generator uses a 5×3 spritesheet of radical components. Each glyph is composed of:

1 left radical (5 options)
1 top radical (5 options)
1 bottom radical (5 options)

Total possible combinations: 5³ = 125 unique glyphs

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

