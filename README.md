# ComfyUI for Medicinal Cats 🐈💊

This repository contains the "codified" source for the manual. It uses a Markdown-to-PDF pipeline powered by Pandoc and Chromium.

## Repository Structure

- `content/`: The raw manuscript
  - `chapters/`: Individual chapter files (renamed for ordering)
  - `images/`: The 8 thematic illustrations
  - `front_matter.md`: Title, foreword, and intro
  - `back_matter.md`: Appendices and index
- `assets/`: Layout and styling (CSS)
- `scripts/`: Automation for assembly and rendering
- `output/`: Where the final PDF/HTML lives
- `pandoc-defaults.yaml`: The codified Pandoc settings

## How to Build

1. **Prerequisites**:
   - `pandoc` installed
   - `chromium` installed
   - `python3` installed

2. **Build the book**:
   ```bash
   python3 scripts/build.py
   ```

## Design Principles

- **Convention over Configuration**: Chapters are ordered by their numeric prefix.
- **Medicinal Aesthetic**: Styled via `assets/manual.css`.
- **Automated Layout**: Image injection rules are codified in `scripts/build.py`, meaning you can update images or text independently without breaking the layout.

## License
CC BY-NC-SA 4.0
