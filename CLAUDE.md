# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A themed technical manual about ComfyUI, written as pharmaceutical cat humor ("Dr. Nyquil Whiskerstein"). The repository codifies a Markdown-to-PDF publishing pipeline using Pandoc and Chromium.

## Build Commands

**Build the complete manual (HTML + PDF):**
```bash
python3 scripts/build.py
```

This generates:
- `output/MANUAL_ASSEMBLED.md` - Concatenated source with processed image references
- `output/manual.html` - Styled HTML output
- `output/ComfyUI_for_Medicinal_Cats.pdf` - Final PDF via Chromium headless print

**Prerequisites:**
- `pandoc` (Markdown processing)
- `chromium` (PDF generation via headless print)
- `python3` (build orchestration)

## Architecture

### Build Pipeline Flow

1. **Assembly** (`scripts/build.py:assemble_book()`):
   - Concatenates `front_matter.md` + sorted chapters + `back_matter.md`
   - Chapter ordering determined by numeric prefix (01_waking_up.md, 02_canvas.md, etc.)
   - Injects thematic images at codified anchor points via `process_images()`

2. **Image Processing** (`scripts/build.py:process_images()`):
   - **Critical**: Hardcoded mapping between chapter files and image insertion rules
   - Replaces placeholder text/headings with markdown image references
   - Transforms relative paths from `images/` to `../content/images/` for Pandoc resolution
   - Example: In `01_waking_up.md`, `![ComfyUI Default Interface]` becomes `![Dr. Nyquil...](images/01_cover...png)`

3. **Rendering**:
   - Pandoc generates standalone HTML with embedded CSS
   - Chromium headless converts HTML to PDF via `--print-to-pdf`

### Content Organization

```
content/
├── front_matter.md       # Title, license, foreword
├── back_matter.md        # Appendices, index
├── chapters/             # 8 chapters ordered by numeric prefix
│   ├── 01_waking_up.md       # Installation
│   ├── 02_canvas.md          # Interface overview
│   ├── 03_first_workflow.md  # Basic workflow tutorial
│   ├── 04_model_zoo.md       # Models, VAEs, LoRAs, VRAM
│   ├── 05_advanced_control.md
│   ├── 06_patterns.md        # Common node combinations
│   ├── 07_optimization.md
│   └── 08_beyond.md
└── images/               # 8 thematic illustrations
    ├── 01_cover_nyquil_cat_hero.png
    ├── 02_character_portrait_dr_whiskerstein.png
    ├── 03_workflow_medical_chart.png
    ├── 04_vram_food_bowl_diagram.png
    ├── 05_installation_warning_poster.png
    ├── 06_prescription_patterns.png
    ├── 07_lora_flavor_packets.png
    └── 08_latent_space_dreamstate.png
```

### Image Integration Rules

When modifying chapters or adding images, update the `replacements` dict in `scripts/build.py:process_images()`. Each chapter has specific anchor points where images are injected:

- Text replacement: Swaps placeholder text with image markdown
- Heading injection: Inserts image before/after specific headings
- Path transformation: All `images/` paths converted to `../content/images/` during assembly

**Example:**
```python
"01_waking_up.md": [
    ("![ComfyUI Default Interface]", "![Dr. Nyquil...](images/01_cover_nyquil_cat_hero.png)"),
    ("## 🚨 Why Your Computer Hates You", "![Warning Poster](images/05_installation_warning_poster.png)\n\n## 🚨 Why Your Computer Hates You")
]
```

## Key Design Principles

**Convention over Configuration:**
- Chapter order determined by filename prefix, not explicit config
- Image injection rules are Python code, not declarative templates
- Pandoc settings in `pandoc-defaults.yaml` supplement CLI args in build script

**Separation of Concerns:**
- Raw content in `content/` (Markdown, images)
- Presentation layer in `assets/manual.css`
- Build logic in `scripts/build.py`
- Generated artifacts in `output/`

**Thematic Coherence:**
- Maintain "pharmaceutical cat" voice (Dr. Nyquil Whiskerstein)
- Use medical/pharmaceutical metaphors (prescriptions, dosages, side effects)
- Chapter illustrations follow medicinal aesthetic

## Modifying Content

**To add/edit chapters:**
1. Create/modify file in `content/chapters/` with numeric prefix
2. Add image injection rules to `scripts/build.py:process_images()` if needed
3. Run `python3 scripts/build.py` to rebuild

**To update images:**
1. Place new image in `content/images/`
2. Update replacement rule in `scripts/build.py` to reference new image
3. Rebuild - layout integration is automatic

**To adjust styling:**
- Edit `assets/manual.css` (loaded by Pandoc's HTML output)
- CSS affects both HTML preview and PDF rendering
