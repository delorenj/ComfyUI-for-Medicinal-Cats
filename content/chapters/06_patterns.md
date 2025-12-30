# Chapter 6: Workflow Patterns (Common Node Combinations)

> *"Turns out, there are... patterns. Recipes. Like, specific mouse arrangements that always work. This is suspiciously organized."*

## The Pattern Recognition Moment

*Nyquil Cat voice:*

I've been staring at workflows for... how long? Days? Weeks? Time is weird when you nap constantly. But something clicked during my seventeenth nap yesterday.

The nodes aren't random.

I mean, I KNEW they weren't random. But I thought each workflow was unique—like each nap position is unique depending on sunbeam angle and how judgmental the humans are being.

But no. There are **patterns**. Actual, repeatable patterns. The same mouse arrangements show up over and over. Text-to-image? Same five nodes, always. Upscaling? Same three-node combo every time. It's like... recipes. For pictures.

This is either brilliantly organized or I'm having a lucid dream. Either way, let's document these patterns before I forget them.

---

## What This Chapter Covers

**You're going to learn:**
- The 8 most common workflow patterns that solve 90% of use cases
- How to recognize patterns in the wild (someone else's workflow)
- How to adapt patterns for your specific needs
- How to save and reuse patterns as templates
- How to combine multiple patterns into mega-workflows

**By the end, you'll have:**
- A library of 10 ready-to-use workflow templates
- The ability to look at ANY workflow and understand its structure
- Confidence to modify patterns without breaking everything
- A mental model of "this is an upscaling pattern" vs "this is img2img"

Think of this chapter as your recipe book. You're not learning to cook from scratch (that was Chapters 1-5). You're learning the classic recipes that every chef knows by heart.

---

## 📚 Sidebar: Straight Answers - What Are Workflow Patterns?

**Workflow Pattern:** A proven combination of nodes that solves a specific problem. Like design patterns in programming, these are standardized solutions to common challenges.

**Why patterns matter:**
- **Speed:** Don't reinvent the wheel; start with known-good structure
- **Reliability:** Patterns are battle-tested by the community
- **Understanding:** Recognizing patterns helps you read others' workflows
- **Remixing:** Combine patterns to create novel workflows

**Core patterns covered:**
1. Text-to-Image (T2I) - The foundation
2. Image-to-Image (I2I) - Redream existing images
3. Highres Fix - Two-pass quality boost
4. Upscaling - ESRGAN detail enhancement
5. Batch Processing - Multiple variations
6. Tiling - Seamless textures
7. Animation - Frame consistency
8. Workflow Snippets - Saving/reusing sub-patterns

---

## Pattern #1: Text-to-Image (The Foundation)

*Nyquil Cat voice:*

You already know this one. It's the default workflow. The "hello world" of image generation. But let's see it as a **pattern** now—a template you can adapt infinitely.

### The Core T2I Pattern

**Node sequence:**
```
Load Checkpoint → CLIP Text Encode (positive) ──┐
                  CLIP Text Encode (negative) ──┤
                  Empty Latent Image ─────────────┤
                                                  ├→ KSampler → VAE Decode → Save Image
```

**What makes this a pattern:**
- **Entry point:** Always starts with checkpoint loading
- **Dual conditioning:** Positive and negative prompts feed the sampler
- **Latent creation:** Empty latent defines resolution/batch
- **Sampling:** The actual image generation happens here
- **Decoding:** Latent → pixels via VAE
- **Output:** Save node captures result

### Pattern Variations

**Same pattern, different flavors:**

1. **SDXL version:** Adds second CLIP Text Encode for refiner model
2. **Flux version:** Different checkpoint, same pattern structure
3. **LoRA-enhanced:** Insert "Load LoRA" node between checkpoint and CLIP
4. **Multi-prompt:** Stack multiple CLIP encodes with conditioning combiners

**The pattern stays the same. The ingredients change.**

### When to Use This Pattern

- Starting a new image from scratch
- Exploring prompt variations
- Testing different models/samplers
- Teaching someone ComfyUI (this is your "hello world")

### 💡 Cat's Wisdom: The Pattern Recognition Trick

When you load someone else's workflow and it looks like spaghetti yarn, find the **KSampler**. Trace backwards to see what's feeding it. That tells you the pattern type.

KSampler getting fed CLIP + Empty Latent? → Text-to-Image pattern
KSampler getting fed CLIP + Loaded Image? → Image-to-Image pattern
KSampler getting fed through two passes? → Highres Fix pattern

The sampler is the heart. Everything else is arteries feeding it.

---

## Pattern #2: Image-to-Image (Redreaming Reality)

*Nyquil Cat voice:*

Img2img is the pattern for when you have a picture and want to... dream it differently. Like when I see a cardboard box and imagine it as a luxury penthouse. Same box. Different dream.

### The Core I2I Pattern

**Node sequence:**
```
Load Checkpoint → CLIP Text Encode (positive) ──┐
                  CLIP Text Encode (negative) ──┤
                  Load Image ──→ VAE Encode ────┤
                                                 ├→ KSampler (denoise < 1.0) → VAE Decode → Save Image
```

**Key differences from T2I:**
- **Load Image** replaces Empty Latent Image
- **VAE Encode** converts loaded image to latent space
- **Denoise strength** < 1.0 (usually 0.4-0.7)
  - 0.3 = subtle changes, keep original structure
  - 0.7 = major changes, loose interpretation
  - 1.0 = basically T2I (ignores input image)

### The Denoise Spectrum

**Understanding denoise strength:**

```
Denoise 0.0 ──────────────────────────────── Denoise 1.0
   │                                              │
Original image unchanged              Completely new image
   │                                              │
Low creativity ←──────────────────────→ High creativity
Faithful to input                     Ignores input
```

**Practical examples:**
- **0.2-0.3:** Color correction, style tweaks (face stays same)
- **0.4-0.5:** Artistic reinterpretation (face changes but pose stays)
- **0.6-0.7:** Loose inspiration (uses composition, reimagines everything)
- **0.8-0.9:** Almost T2I (why are you even using img2img?)

### When to Use This Pattern

- You have a rough sketch/photo to refine
- Style transfer (realistic photo → anime version)
- Iteration (take output, feed back as input with tweaked prompt)
- Fixing specific issues in generated images
- "Make this, but different"

### 🎨 Pattern Remix: Style Transfer I2I

**Advanced variation:**
```
Load Image ──→ VAE Encode ──┐
                             ├→ KSampler (denoise 0.6) → VAE Decode → Save
Load Checkpoint (style model) ──→ CLIP (style prompt) ──┘
```

Load a photo with an anime checkpoint and prompt. Denoise at 0.5-0.6. You get anime version of your photo. Same pattern, creative application.

---

## Pattern #3: Highres Fix (The Two-Pass Quality Boost)

*Nyquil Cat voice:*

Here's the thing about generating large images directly: it often looks... weird. Off. Like when you wake up from a nap and your face is doing something geometrically improbable.

Highres Fix solves this by dreaming in two stages:
1. Small, coherent image
2. Upscale + refine at low denoise

It's like taking a quick nap (rough draft) then a long nap (polished version). Two naps are better than one confused giant nap.

### The Core Highres Fix Pattern

**Node sequence:**
```
[FIRST PASS - Low Resolution]
Checkpoint → CLIP → Empty Latent (512x512) → KSampler → VAE Decode ──┐
                                                                       │
[SECOND PASS - High Resolution]                                       │
Same Checkpoint → Same CLIP → Latent Upscale (x2) ←── VAE Encode ←──┘
                                  ↓
                              KSampler (denoise 0.4-0.5) → VAE Decode → Save
```

**Why this works:**
- **First pass:** Model generates coherent composition at native training resolution (usually 512x512 or 1024x1024 for SDXL)
- **Second pass:** Upscaled latent gets refined with low denoise, adding detail without changing composition

**Common mistake:** Using high denoise in second pass → completely regenerates image, ignoring first pass. Use 0.3-0.5 max.

### Highres Fix Variations

**Latent Upscale vs Pixel Upscale:**

```
METHOD 1: Latent Upscale (faster, softer)
VAE Decode → VAE Encode → Latent Upscale → KSampler

METHOD 2: Pixel Upscale + Encode (sharper, more control)
VAE Decode → Image Scale (bilinear/bicubic) → VAE Encode → KSampler
```

**Latent upscale** works directly in latent space (fast, smooth). **Pixel upscale** works in pixel space (sharper, more options).

I use latent 80% of the time. It's faster and my computer is tired.

### When to Use This Pattern

- You want images larger than 512x512 but direct generation looks weird
- Face details are off at high resolutions
- Body proportions get wonky in full-resolution T2I
- You want more detail without regenerating entirely

### 📊 Sidebar: Straight Answers - Resolution Strategy

**SD 1.5 models:**
- Native training: 512x512
- Direct generation limit: ~768x768 before quality degrades
- Highres fix recommended: anything above 768px

**SDXL models:**
- Native training: 1024x1024
- Direct generation limit: ~1536x1536 before issues
- Highres fix recommended: anything above 1536px

**Flux models:**
- More flexible, but still benefits from two-pass at extreme resolutions (>2048px)

**Rule of thumb:** If you're generating more than 1.5x the model's native resolution, use Highres Fix.

---

## Pattern #4: Upscaling (ESRGAN Detail Enhancement)

*Nyquil Cat voice:*

Sometimes you have a finished image and just want... MORE. More pixels. More detail. Like zooming into a dream.

Upscaling patterns use specialized models (ESRGAN, RealESRGAN, etc.) trained specifically to add detail when scaling images.

### The Core Upscaling Pattern

**Node sequence:**
```
Load Image → Upscale Image (Model) → Save Image
```

Yes, it's that simple. Three nodes. This is the "heat up leftovers" of patterns—minimal effort, maximum result.

**But the devil is in the model choice.**

### Upscale Model Types

**Common upscale models:**

| Model | Best For | Multiplier | Notes |
|-------|----------|------------|-------|
| **RealESRGAN_x4plus** | General photos, faces | 4x | All-purpose workhorse |
| **RealESRGAN_x4plus_anime_6B** | Anime/illustration | 4x | Preserves line art |
| **ESRGAN_4x** | Generic upscaling | 4x | Older, still solid |
| **SwinIR** | Texture preservation | 4x | Slower, higher quality |
| **Ultrasharp** | Sharpness priority | 4x | Can oversharpen |

**My lazy approach:** RealESRGAN_x4plus for everything. It works 90% of the time.

### Advanced Upscaling Pattern

**Two-stage upscale for extreme sizes:**

```
Load Image → Upscale 2x (ESRGAN) → Upscale 2x again (different model) → Save
```

**Why two passes?**
- Upscaling 4x directly can introduce artifacts
- Two 2x passes often looks cleaner
- You can use different models (one for structure, one for detail)

### Upscale + Refine Pattern

**Combining upscale with img2img:**

```
Load Image → Upscale 4x (ESRGAN) → VAE Encode ──┐
                                                 ├→ KSampler (denoise 0.2-0.3) → VAE Decode → Save
Checkpoint → CLIP (detail enhancement prompt) ──┘
```

**This is POWERFUL:**
1. ESRGAN adds pixels
2. Img2img pass at low denoise adds AI detail
3. Result: 4x larger with enhanced features

**Denoise sweet spot:** 0.2-0.3. Higher = you're regenerating, not enhancing.

### When to Use This Pattern

- Final output needs to be large (print, wallpaper, etc.)
- You have a good 512x512 image, need 2048x2048
- Adding detail to upscaled photos
- Preparing images for further editing in Photoshop/GIMP

### ⚠️ Common Mistake: Upscaling Won't Fix Bad Images

Upscaling enhances detail. It doesn't fix:
- Bad anatomy (that hand was weird at 512px, it's VERY weird at 2048px)
- Poor composition
- Artifacts from bad generation

**Fix the image FIRST, then upscale.** Don't upscale garbage hoping it'll get better. It'll just be high-resolution garbage.

---

## Pattern #5: Batch Processing (Multiple Naps at Once)

*Nyquil Cat voice:*

You know what's better than one nap? FOUR SIMULTANEOUS NAPS. That's batch processing.

Generate multiple variations in a single queue. Same prompt, different seeds. Or different prompts, same settings. Explore possibilities without clicking "Queue" 47 times.

### The Core Batch Pattern

**Method 1: Batch Size (same prompt, different seeds)**

```
Checkpoint → CLIP → Empty Latent (batch_size=4) → KSampler → VAE Decode → Save
```

**Empty Latent settings:**
- Width: 512
- Height: 512
- **Batch_size: 4** ← This is the magic

**Result:** Four different images from same prompt, using seeds [seed, seed+1, seed+2, seed+3]

**VRAM warning:** Batch size multiplies VRAM usage. Batch size 4 = 4x memory. Don't set this to 10 and wonder why your computer is screaming.

### Method 2: Seed Schedule (controlled variation)

**Using a seed list:**

Some custom nodes let you specify seed lists. But honestly? Just use batch size and increment. Simpler.

**Or manually queue multiple times with seed+1 each time.** Sometimes the old ways are fine.

### Pattern Variation: Prompt Batching

**Different prompts, same settings:**

This requires custom nodes (like "Batch Prompt Schedule") or you do it manually:

1. Generate image with prompt A
2. Change prompt to B
3. Queue again
4. Repeat

**Is there a node for this?** Yes. "Batch Prompt" custom node. But it's complex and I'm sleepy. The manual method works fine for 3-5 variations.

### When to Use This Pattern

- Exploring prompt variations
- Finding the "right" seed (generate 10, pick best)
- Creating image sets (character turnaround, expression sheet)
- A/B testing different settings (though you'll need to queue separately)

### 📉 Sidebar: VRAM Budget for Batching

**VRAM usage scales linearly with batch size:**

| GPU VRAM | SD 1.5 Max Batch | SDXL Max Batch |
|----------|------------------|----------------|
| 6GB | 4-6 | 1-2 |
| 8GB | 8-10 | 2-3 |
| 12GB | 16+ | 4-6 |
| 24GB | 32+ | 10-12 |

**When batch size exceeds VRAM:** Generation slows to a crawl (swapping to RAM) or crashes entirely.

**My advice:** Start with batch 2. If it works, try 4. If it works, try 8. Find your limit through experimentation, not through reading charts written by sleepy cats.

---

## Pattern #6: Tiling (Seamless Textures)

*Nyquil Cat voice:*

Sometimes you need a texture that loops. Wallpaper. Game textures. Fabric patterns. The kind of image where the edges connect perfectly.

This pattern ensures your image tiles seamlessly—no visible seams when repeated.

### The Core Tiling Pattern

**Node sequence:**
```
Checkpoint → CLIP → Empty Latent → KSampler → VAE Decode → Save
                                        ↑
                                   [Circular padding enabled]
```

**Wait, where's the tiling?**

It's in the **sampler settings.** Some samplers have tiling built in. Or you use a custom node like "Tiled KSampler."

**Honest truth:** The easiest way is using a custom node called "Seamless Tiling" from ComfyUI Manager. It wraps the sampling process with circular padding.

### Installing Seamless Tiling (Custom Node)

1. Open ComfyUI Manager
2. Search: "seamless"
3. Install: "ComfyUI Seamless Tiling"
4. Restart ComfyUI
5. Find new node: "Seamless Mode"

**Usage:**
```
Checkpoint → Seamless Mode (tiling=both) → CLIP → KSampler → ...
```

**Seamless Mode settings:**
- `tiling = both` → tiles horizontally AND vertically
- `tiling = horizontal` → only horizontal seams removed
- `tiling = vertical` → only vertical seams removed

### When to Use This Pattern

- Creating game textures (ground, walls, etc.)
- Generating seamless patterns (fabric, wallpaper)
- Background assets that need to repeat
- Any case where edges must match perfectly

### Testing Tileability

**After generating, test it:**

1. Save image
2. Load in image editor (GIMP, Photoshop)
3. Create 2x2 grid of the same image
4. Look for seams

**If you see seams:** Increase denoise slightly (gives model more freedom to blend edges).

**If it's perfect:** Congrats, you've made a seamless texture. Go take a nap; you've earned it.

---

## Pattern #7: Animation Basics (Frame Consistency)

*Nyquil Cat voice:*

Animation is... complex. Like, "I need a three-hour nap before explaining this" complex.

But the **basic pattern** is simple: batch processing + frame conditioning to maintain consistency across frames.

**Full disclosure:** This section is an overview. Real animation workflows need custom nodes (AnimateDiff, Wan, Frame Interpolation). But the pattern structure is universal.

### The Core Animation Pattern

**Conceptual sequence:**
```
Checkpoint → CLIP (prompt) → Frame Latents (batch of N frames) →
  Temporal KSampler (samples with frame-to-frame consistency) →
  VAE Decode → Save Frames → Combine to Video
```

**Key differences from static image:**
- **Frame latents:** Batch of latents representing each frame
- **Temporal sampler:** Considers previous frames when generating next frame
- **Frame consistency:** Prevents flickering/morphing between frames

### Practical Animation Pattern (AnimateDiff)

**Using AnimateDiff custom node:**

1. Install "AnimateDiff Evolved" from ComfyUI Manager
2. Download motion module model (these are separate from checkpoints)
3. Build workflow:

```
Checkpoint → AnimateDiff Loader (motion_model) → CLIP →
  Empty Latent Video (frames=16, fps=8) → KSampler → VAE Decode →
  Video Combine → Save
```

**Settings that matter:**
- **Frames:** How many frames (16 = 2 seconds at 8fps)
- **FPS:** Playback speed
- **Context length:** How many previous frames influence current frame (more = smoother, more VRAM)

### Image-to-Video Pattern

**Starting from a static image:**

```
Load Image → VAE Encode → [Convert to video latent] →
  Temporal KSampler → VAE Decode → Video Combine
```

**This is how you make still images "move."** The model generates subsequent frames that evolve from the initial image.

### When to Use This Pattern

- Creating short looping animations
- Making static images "come alive"
- Prototyping animation before serious 3D work
- Because it's cool and you want to

### ⚠️ Reality Check: Animation is VRAM-Hungry

**VRAM requirements:**

| GPU VRAM | Max Frames (SD 1.5) | Max Frames (SDXL) |
|----------|---------------------|-------------------|
| 6GB | 8-12 | Don't even try |
| 8GB | 16-24 | 8-12 |
| 12GB | 32-48 | 16-24 |
| 24GB | 64+ | 32-48 |

**My advice:** Start with 8 frames. If it works, try 16. Video generation is where even powerful GPUs start sweating.

---

## Pattern #8: Workflow Snippets (Saving & Reusing Patterns)

*Nyquil Cat voice:*

Here's the thing about patterns: once you build them, you shouldn't have to build them again.

Save. Reuse. Combine.

This isn't a node pattern—it's a **workflow management pattern.** How to organize your templates so you're not starting from scratch every time.

### Saving Patterns as Templates

**Method 1: Save entire workflow**

1. Build your pattern (e.g., Highres Fix workflow)
2. Menu → Save
3. Name it: `Template_HighresFix.json`
4. Store in a `templates/` folder

**Next time you need Highres Fix:** Load template, adjust prompts/settings, generate.

**Method 2: Node group export (custom node required)**

Some custom nodes let you select nodes → right-click → "Export as template." This saves just that section, not the whole workflow.

**Honestly?** Just save full workflows. Simpler. The file is tiny (a few KB).

### Organizing Your Template Library

**Suggested folder structure:**
```
ComfyUI/
  workflows/
    templates/
      00_Basic_T2I.json
      01_Image2Image.json
      02_HighresFix.json
      03_Upscale_ESRGAN.json
      04_Upscale_Plus_Refine.json
      05_Seamless_Tiling.json
      06_Batch_Processing.json
      07_Animation_Basic.json
      10_Portrait_Workflow.json
      11_Landscape_Workflow.json
    projects/
      [your actual project files]
```

**Naming convention:**
- Number prefix = load order in file browser
- Descriptive name = you remember what it does in 3 months

### Combining Patterns

**The real power: remix patterns into mega-workflows**

**Example: Highres Fix + Upscale + Refine**
```
[Pattern 1: Highres Fix]
T2I → Latent Upscale → KSampler (denoise 0.4) → VAE Decode
                                                    ↓
[Pattern 2: ESRGAN Upscale]
                                          Upscale 2x (ESRGAN)
                                                    ↓
[Pattern 3: Detail Refine]
                          VAE Encode → KSampler (denoise 0.25) → VAE Decode → Save
```

**This workflow:**
1. Generates 512x512 clean image
2. Highres fixes to 1024x1024
3. ESRGAN upscales to 2048x2048
4. Final refine pass adds AI detail

**Result:** Professional-quality large images. But it takes 3-4 minutes. Go take a nap while it runs.

### When to Use This Pattern

- Every project (save your successful workflows!)
- Building a personal workflow library
- Sharing workflows with others
- Teaching (give someone your template, they modify it)

---

## 🎨 The Pattern Cookbook (Visual Guide)

*Here's where you'd have visual diagrams of each pattern. Since this is markdown, I'll describe them:*

### Visual Pattern Chart

**T2I Pattern:**
```
[Checkpoint] → [CLIP+] ──┐
               [CLIP-] ──┤
               [Empty] ──┤─→ [Sample] → [Decode] → [Save]
```

**I2I Pattern:**
```
[Checkpoint] → [CLIP+] ──┐
               [CLIP-] ──┤
[Load] → [Encode] ───────┤─→ [Sample] → [Decode] → [Save]
```

**Highres Fix Pattern:**
```
Pass 1: [Basic T2I] → [Decode]
                         ↓
Pass 2: [Encode] → [Upscale Latent] → [Sample 0.4] → [Decode] → [Save]
```

**Upscale Pattern:**
```
[Load] → [ESRGAN 4x] → [Save]

OR with refine:
[Load] → [ESRGAN] → [Encode] → [Sample 0.2] → [Decode] → [Save]
```

**Tiling Pattern:**
```
[Checkpoint] → [Seamless Mode] → [CLIP] → [Sample] → [Decode] → [Save]
```

**Animation Pattern:**
```
[Checkpoint] → [AnimateDiff] → [CLIP] → [Video Latent] →
  [Temporal Sample] → [Decode] → [Combine Video] → [Save]
```

---

## 🔧 Workflow Remix Guide

### How to Combine Patterns

**General rules:**

1. **Identify the core pattern** (what's the main goal?)
2. **Add secondary patterns** (enhancements, variations)
3. **Check connections** (make sure data types match)
4. **Test incrementally** (add one pattern at a time, test after each)

### Common Combinations

**Portrait Workflow = T2I + Highres Fix + Face Fix**
```
Basic T2I → Highres Fix → Face Restore (GFPGAN) → Save
```

**Landscape Workflow = T2I + Highres Fix + Upscale**
```
Basic T2I → Highres Fix → ESRGAN 2x → Save
```

**Product Texture = Tiling + I2I + Upscale**
```
Load sketch → I2I (seamless mode) → ESRGAN → Save
```

**Animation Loop = AnimateDiff + I2I (last frame feeds first)**
```
[This is complex and I'm very sleepy. Advanced topic for another nap.]
```

### Troubleshooting Combined Patterns

**When patterns don't play nice:**

1. **VRAM explosion:** Too many patterns = too much memory
   - **Fix:** Reduce batch sizes, use GGUF models, enable VAE tiling

2. **Wrong data types:** Trying to connect incompatible nodes
   - **Fix:** Use convert nodes (Image to Latent, Latent to Image)

3. **Quality degradation:** Too many passes = cumulative errors
   - **Fix:** Use lower denoise values, fewer total passes

4. **Generation time measured in geological epochs:**
   - **Fix:** This is life now. Go take a real nap.

---

## 📦 Template Library Starter Pack

*Nyquil Cat voice:*

Here are 10 ready-to-use workflows you should have in your library. I'm not giving you the JSON (that'd be hundreds of lines), but I'm describing exactly what nodes go where.

Build these once. Save them. Use them forever.

### Template 1: Basic T2I (512x512)

**Nodes:**
- Load Checkpoint
- CLIP Text Encode (Positive)
- CLIP Text Encode (Negative)
- Empty Latent Image (512x512, batch 1)
- KSampler (steps 20, cfg 7, euler_a)
- VAE Decode
- Save Image

**Use for:** Quick tests, prompt exploration, daily generation

---

### Template 2: SDXL T2I (1024x1024)

**Same as Template 1, but:**
- Empty Latent: 1024x1024
- Consider adding second CLIP for refiner (optional)

**Use for:** SDXL checkpoint generations

---

### Template 3: Image-to-Image (Variable Denoise)

**Nodes:**
- Load Checkpoint
- Load Image
- VAE Encode
- CLIP Text Encode (Positive)
- CLIP Text Encode (Negative)
- KSampler (denoise 0.5, adjust as needed)
- VAE Decode
- Save Image

**Use for:** Refining images, style transfer, iterations

---

### Template 4: Highres Fix (512→1024)

**First Pass:**
- Load Checkpoint
- CLIP Encode (Positive)
- CLIP Encode (Negative)
- Empty Latent (512x512)
- KSampler (steps 20)
- VAE Decode

**Second Pass:**
- VAE Encode (from first pass)
- Latent Upscale (scale 2.0)
- KSampler (steps 15, denoise 0.4)
- VAE Decode
- Save Image

**Use for:** Clean high-res images from SD 1.5 models

---

### Template 5: ESRGAN Upscale (4x)

**Nodes:**
- Load Image
- Upscale Image (model: RealESRGAN_x4plus)
- Save Image

**Use for:** Final upscaling, print preparation

---

### Template 6: Upscale + AI Refine

**Nodes:**
- Load Image
- Upscale Image (ESRGAN 4x)
- VAE Encode
- Load Checkpoint
- CLIP Text Encode ("high quality, detailed" prompt)
- KSampler (denoise 0.25, steps 12)
- VAE Decode
- Save Image

**Use for:** Upscaling with detail enhancement

---

### Template 7: Batch Generation (4 variations)

**Same as Template 1, but:**
- Empty Latent: batch_size = 4
- Adjust VRAM accordingly

**Use for:** Exploring seed variations

---

### Template 8: Seamless Tiling

**Nodes:**
- Load Checkpoint
- Seamless Mode (tiling: both) [custom node]
- CLIP Text Encode (Positive)
- CLIP Text Encode (Negative)
- Empty Latent (512x512)
- KSampler
- VAE Decode
- Save Image

**Use for:** Game textures, patterns, wallpapers

---

### Template 9: LoRA-Enhanced T2I

**Nodes:**
- Load Checkpoint
- Load LoRA (strength 0.8)
- CLIP Text Encode (Positive) [from LoRA output]
- CLIP Text Encode (Negative) [from LoRA output]
- Empty Latent
- KSampler
- VAE Decode
- Save Image

**Use for:** Style-specific generations (character LoRAs, art styles)

---

### Template 10: Portrait Fix Workflow

**Nodes:**
- [Full T2I workflow]
- VAE Decode
- Face Restore (GFPGAN or CodeFormer) [custom node]
- Save Image

**Use for:** Fixing face details in portraits

---

## 🧪 Practice Exercises

Time to build these patterns yourself. No napping until you've done at least three.

### Exercise 1: Build the Highres Fix Pattern

**Task:**
1. Create basic T2I workflow
2. Add second pass with Latent Upscale (2x)
3. Set second KSampler to denoise 0.4
4. Generate a 512→1024 image
5. Save workflow as `Template_HighresFix.json`

**Prompt suggestion:** "a mysterious forest, detailed, atmospheric lighting"

**Success criteria:** Image is 1024x1024, looks detailed, no weird artifacts

---

### Exercise 2: Image-to-Image Exploration

**Task:**
1. Generate an image using basic T2I
2. Build I2I workflow
3. Load your generated image
4. Use different prompt: "same scene, but at sunset"
5. Experiment with denoise: 0.3, 0.5, 0.7
6. Compare results

**Success criteria:** You understand how denoise affects transformation strength

---

### Exercise 3: Create Seamless Texture

**Task:**
1. Install "Seamless Tiling" custom node
2. Build tiling workflow
3. Generate a stone texture: "rough stone wall texture, seamless"
4. Test tileability in image editor (2x2 grid)
5. Iterate until seams are invisible

**Success criteria:** Texture tiles perfectly with no visible edges

---

### Exercise 4: Upscale + Refine Combo

**Task:**
1. Take a 512x512 generated image
2. Build combined pattern: ESRGAN 4x → I2I refine (denoise 0.25)
3. Compare upscaled version vs upscale+refine
4. Notice the AI-added detail

**Success criteria:** You see clear difference between pure upscale and refined upscale

---

### Exercise 5: Build Your Template Library

**Task:**
1. Create a `templates/` folder in your workflows directory
2. Build and save all 10 starter pack templates
3. Test each one to make sure it works
4. Add your own notes in the workflow (use "Note" nodes)

**Success criteria:** You have 10 working templates ready for future use

---

## 📊 Sidebar: Straight Answers - Pattern Decision Tree

**"Which pattern should I use?"**

```
START: What do you want to do?
  ↓
Generate new image from text?
  → YES: T2I Pattern
  → NO ↓

Modify existing image?
  → YES: I2I Pattern (set denoise based on how much change you want)
  → NO ↓

Make image larger?
  → YES: Need more detail or just bigger?
    → Just bigger: ESRGAN Upscale
    → More detail: Upscale + Refine Pattern
  → NO ↓

Need high resolution from scratch?
  → YES: Highres Fix Pattern
  → NO ↓

Create seamless texture?
  → YES: Tiling Pattern
  → NO ↓

Generate animation?
  → YES: Animation Pattern (needs custom nodes)
  → NO ↓

Make multiple variations?
  → YES: Batch Processing Pattern
  → NO ↓

You probably need a custom workflow. Start with closest pattern and modify.
```

---

## Common Mistakes & How to Avoid Them

### Mistake 1: Using Wrong Pattern for the Job

**Example:** Using I2I when you need Highres Fix

**Symptoms:** Image changes too much, doesn't look like improved version

**Fix:** If you want same image but bigger/better, use Highres Fix (low denoise, upscale). I2I is for creative reinterpretation.

---

### Mistake 2: Denoise Too High in Multi-Pass Workflows

**Example:** Highres Fix with denoise 0.8

**Symptoms:** Second pass completely regenerates image, ignores first pass

**Fix:** Keep denoise 0.3-0.5 in enhancement passes. You're refining, not regenerating.

---

### Mistake 3: Combining Too Many Patterns

**Example:** T2I + Highres Fix + Upscale 4x + Refine + Face Fix

**Symptoms:** VRAM explosion, generation takes 10 minutes, quality actually gets WORSE

**Fix:** More isn't always better. Each pass introduces tiny errors. Usually 2-3 stages max.

---

### Mistake 4: Not Testing Patterns Incrementally

**Example:** Building giant mega-workflow, clicking Queue, everything fails

**Symptoms:** No idea which part is broken

**Fix:** Build patterns one at a time. Test after adding each. Don't build a 50-node workflow in one go.

---

### Mistake 5: Forgetting to Save Working Patterns

**Example:** "I made the perfect workflow yesterday... where is it?"

**Symptoms:** Crying, rebuilding from scratch, regret

**Fix:** Hit Save immediately after successful generation. Name it descriptively. Future you will thank present you.

---

## Chapter Summary

*Nyquil Cat voice:*

We covered eight patterns. EIGHT. That's almost as many as I have nap spots.

These aren't just random node arrangements. They're proven solutions to common problems. The recipes that work.

**You learned:**
- **T2I pattern:** The foundation everything builds on
- **I2I pattern:** Redreaming existing images with denoise control
- **Highres Fix:** Two-pass quality for large images
- **Upscaling:** ESRGAN for adding pixels and detail
- **Batch processing:** Multiple variations in one queue
- **Tiling:** Seamless textures for games/patterns
- **Animation basics:** Frame consistency patterns (overview)
- **Template management:** Save, organize, reuse

**You can now:**
- ✅ Recognize patterns in others' workflows
- ✅ Build the 8 core patterns from scratch
- ✅ Adapt patterns for your specific needs
- ✅ Combine patterns into custom workflows
- ✅ Maintain a library of reusable templates
- ✅ Choose the right pattern for the task

**What you have:**
- 10 ready-to-use workflow templates
- Understanding of pattern structure
- Ability to remix patterns creatively
- Decision tree for "which pattern do I need?"

---

## What's Next

**Chapter 7: Optimization & Troubleshooting**

Now that you know the patterns, let's make them run faster. And fix them when they break. Because your computer is yelling about VRAM and I'm going to explain why the food bowl is always empty.

Topics:
- VRAM management (the eternal struggle)
- Quantization (GGUF, FP8, making models smaller)
- CPU offloading (when your GPU gives up)
- Launch flags (--lowvram and friends)
- Error messages decoded (what "CUDA OOM" actually means)

**But first: Practice.**

Build those templates. Save them. Use them. Patterns are only useful if they're in your muscle memory.

And then take a nap. You've earned it.

---

## 💤 Cat's Final Thoughts

Patterns are... comforting. Like knowing exactly which sunbeam will be warm at 3 PM. Or which cardboard box is structurally sound enough for a nap.

ComfyUI looked chaotic at first. Random mice (nodes) everywhere. Tangled yarn (connections) with no logic.

But there IS logic. There are patterns. Repeatable, reliable, proven patterns.

And now you know them.

You're not just clicking nodes randomly anymore. You're following recipes. Building on foundations. Standing on the shoulders of sleepy giants who figured this out before you.

Use these patterns. Modify them. Break them. Rebuild them better.

And when someone asks, "How did you make that?" you can say:

"It's just a pattern. Let me show you."

---

**End of Chapter 6**

**Word Count:** ~2,950 words (excluding code blocks and tables)

---

*Nyquil Cat is now sleeping on the keyboard. The letter 'h' is being pressed continuously. hhhhhhhhhhhhhhhhhh*