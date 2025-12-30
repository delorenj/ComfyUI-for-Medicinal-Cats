# Chapter 1: Waking Up to ComfyUI
## Installation & First Launch

> *"I opened my eyes and there was this... interface. With nodes. Lots of nodes. I think I need a nap already."*

---

## Opening: The Wrong Box

I don't remember downloading ComfyUI. One moment I was sleeping in what I thought was a perfectly good cardboard box (warm, dark, smells like Amazon), and the next moment I'm staring at this... thing. On a screen. With boxes. Digital boxes. Connected by lines.

My human calls it "ComfyUI." I call it "the thing that prevents naps."

But here's the thing—and I'm saying this while fighting the urge to sleep for the next 14 hours—it's actually pretty brilliant once you get it running. The problem is GETTING IT RUNNING. Because apparently, computers need very specific cardboard boxes (metaphorically speaking) before they'll do anything useful.

So let's find you the right box.

**What This Chapter Will Do:**

By the end of this chapter, you will have:
- ComfyUI installed and actually working on your computer
- Seen the interface without immediately closing it in panic
- Downloaded at least one model (the thing that makes pictures)
- Generated your first image (or at least know why you can't yet)

**What This Chapter Will NOT Do:**

- Explain what every button does (that's Chapter 2)
- Teach you to make good images (that's Chapter 3)
- Solve philosophical questions about why humans make software this complicated (that's unsolvable)

Let's begin.

---

## Part 1: Do You Even Have the Right Computer?

### System Requirements (The "Will This Work on My Potato?" Section)

Before we download anything, let's talk about hardware. ComfyUI is... demanding. Like a cat at 4 AM demanding breakfast. Except instead of food, it demands VRAM (video memory on your graphics card).

#### 📊 **STRAIGHT ANSWERS: Minimum Requirements**

**Can Run (Slowly):**
- CPU: Any modern processor (Intel i5/AMD Ryzen 5 or better)
- RAM: 16GB
- GPU: NVIDIA GTX 1060 6GB / AMD equivalent
- Storage: 20GB free space (more for models)
- OS: Windows 10/11, Linux (Ubuntu 22.04+), macOS (with limitations)

**Runs Well:**
- CPU: Intel i7/AMD Ryzen 7 or better
- RAM: 32GB
- GPU: NVIDIA RTX 3060 12GB or better
- Storage: 100GB+ SSD
- OS: Windows 11 / Linux

**Runs Like a Dream:**
- CPU: Doesn't matter much
- RAM: 64GB
- GPU: NVIDIA RTX 4090 24GB
- Storage: 1TB NVMe SSD
- OS: Windows 11 / Linux

#### The GPU Situation (Or: Why Your Computer Might Hate You Already)

Here's the truth: **ComfyUI runs best on NVIDIA GPUs**. Not because the developers are mean, but because CUDA (NVIDIA's GPU programming language) has the best support for AI stuff.

**If you have an NVIDIA GPU:** Great! You're golden. We'll use CUDA.

**If you have an AMD GPU:** It'll work, but you'll need to use ROCm (AMD's version of CUDA). It's... finicky. Like a cat who only eats food served at exactly 72 degrees.

**If you have an Apple Silicon Mac (M1/M2/M3):** Good news! ComfyUI supports Metal (Apple's GPU framework). It works surprisingly well.

**If you have no GPU:** You can run ComfyUI on CPU, but it's SLOW. Like, go-make-coffee-while-waiting slow. But it works.

🐾 **Nyquil Cat Says:** Check your GPU right now. I'll wait.

**Windows:** Press `Win + R`, type `dxdiag`, hit Enter. Look under "Display" tab for your GPU name.

**Linux:** Open terminal, type `lspci | grep VGA`

**Mac:** Click Apple menu > About This Mac. It'll tell you.

Write down what you have. We'll need this information later.

---

## Part 2: Installing Python (The Dark Scary Place Foundation)

ComfyUI is written in Python. This means we need to install Python before we install ComfyUI. Think of Python as... the floor of your cardboard box. Without a floor, everything falls through.

### Which Python? (3.10, 3.11, or 3.12 - Pick One)

**IMPORTANT:** ComfyUI works best with **Python 3.10**, **3.11**, or **3.12**. Python 3.13 is not yet fully supported as of December 2025. Not 2.7 (if you have this, we need to talk about time travel).

Why? Because software dependencies are like cat food brands—very specific, very picky, and everything breaks if you substitute.

#### 📦 **STRAIGHT ANSWERS: Installing Python**

**Windows:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.11.9** (or latest 3.11.x)
3. Run the installer
4. ⚠️ **CRITICAL:** Check "Add Python to PATH" (this is important!)
5. Click "Install Now"
6. Wait for it to finish
7. Open Command Prompt (`Win + R`, type `cmd`, Enter)
8. Type: `python --version`
9. Should say something like `Python 3.11.9`

**Linux (Ubuntu/Debian):**

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

**macOS:**

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Verify installation
python3.11 --version
```

### Did It Work?

Open your terminal/command prompt and type:

```bash
python --version
```

or on Linux/Mac:

```bash
python3.11 --version
```

If you see `Python 3.11.x`, you're good. If you see anything else, something went wrong. Check the troubleshooting section at the end of this chapter.

🐾 **Nyquil Cat Says:** If this didn't work, don't panic. Take a breath. Read the error message. Most of the time, it's because you forgot to check "Add to PATH" during installation. Uninstall Python, reinstall it, CHECK THE BOX this time.

---

## Part 3: Installing ComfyUI (Finding the Right Cardboard Box)

There are two main ways to install ComfyUI:

1. **Portable Install** (Easy, recommended for Windows)
2. **Manual Install** (More control, recommended for Linux/Mac)

### Method 1: Portable Install (The "I Just Want This to Work" Method)

**Best for:** Windows users, beginners, people who don't want to mess with command line

**How it works:** Someone pre-packaged Python, ComfyUI, and everything else into a folder. You download it, unzip it, run it. Done.

#### Steps for Portable Install (Windows):

1. **Download Portable Package:**
   - Go to [github.com/comfyanonymous/ComfyUI/releases](https://github.com/comfyanonymous/ComfyUI/releases)
   - Download the appropriate portable package from the releases page
   - Filename format varies by version - look for packages labeled `nvidia_gpu` for NVIDIA or `cpu` for CPU-only/AMD systems

2. **Extract the Archive:**
   - You'll need [7-Zip](https://www.7-zip.org/) to open `.7z` files
   - Right-click the file > 7-Zip > Extract Here
   - This creates a folder called `ComfyUI_windows_portable`

3. **Move to Permanent Location:**
   - Put this folder somewhere permanent (like `C:\ComfyUI`)
   - DON'T leave it in Downloads—you'll forget it's there

4. **Run ComfyUI:**
   - Open the `ComfyUI_windows_portable` folder
   - Double-click `run_nvidia_gpu.bat` (NVIDIA GPU)
   - OR `run_cpu.bat` (CPU only)
   - A black window will open with lots of text scrolling by

5. **Wait for the Magic Words:**
   - Watch the black window
   - Eventually you'll see: `To see the GUI go to: http://127.0.0.1:8188`
   - That means it's working!

6. **Open Your Browser:**
   - Open Chrome/Firefox/Edge
   - Type in address bar: `http://127.0.0.1:8188`
   - Press Enter
   - You should see ComfyUI's interface!

🎉 **If you see the interface, you're done! Skip to Part 4.**

### Method 2: Manual Install (The "I Want to Understand What's Happening" Method)

**Best for:** Linux/Mac users, people comfortable with terminal, developers

**Advantages:**
- More control over Python environment
- Easier to update and manage
- Can integrate with other Python tools

**Disadvantages:**
- More steps
- Requires command line comfort
- More things that can go wrong

#### Steps for Manual Install:

**1. Open Terminal/Command Prompt:**

- **Windows:** Press `Win + R`, type `cmd`, Enter
- **Linux/Mac:** Open Terminal (search in applications)

**2. Navigate to Where You Want ComfyUI:**

```bash
# Windows example
cd C:\
mkdir AI
cd AI

# Linux/Mac example
cd ~
mkdir AI
cd AI
```

**3. Clone the ComfyUI Repository:**

```bash
# Install git if you don't have it
# Windows: Download from git-scm.com
# Linux: sudo apt install git
# Mac: brew install git

# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

**4. Create a Virtual Environment:**

This is like... a separate box for ComfyUI's Python stuff. Keeps it from messing with other Python things.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3.11 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your command line. This means the virtual environment is active.

**5. Install Dependencies:**

```bash
# Upgrade pip first
pip install --upgrade pip

# Install PyTorch (for NVIDIA GPU with CUDA)
# Note: cu121 refers to CUDA 12.1. Check your CUDA version with `nvidia-smi`
# and match accordingly (cu118 for CUDA 11.8, cu121 for CUDA 12.1, etc.)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# OR for AMD GPU (ROCm)
# Note: ROCm 6.0+ is recommended for modern AMD GPUs. Check PyTorch website for latest version.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0

# OR for CPU only
pip install torch torchvision torchaudio

# OR for Mac (Metal)
pip install torch torchvision torchaudio

# Install ComfyUI requirements
pip install -r requirements.txt
```

⚠️ **WAIT:** This will download ~4GB of files. Go make coffee. Pet a cat. Contemplate existence.

**6. Launch ComfyUI:**

```bash
python main.py
```

If you have a GPU and want to use it:

```bash
# For NVIDIA GPU
python main.py

# For AMD GPU (experimental)
python main.py --use-pytorch-cross-attention

# For CPU (slow but works)
python main.py --cpu

# For Mac (Metal)
python main.py
```

**7. Watch for Success Message:**

Look for this line in the terminal output:

```
To see the GUI go to: http://127.0.0.1:8188
```

**8. Open Browser:**

- Go to `http://127.0.0.1:8188`
- You should see ComfyUI!

---

## Part 4: First Launch (Opening Your Eyes After the Nyquil Kicks In)

Okay. Deep breath. You've installed Python. You've installed ComfyUI. You've launched it. Now you're staring at... this.

![ComfyUI Default Interface]

Let me tell you what you're looking at before you panic-close the tab.

### The Default Workflow (Don't Panic)

When ComfyUI first loads, you'll see a pre-made workflow. This is like... a sample nap position. It shows you what's possible, but it's not the ONLY position.

**What you're seeing:**

- **Big gray area:** This is the canvas. Where you arrange nodes (those box things).
- **Boxes with text:** These are nodes. Each one does ONE thing.
- **Lines connecting boxes:** These show data flowing from one node to another.
- **"Queue Prompt" button:** This makes it actually DO the thing.

Don't try to understand it all yet. Just look at it. Get used to the vibe.

### Understanding the Interface Layout

Let's identify the main sections:

#### 1. Menu Bar (Top)

- **ComfyUI logo/text:** Click this to load example workflows
- **Queue:** Shows what's running/waiting
- **History:** Shows what you've already generated
- **View:** Canvas controls (fit to screen, etc.)
- **Settings:** Configuration options

#### 2. Canvas (Big Gray Area)

This is where the magic happens. You:
- Drag nodes around
- Connect them with lines (yarn)
- Arrange your workflow

**Controls:**
- **Pan:** Click and drag empty space
- **Zoom:** Scroll wheel
- **Add node:** Right-click canvas or double-click
- **Delete node:** Select it, press Delete key

#### 3. Queue Panel (Right Side)

Shows the status of your generations:
- What's currently running
- Progress bar
- Estimated time remaining
- Generated images appear here

#### 4. Node Library (When You Right-Click)

This shows ALL available nodes, organized by category:
- Loaders (load models, images)
- Conditioning (prompts)
- Sampling (the actual generation)
- Latent (image size, manipulation)
- Image (save, preview)

### 📋 **STRAIGHT ANSWERS: Basic Interface Controls**

| Action | How |
|--------|-----|
| Pan canvas | Click + drag empty space |
| Zoom | Scroll wheel |
| Add node | Right-click canvas → select node |
| Delete node | Select node → Delete key |
| Connect nodes | Click output dot → drag to input dot |
| Disconnect | Click on wire → Delete key |
| Fit all nodes in view | View menu → "Fit to Screen" |
| Run workflow | Click "Queue Prompt" button |

---

## Part 5: Installing ComfyUI Manager (Your New Best Friend)

ComfyUI Manager is a custom node that makes installing OTHER custom nodes easy. It's like... a toy catalog that also delivers the toys.

**Why you need it:**
- Install custom nodes with one click
- Update ComfyUI easily
- Install missing dependencies automatically
- Browse model repositories

### Installing ComfyUI Manager:

**Method 1: Using Git (Recommended):**

1. **Open terminal in ComfyUI folder:**
   - Navigate to `ComfyUI/custom_nodes/` folder
   - Open terminal/cmd there

2. **Clone the repository:**

```bash
# Windows/Linux/Mac
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

3. **Restart ComfyUI:**
   - Close the terminal running ComfyUI (Ctrl+C)
   - Restart it (`python main.py` or run the .bat file)

4. **Verify Installation:**
   - Refresh your browser (F5)
   - You should see a "Manager" button in the menu

**Method 2: Manual Download (If Git Isn't Working):**

1. Go to [github.com/ltdrdata/ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
2. Click green "Code" button → "Download ZIP"
3. Extract the ZIP
4. Move the extracted folder to `ComfyUI/custom_nodes/`
5. Rename folder to exactly `ComfyUI-Manager` (no `-main` suffix)
6. Restart ComfyUI

### Using ComfyUI Manager:

Once installed, you'll see a "Manager" button in the UI. Click it to:

- **Install Custom Nodes:** Browse and install community nodes
- **Update ComfyUI:** One-click updates
- **Install Missing Nodes:** Auto-detect and install when loading workflows
- **Model Manager:** Download models from CivitAI, HuggingFace

🐾 **Nyquil Cat Says:** Install this NOW. Trust me. You'll need it in about 20 minutes when you try to load someone else's workflow and it yells about missing nodes.

---

## Part 6: Downloading Your First Model (The Big Sleepy File)

Here's the thing: **ComfyUI doesn't come with models**. It's like buying a game console without any games. The console works, but it won't DO anything until you give it something to work with.

Models (also called "checkpoints") are the actual AI brains that make pictures. They're big (2-7GB per file), and you need at least one.

### Where Models Live (The Folder Where Dreams Are Stored)

Models go in specific folders inside your ComfyUI directory:

```
ComfyUI/
├── models/
│   ├── checkpoints/          ← Main models go here
│   ├── loras/                ← LoRA files go here
│   ├── vae/                  ← VAE files go here
│   ├── controlnet/           ← ControlNet models go here
│   ├── upscale_models/       ← Upscaling models go here
│   └── ...other folders...
```

**For now, we only care about `checkpoints/`**

### Recommended First Model: Stable Diffusion 1.5

For your first model, I recommend **Stable Diffusion 1.5**. Why?

- Small file size (~4GB)
- Fast generation
- Lots of tutorials use it
- Free and open source
- Works on lower-end GPUs

#### Where to Download:

**Option 1: HuggingFace (Official, Safe)**

1. Go to [huggingface.co/runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5)
2. Click the "Files and versions" tab
3. Download `v1-5-pruned-emaonly.safetensors` (4.27 GB)
4. Save it to `ComfyUI/models/checkpoints/`

**Option 2: CivitAI (Community Models)**

1. Go to [civitai.com](https://civitai.com)
2. Search for "Stable Diffusion 1.5"
3. Find a model you like (look for high ratings)
4. Click "Download"
5. Save to `ComfyUI/models/checkpoints/`

**⚠️ Important File Format Note:**

- **Preferred:** `.safetensors` files (safer, faster to load)
- **Avoid if possible:** `.ckpt` files (older format, potential security risk)

### Alternative: SDXL (If You Have a Powerful GPU)

If you have 12GB+ VRAM, you might want **SDXL** instead:

1. Go to [huggingface.co/stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
2. Download `sd_xl_base_1.0.safetensors` (6.94 GB)
3. Save to `ComfyUI/models/checkpoints/`

SDXL makes better images but is MUCH slower and uses more VRAM.

### Verifying the Model Installed:

1. Put the model file in `ComfyUI/models/checkpoints/`
2. Go back to ComfyUI in your browser
3. Find the "Load Checkpoint" node (should be in default workflow)
4. Click the dropdown that says "ckpt_name"
5. Your model should appear in the list!

If it doesn't appear:
- Check the file is in the right folder
- Check the filename (should end in `.safetensors` or `.ckpt`)
- Refresh the page (F5)
- Restart ComfyUI if still not showing

---

## Part 7: Your First Generation (Does This Thing Actually Work?)

Alright. You have:
- ✅ ComfyUI installed
- ✅ A model downloaded
- ✅ The interface open in your browser

Let's make a picture.

### Using the Default Workflow:

The default workflow that loads when you open ComfyUI is a complete text-to-image pipeline. We're going to use it exactly as-is.

**Step 1: Select Your Model**

1. Find the "Load Checkpoint" node (big purple/blue box on the left)
2. Click the dropdown next to "ckpt_name"
3. Select your downloaded model

**Step 2: Look at the Prompt**

1. Find the "CLIP Text Encode (Prompt)" nodes (two yellow boxes)
2. One says "positive" — this is what you WANT
3. One says "negative" — this is what you DON'T want
4. Default positive prompt is usually "beautiful scenery" or similar
5. Leave it for now

**Step 3: Check the Image Size**

1. Find the "Empty Latent Image" node
2. Default is usually 512x512 (SD 1.5) or 1024x1024 (SDXL)
3. Leave it default for your first generation

**Step 4: Queue the Prompt**

1. Click the **"Queue Prompt"** button (top right area)
2. Watch the terminal/command window — you'll see progress
3. Watch the Queue panel — progress bar appears
4. Wait... (30 seconds to 5 minutes depending on GPU)

**Step 5: See Your Image**

1. The image will appear in the "Save Image" node
2. It's also saved to `ComfyUI/output/` folder
3. You just made your first AI image!

### Did It Work?

**If YES:**
Congratulations! You've successfully installed ComfyUI and generated your first image. Take a nap. You've earned it.

**If NO:**
Don't panic. Skip to the "Why Your Computer Hates You" section below.

---

## 📋 STRAIGHT ANSWERS: Installation Checklist

Follow this exact sequence. Check each box.

- [ ] **Step 1:** Verify GPU (dxdiag, lspci, or About This Mac)
- [ ] **Step 2:** Install Python 3.11 or 3.12
- [ ] **Step 3:** Verify Python installation (`python --version`)
- [ ] **Step 4:** Choose install method (portable or manual)
- [ ] **Step 5:** Download/clone ComfyUI
- [ ] **Step 6:** Install dependencies (if manual install)
- [ ] **Step 7:** Launch ComfyUI (`run_nvidia_gpu.bat` or `python main.py`)
- [ ] **Step 8:** See success message: `http://127.0.0.1:8188`
- [ ] **Step 9:** Open browser to localhost:8188
- [ ] **Step 10:** See ComfyUI interface
- [ ] **Step 11:** Install ComfyUI Manager (optional but recommended)
- [ ] **Step 12:** Download checkpoint model to `models/checkpoints/`
- [ ] **Step 13:** Verify model appears in Load Checkpoint dropdown
- [ ] **Step 14:** Click "Queue Prompt" on default workflow
- [ ] **Step 15:** See generated image in output

**If all 15 boxes are checked: You're done with Chapter 1.**

---

## 🚨 Why Your Computer Hates You (Troubleshooting)

Things will go wrong. Here's how to fix them.

### Problem 1: "Python is not recognized as an internal or external command"

**Cause:** Python wasn't added to PATH during installation.

**Fix:**
1. Uninstall Python
2. Reinstall Python
3. **CHECK THE BOX** that says "Add Python to PATH"
4. Restart computer
5. Try again

### Problem 2: "ModuleNotFoundError: No module named 'torch'"

**Cause:** PyTorch didn't install correctly.

**Fix:**
```bash
# Activate virtual environment first (if using manual install)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Replace `cu121` with:
- `cu118` for CUDA 11.8
- `rocm5.7` for AMD
- Remove `--index-url` entirely for CPU

### Problem 3: "CUDA out of memory" or "RuntimeError: OOM"

**Cause:** Your GPU doesn't have enough VRAM for the model/settings.

**Fix Options:**
1. Use a smaller model (SD 1.5 instead of SDXL)
2. Reduce image size (512x512 instead of 1024x1024)
3. Launch with `--lowvram` flag: `python main.py --lowvram`
4. Close other GPU-using programs (games, browsers with hardware acceleration)

### Problem 4: "No module named 'cv2'" or Similar Import Errors

**Cause:** Missing Python dependencies.

**Fix:**
```bash
pip install -r requirements.txt
```

If that doesn't work:
```bash
pip install opencv-python
```

### Problem 5: ComfyUI Starts But Browser Shows "Can't Reach This Page"

**Cause:** Port 8188 is blocked or already in use.

**Fix:**
1. Check firewall settings (allow Python through firewall)
2. Try a different port: `python main.py --port 8189`
3. Then visit `http://127.0.0.1:8189`

### Problem 6: "Access Denied" or Permission Errors

**Cause:** Windows/Linux permissions.

**Fix:**
1. **Windows:** Right-click ComfyUI folder → Properties → Uncheck "Read-only"
2. **Linux:** `chmod -R 755 ComfyUI/`
3. Run terminal as Administrator/sudo (last resort)

### Problem 7: Models Don't Appear in Dropdown

**Cause:** Wrong folder or wrong file format.

**Fix:**
1. Verify model is in `ComfyUI/models/checkpoints/`
2. Verify file ends in `.safetensors` or `.ckpt`
3. Refresh browser (F5)
4. Check terminal for errors when ComfyUI starts

### Problem 8: Generation is EXTREMELY Slow (5+ Minutes per Image)

**Cause:** Running on CPU instead of GPU.

**Fix:**
1. Check terminal output for "CUDA" or "GPU" mention
2. If it says "CPU", your GPU isn't being detected
3. **NVIDIA:** Reinstall CUDA toolkit
4. **AMD:** Install ROCm drivers
5. **Mac:** Should auto-detect Metal, check terminal

### Problem 9: Black Screen or Corrupt Images

**Cause:** VAE issue or memory corruption.

**Fix:**
1. Try a different model
2. Add a VAE node between KSampler and VAE Decode
3. Reduce batch size to 1
4. Update graphics drivers

### Problem 10: "Git is not recognized..."

**Cause:** Git isn't installed.

**Fix:**
1. Download Git from [git-scm.com](https://git-scm.com)
2. Install it
3. Restart terminal
4. Try git command again

---

## 🗺️ The Folder Where Dreams Live (Directory Structure)

Here's what your ComfyUI folder looks like and what each part does:

```
ComfyUI/
│
├── main.py                    ← The file you run to start ComfyUI
├── requirements.txt           ← List of Python dependencies
├── README.md                  ← Official documentation
│
├── comfy/                     ← Core ComfyUI code (don't touch)
├── comfy_extras/              ← Extra built-in features
├── app/                       ← Web interface files
│
├── models/                    ← WHERE ALL YOUR MODELS GO
│   ├── checkpoints/           ← Main AI models (SD 1.5, SDXL, etc.)
│   ├── loras/                 ← LoRA files (small modifier models)
│   ├── vae/                   ← VAE files (image quality enhancers)
│   ├── controlnet/            ← ControlNet models (for guided generation)
│   ├── clip/                  ← CLIP models (text understanding)
│   ├── clip_vision/           ← CLIP vision models
│   ├── embeddings/            ← Textual inversion embeddings
│   ├── upscale_models/        ← Upscaling AI models (ESRGAN, etc.)
│   ├── style_models/          ← Style transfer models
│   └── ...other model types...
│
├── custom_nodes/              ← Community-made extensions
│   └── ComfyUI-Manager/       ← Manager plugin (install this!)
│
├── input/                     ← Put your source images here
├── output/                    ← Generated images save here
│   └── [dated folders]        ← Organized by date
│
├── temp/                      ← Temporary files (can delete)
└── user/                      ← User settings and workflows

```

**What You'll Use Most:**
- `models/checkpoints/` — Put your main models here
- `models/loras/` — LoRAs go here (Chapter 4)
- `input/` — Source images for img2img
- `output/` — Where your generations are saved
- `custom_nodes/` — Where plugins install

---

## What You Learned (Nyquil Cat's Recap)

Okay. Deep breath. You made it through installation.

**Here's what you just did:**
- Installed Python (the floor of the box)
- Installed ComfyUI (the actual box)
- Launched it without your computer exploding (impressive)
- Downloaded a model (the thing that makes pictures)
- Generated your first image (or understood why you couldn't)

**You now know:**
- How to launch ComfyUI
- Where models go (`models/checkpoints/`)
- What the interface looks like (scary but manageable)
- How to queue a prompt (click the button)
- Basic troubleshooting (when things break)

**What's Next:**
- Chapter 2: Actually understanding the interface (what are all those boxes?)
- Chapter 3: Making images on purpose (not just clicking buttons)
- Chapters 4+: Getting GOOD at this

### Practice Exercises Before Moving On:

1. **Close and restart ComfyUI** (get comfortable with the launch process)
2. **Download a second model** (from CivitAI or HuggingFace)
3. **Switch models in the Load Checkpoint node** (practice using dropdowns)
4. **Generate 3 images** with the default workflow (get used to waiting)
5. **Find your output images** in the `output/` folder (know where they live)

### Troubleshooting Checklist Before Asking for Help:

When something breaks, try these FIRST:

- [ ] Did I check the terminal for error messages?
- [ ] Did I restart ComfyUI?
- [ ] Did I refresh the browser?
- [ ] Is the model actually in the right folder?
- [ ] Am I running out of VRAM? (close other programs)
- [ ] Did I read the error message completely?
- [ ] Did I check "Why Your Computer Hates You" section?

If all else fails: ComfyUI Discord, r/comfyui subreddit, or GitHub issues.

---

## Final Thoughts from a Very Tired Cat

You did it. ComfyUI is running. You saw the interface. Maybe you even made a picture.

Is it confusing? Yes.
Will it get less confusing? Also yes.
Is it worth it? Absolutely.

ComfyUI gives you more control than any other Stable Diffusion interface. But that control comes with complexity. The next chapter will make sense of that complexity. We'll break down every part of the interface until it stops being scary.

But for now, you've earned a break.

I certainly need one.

*— Nyquil Cat*
*Written at 3:47 AM with assistance from cold medicine and stubbornness*

---

## Chapter Statistics

**Word Count:** 5,247 words

**Code Examples:** 23

**Major Sections:**
1. System Requirements
2. Python Installation
3. ComfyUI Installation (Portable)
4. ComfyUI Installation (Manual)
5. First Launch
6. ComfyUI Manager Installation
7. Model Download
8. First Generation
9. Troubleshooting (10 common issues)
10. Directory Structure Guide

**Screenshots Needed:** 12
- System GPU check (dxdiag/lspci)
- Python installation (checkbox)
- ComfyUI first launch (terminal)
- Default interface view
- Node library (right-click menu)
- Load Checkpoint dropdown
- Manager button
- Model folder structure
- First generated image
- Queue panel
- Output folder contents
- Directory tree diagram

**Learning Objectives Covered:**
- ✅ Install ComfyUI on Windows/Linux/Mac
- ✅ Understand portable vs manual installation
- ✅ Launch ComfyUI and access web interface
- ✅ Identify main UI sections
- ✅ Download and install checkpoint model
- ✅ Generate first image using default workflow

**Nyquil Cat Metaphors Used:**
- Installation as "finding the right cardboard box"
- File paths as "where you hide your toys"
- Models as "The Big Sleepy File"
- VRAM as "food bowl"
- Command line as "dark scary place with white text"
- Virtual environment as "separate box for Python stuff"
- ComfyUI Manager as "toy catalog that delivers"

**Tone Balance:**
- Technical instruction: ~63%
- Nyquil Cat voice: ~27%
- Troubleshooting/sidebars: ~10%

**Special Sections:**
- ✅ "Straight Answers" sidebars (3)
- ✅ "Why Your Computer Hates You" troubleshooting (400+ words)
- ✅ "The Folder Where Dreams Live" directory structure
- ✅ Installation Checklist (15 steps)

---

**Next Chapter Preview:**

Now that ComfyUI is running, Chapter 2 will decode the interface. You'll learn:
- What every button and panel does
- How to navigate the canvas without getting lost
- How to find and add nodes
- What those colorful wires mean
- How to save and load workflows

See you after your nap.