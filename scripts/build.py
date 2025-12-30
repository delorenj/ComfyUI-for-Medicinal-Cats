import os
import subprocess
import shutil

# Configuration
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_ROOT, "content")
CHAPTERS_DIR = os.path.join(CONTENT_DIR, "chapters")
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
OUTPUT_DIR = os.path.join(REPO_ROOT, "output")

def assemble_book():
    assembled_md = os.path.join(OUTPUT_DIR, "MANUAL_ASSEMBLED.md")
    
    # Order matters!
    chapters = sorted([f for f in os.listdir(CHAPTERS_DIR) if f.endswith(".md")])
    
    with open(assembled_md, "w") as out:
        # 1. Front Matter
        with open(os.path.join(CONTENT_DIR, "front_matter.md"), "r") as f:
            out.write(f.read())
            out.write("\n\n")
            
        # 2. Chapters with Image Injection
        for chapter in chapters:
            chapter_path = os.path.join(CHAPTERS_DIR, chapter)
            with open(chapter_path, "r") as f:
                content = f.read()
            
            # Perform image replacements (codifying the integration rules)
            content = process_images(chapter, content)
            
            # Add some spacing and a thematic header if missing
            out.write(f"\n\n<!-- START OF {chapter} -->\n\n")
            out.write(content)
            out.write("\n\n")
            
        # 3. Back Matter
        with open(os.path.join(CONTENT_DIR, "back_matter.md"), "r") as f:
            out.write(f.read())

    return assembled_md

def process_images(chapter_name, content):
    """Codifies the specific layout rules for each chapter"""
    # Map of placeholders to images (from SAMPLE_INTEGRATIONS.md)
    replacements = {
        "01_waking_up.md": [
            ("![ComfyUI Default Interface]", "![Dr. Nyquil Whiskerstein](images/01_cover_nyquil_cat_hero.png)"),
            ("## 🚨 Why Your Computer Hates You", "![Warning Poster](images/05_installation_warning_poster.png)\n\n## 🚨 Why Your Computer Hates You")
        ],
        "02_canvas.md": [
            ("## Understanding the Interface", "## Understanding the Interface\n\n![Dr. Nyquil Portrait](images/02_character_portrait_dr_whiskerstein.png)")
        ],
        "03_first_workflow.md": [
            ("[SCREENSHOT: Default workflow with all nodes visible]", "![Workflow Chart](images/03_workflow_medical_chart.png)"),
            ("**What is latent space?**", "**What is latent space?**\n\n![Latent Space Visualization](images/08_latent_space_dreamstate.png)")
        ],
        "04_model_zoo.md": [
            ("## Part 6: LoRAs Explained (The Flavor Packets)", "## Part 6: LoRAs Explained (The Flavor Packets)\n\n![LoRA Flavor Packets](images/07_lora_flavor_packets.png)"),
            ("## Part 8: VRAM Requirements (The Food Bowl Problem)", "## Part 8: VRAM Requirements (The Food Bowl Problem)\n\n![VRAM Food Bowl](images/04_vram_food_bowl_diagram.png)")
        ],
        "06_patterns.md": [
            ("## Common Node Combinations", "## Common Node Combinations\n\n![Workflow Patterns](images/06_prescription_patterns.png)")
        ]
    }
    
    if chapter_name in replacements:
        for old, new in replacements[chapter_name]:
            content = content.replace(old, new)
            
    # Fix image paths to be relative to the assembly file
    # Pandoc needs to find images relative to where it runs or absolute
    content = content.replace("images/", "../content/images/")
    
    return content

def build_pdf(assembled_md):
    output_pdf = os.path.join(OUTPUT_DIR, "ComfyUI_for_Medicinal_Cats.pdf")
    output_html = os.path.join(OUTPUT_DIR, "manual.html")
    
    print(f"Building HTML/PDF from {assembled_md}...")
    
    # Build HTML first (with CSS)
    subprocess.run([
        "pandoc", assembled_md,
        "-o", output_html,
        "--standalone",
        "--css", "../assets/manual.css",
        "--metadata", "title=ComfyUI for Medicinal Cats"
    ])
    
    # Print to PDF using Chromium (Headless)
    # We use the absolute path for the file to ensure Chromium finds it
    abs_html = os.path.abspath(output_html)
    subprocess.run([
        "chromium", "--headless", "--disable-gpu", 
        f"--print-to-pdf={output_pdf}", abs_html
    ])
    
    print(f"Success! Book generated at: {output_pdf}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = assemble_book()
    build_pdf(path)
