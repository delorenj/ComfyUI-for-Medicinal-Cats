# Chapter 5: Advanced Prompting & Control (ControlNet, IPAdapter, Inpainting)

> *"You can GUIDE the dream with invisible fences. And masks. And reference images. It's like... lucid dreaming? I think? Brain is fuzzy."*

---

## Opening: The Dream Gets Specific

I had this dream once where I was catching mice, but the mice were EXACTLY the right color. And in EXACTLY the right spot. And doing EXACTLY the right pose. It was weird. Suspiciously controlled.

That's when I realized: sometimes you don't want the AI to just "dream up" whatever it feels like. Sometimes you need to GUIDE it. Not with words alone, but with... invisible fences. Reference images. Masks that say "only edit THIS part."

It's like lucid dreaming, but for computers. You're still dreaming, but you're also... steering.

This chapter is about control. Not the boring kind (nobody likes being told what to do). The useful kind. The "make the character do THIS pose" kind. The "keep this style from THIS reference image" kind. The "fix just the face without regenerating the whole picture" kind.

We're going deeper than prompts now. We're getting... architectural about our dreams.

*Stretches. Yawns. Realizes this is going to take more than one nap to explain.*

Let's start with making your prompts smarter.

---

## Part 1: Advanced Prompt Syntax (Words, But Fancier)

You already know how to write prompts: "a cat in a cardboard box, digital art" and the AI figures it out. But prompts have SECRET SYNTAX. Like cheat codes. For dreams.

### Emphasis: Making Words LOUDER

Sometimes you want the AI to pay MORE attention to specific words. That's emphasis.

**The Syntax:**
- `(word)` = 1.1x attention (slightly more)
- `((word))` = 1.21x attention (definitely more)
- `(word:1.5)` = 1.5x attention (MUCH more, specific multiplier)
- `[word]` = 0.9x attention (slightly less)

**Example:**
```
Normal prompt:
"portrait of a woman, red hair, blue eyes, smiling"

With emphasis:
"portrait of a woman, (red hair:1.4), (blue eyes:1.3), smiling"
```

The AI will now REALLY focus on making the hair red and the eyes blue. The smile is normal priority.

**Nyquil Cat's Rule:** Don't over-emphasize everything. If EVERY word is loud, then NO words are loud. It's like yelling. Effective once, annoying if constant.

---

### Prompt Editing: Changing Mid-Generation

This is WILD. You can tell the AI to change the prompt DURING sampling.

**The Syntax:**
```
[word1:word2:step]
```

- Starts with `word1`
- Switches to `word2` at step `step`

**Example:**
```
[cat:dog:15]
```

If you're using 30 sampling steps:
- Steps 0-14: AI thinks "cat"
- Steps 15-30: AI thinks "dog"

The result? Some kind of cat-dog hybrid abomination. Or a cat that morphs into a dog. Depends on the seed and your luck.

**Why This Exists:** Sometimes you want the AI to start with one concept's STRUCTURE, then shift to another concept's DETAILS. Advanced users do this for complex compositions.

**Nyquil Cat's Take:** This is the dream equivalent of "start thinking about fish, then switch to thinking about birds mid-nap." Your brain gets confused. So does the AI. Use sparingly.

---

### Attention/Emphasis in Practice

Let's say you keep generating "a warrior in a forest" but the AI keeps making the forest HUGE and the warrior tiny.

**Fix with emphasis:**
```
(warrior:1.3) in a forest, medieval armor, sword
```

Now the warrior gets more "attention weight" and won't be a tiny background detail.

**Common Use Cases:**
- `(detailed face:1.2)` — fixes blurry faces
- `(sharp focus:1.3)` — reduces blur
- `(vibrant colors:1.4)` — increases saturation
- `[simplified:0.8]` — reduces detail (sometimes you want loose, painterly)

---

**[STRAIGHT ANSWERS: Prompt Syntax Cheat Sheet]**

| Syntax | Effect | Use When |
|--------|--------|----------|
| `(word)` | 1.1x attention | Slight boost needed |
| `((word))` | 1.21x attention | Medium boost |
| `(word:1.5)` | 1.5x attention | Strong boost, precise control |
| `[word]` | 0.9x attention | Slight reduction |
| `[word1:word2:10]` | Switch words at step 10 | Advanced morphing/hybrid concepts |

**Rule:** Emphasis values above 1.8 often create distortion. Keep it reasonable.

---

## Part 2: ControlNet — The Invisible Fence

Prompts describe WHAT you want. ControlNet describes HOW it should be arranged.

Think of it like this:
- **Prompt:** "I want a cat"
- **ControlNet:** "I want a cat in THIS exact pose, with THIS exact composition"

ControlNet takes a reference image, extracts a "control signal" (like edges, or depth, or pose), and forces the AI to follow that structure while generating.

It's an invisible fence. The AI can dream freely INSIDE the fence, but can't cross the boundaries.

### What is ControlNet, Technically?

ControlNet is an ADDITIONAL neural network that plugs into your diffusion model. It was trained to:
1. Take a control image (like edge map or pose skeleton)
2. Condition the generation to match that structure
3. Let the rest (colors, style, details) be determined by your prompt

**Result:** You get structural control without sacrificing creativity.

---

### Installing ControlNet

ControlNet requires:
1. **ControlNet custom nodes** (via ComfyUI Manager)
2. **ControlNet model files** (downloaded separately)
3. **Preprocessor nodes** (to extract control signals from images)

**Installation Steps:**

1. **Install ComfyUI Manager** (if you haven't already — see Chapter 1)

2. **Search for ControlNet nodes:**
   - Open ComfyUI Manager
   - Search: "ControlNet"
   - Install: **"comfyui_controlnet_aux"** (preprocessors)
   - Also install any ControlNet node packs you find (there are several)

3. **Download ControlNet models:**
   - Go to: HuggingFace (lllyasviel/ControlNet models)
   - Or: CivitAI (search "ControlNet")
   - Download models for the control types you want (Canny, Depth, Pose, etc.)
   - Place in: `ComfyUI/models/controlnet/`

**Common ControlNet Models:**
- `control_sd15_canny.pth` — Edge detection (SD 1.5)
- `control_sd15_depth.pth` — Depth map (SD 1.5)
- `control_sd15_openpose.pth` — Human pose (SD 1.5)
- SDXL versions also exist (they're BIG — 2.5GB+)

---

### ControlNet Types: When to Use What

There are MANY ControlNet types. Here's the cheat sheet.

**[ControlNet Cheat Sheet]**

| Type | Extracts | Use Case | Best For |
|------|----------|----------|----------|
| **Canny** | Edges | Preserve line art, shapes | Line drawings, architectural sketches |
| **Depth** | Depth map | Preserve 3D structure | Photographs, 3D renders, maintaining spatial layout |
| **Pose/OpenPose** | Body skeleton | Match human poses | Character art, specific poses, anatomy reference |
| **Scribble** | Rough sketches | Turn doodles into art | Quick concept art, sketchy references |
| **Normal Map** | Surface normals | Preserve surface detail | Textures, relief maps, detailed surfaces |
| **Segmentation** | Semantic regions | Match scene layout | Landscapes, multi-region compositions |
| **Lineart** | Clean line extraction | Anime/manga style | Clean lineart, coloring existing drawings |

**Nyquil Cat's Summary:**
- **Canny:** "Follow these edges exactly"
- **Depth:** "Keep this depth exactly"
- **Pose:** "Put the human in THIS pose"
- **Scribble:** "My terrible doodle, but make it good"

---

### Using ControlNet: Basic Workflow

Let's do a **Pose** example. You have a reference photo of someone in a cool pose, and you want to generate a character in THAT pose.

**Nodes You Need:**
1. **Load Image** — Your reference image
2. **ControlNet Preprocessor** — Extracts pose skeleton
3. **Apply ControlNet** — Applies control to generation
4. **Load ControlNet Model** — Loads the ControlNet weights
5. Your normal workflow (Load Checkpoint, KSampler, etc.)

**Step-by-Step:**

1. **Add Reference Image:**
   - Add node: `Load Image`
   - Upload your pose reference photo

2. **Extract Pose:**
   - Add node: `OpenPose Preprocessor` (or whatever ControlNet type you're using)
   - Connect: `Load Image` → `OpenPose Preprocessor`
   - This outputs: `IMAGE` (the pose skeleton visualization)

3. **Load ControlNet Model:**
   - Add node: `Load ControlNet Model`
   - Widget: Select your `control_sd15_openpose.pth` (or SDXL version)

4. **Apply ControlNet:**
   - Add node: `Apply ControlNet`
   - Connect:
     - `CONDITIONING` (from your CLIP Text Encode) → `Apply ControlNet`
     - `CONTROL_NET` (from Load ControlNet Model) → `Apply ControlNet`
     - `IMAGE` (from OpenPose Preprocessor) → `Apply ControlNet`
   - Widget: Set `strength` (0.0-1.0, usually 0.7-1.0 for strong control)

5. **Connect to KSampler:**
   - Use the CONDITIONED output from `Apply ControlNet` as your positive conditioning in KSampler
   - Everything else stays the same

6. **Generate:**
   - Your prompt describes the character: "fantasy knight, armor, dramatic lighting"
   - ControlNet ensures the knight is in the EXACT pose from your reference

**Result:** Character in your exact pose, but with your prompt's style/details.

---

**[CAT TAKES OFF THE MASK: How ControlNet Actually Works]**

During training, ControlNet learns:
- "When I see THESE edges/depth/pose..."
- "...the latent should look like THIS"

It's a mapping from structural information to latent space biases.

When you apply ControlNet:
- Each sampling step, the ControlNet looks at the control image
- It says: "Hey diffusion model, bias your denoising toward THIS structure"
- The model still follows your prompt, but can't deviate from the structure

**Strength Parameter:** How much the model listens to ControlNet vs your prompt
- `1.0` = Follow ControlNet exactly (very rigid)
- `0.7` = Follow mostly, but allow some freedom
- `0.3` = Light suggestion (often too weak)

**Sweet Spot:** 0.7-0.9 for most use cases.

---

### Troubleshooting ControlNet

**Problem: "Control isn't working, image ignores my reference"**

Fixes:
- Increase `strength` to 0.9 or 1.0
- Check preprocessor actually ran (you should see the processed control image)
- Verify ControlNet model matches your checkpoint architecture (SD 1.5 ControlNet won't work with SDXL checkpoint)
- Make sure control image is connected to Apply ControlNet node

**Problem: "Image is TOO rigid, looks exactly like reference"**

Fixes:
- Lower `strength` to 0.6-0.7
- Increase CFG scale slightly (gives prompt more influence)
- Use a different sampler (DPM++ sometimes balances better than Euler)

**Problem: "Preprocessor output looks wrong"**

Fixes:
- Check preprocessor settings (some have resolution limits)
- Try a different preprocessor variant (there are often multiple versions)
- Verify reference image is clear enough for extraction

---

## Part 3: IPAdapter — Style Transfer from Reference

ControlNet controls STRUCTURE. IPAdapter controls STYLE.

**Use Case:** You have an image you love (a painting, a photo, a render) and you want to generate NEW images in that SAME style.

**How It Works:** IPAdapter uses CLIP image embeddings to extract the "vibe" of a reference image, then biases generation toward that vibe.

**The Difference:**
- **ControlNet:** "Match THIS pose/edge/depth"
- **IPAdapter:** "Match THIS aesthetic/color palette/mood"

---

### Installing IPAdapter

1. **Install via ComfyUI Manager:**
   - Search: "IPAdapter"
   - Install: **"ComfyUI IPAdapter Plus"** (most popular implementation)

2. **Download IPAdapter models:**
   - Go to: HuggingFace (search "IPAdapter models")
   - Download the appropriate model for your checkpoint architecture
   - Place in: `ComfyUI/models/ipadapter/`

**Common Models:**
- `ip-adapter_sd15.safetensors` — SD 1.5
- `ip-adapter_sdxl.safetensors` — SDXL

---

### Using IPAdapter: Basic Workflow

**Goal:** Generate a portrait in the style of a reference painting.

**Nodes:**
1. **Load Image** — Your style reference
2. **IPAdapter Apply** — Applies style conditioning
3. **Load IPAdapter Model** — Loads weights
4. Normal workflow (checkpoint, KSampler, etc.)

**Connections:**
1. Load your style reference image
2. Connect reference to IPAdapter node
3. Connect IPAdapter to your model/conditioning chain
4. Generate with your prompt

**Strength Parameter:** How much to copy the style
- `1.0` = Copy style heavily (might override your prompt)
- `0.5` = Balanced (style + prompt)
- `0.2` = Light style hint

**Nyquil Cat's Metaphor:** IPAdapter is like saying "dream in the style of THIS picture." The dream content is still your prompt, but the painting technique matches the reference.

---

### Combining ControlNet + IPAdapter

Here's where it gets POWERFUL.

You can use BOTH:
- **ControlNet:** Controls pose/structure
- **IPAdapter:** Controls style/aesthetic

**Example Workflow:**
1. Reference Image A: Cool pose (use with ControlNet Pose)
2. Reference Image B: Beautiful painting style (use with IPAdapter)
3. Prompt: "fantasy warrior, dramatic lighting"

**Result:** Warrior in the pose from Image A, painted in the style of Image B, with details from your prompt.

This is EXTREMELY versatile. You're separating concerns:
- Structure → ControlNet
- Style → IPAdapter
- Content → Prompt

---

## Part 4: Inpainting — Selective Dream Editing

Sometimes you generate an image and it's ALMOST perfect. But the hand is weird. Or the background has a random object. Or you want to change JUST the face.

That's inpainting.

**Definition:** Regenerating ONLY a masked region of an image, keeping the rest intact.

---

### How Inpainting Works

Standard generation: The AI starts from pure noise, gradually denoises into an image.

Inpainting: The AI starts from:
- **Masked region:** Noise (will be regenerated)
- **Unmasked region:** Original image (will be preserved)

The AI smoothly blends the regenerated region with the preserved region.

---

### Creating Masks

A **mask** is a black-and-white image:
- **White:** Regenerate this area
- **Black:** Keep this area

**Ways to Create Masks:**

1. **External Editor (GIMP, Photoshop, etc.):**
   - Open your generated image
   - Paint white over the area to inpaint
   - Save as separate mask image
   - Load both image and mask into ComfyUI

2. **ComfyUI Mask Editor Node:**
   - Some custom node packs have built-in mask painters
   - Draw directly in the interface
   - Less precise, but faster

3. **Automatic Masking (SAM, Segment Anything):**
   - Use Segment Anything Model to auto-detect regions
   - Click an object, get a mask
   - Requires installing SAM custom nodes

---

### Inpainting Workflow

**Nodes:**
1. **Load Image** — Your original image
2. **Load Image (Mask)** — Your mask (white = inpaint)
3. **VAE Encode (for Inpainting)** — Special VAE encode that handles masks
4. **KSampler** — With appropriate denoise strength
5. **VAE Decode** — Back to pixels
6. **Save Image**

**Critical Settings:**
- **Denoise Strength:** How much to change the masked region
  - `1.0` = Completely regenerate (ignores original)
  - `0.7` = Regenerate but keep some original influence
  - `0.3` = Light editing (subtle changes)

**Typical Denoise for Inpainting:** 0.6-0.8

---

### Inpainting Example: Fix a Blurry Face

**Scenario:** You generated a portrait. The composition is perfect, but the face is blurry.

**Steps:**

1. **Create Mask:**
   - Open image in GIMP
   - Use brush tool, paint white over the face
   - Save as `mask.png`

2. **Load Both Images:**
   - Load Image node: Original portrait
   - Load Image node: Mask

3. **Setup Inpainting:**
   - Add: `VAE Encode (for Inpainting)` node
   - Connect: Original image → VAE Encode
   - Connect: Mask → VAE Encode (mask input)
   - This outputs: LATENT (with masked region marked)

4. **Sample:**
   - Connect LATENT to KSampler
   - Set denoise: `0.75` (strong regeneration)
   - Use SAME checkpoint/settings as original (for consistency)
   - Prompt: Focus on face details — "(detailed face:1.3), sharp focus, clear eyes"

5. **Decode and Save:**
   - VAE Decode → Save Image

**Result:** New face, same composition/background.

---

**[MASKING FOR CATS: Visual Guide]**

**Good Mask:**
```
[Image area visualization]
████████████████████  ← Black (keep)
████░░░░░░░░░░░████  ← White (regenerate)
████░░FACE░░░░░████
████░░░░░░░░░░░████
████████████████████
```

**Feathered Edges:** Blur the mask edges slightly (Gaussian blur in GIMP) for smoother blending.

**Common Mistake:** Mask too small → visible seam where regenerated region meets original

**Fix:** Make mask slightly LARGER than the problem area, with feathered edges.

---

### Outpainting: Extending the Canvas

Outpainting is inpainting, but for areas OUTSIDE the original image.

**Use Case:** You have a portrait, but you want to extend the background to the sides.

**Process:**
1. Expand canvas in image editor (add transparent areas)
2. Mask = the new transparent areas (white)
3. Inpaint with background-focused prompt

**Denoise:** Usually 0.9-1.0 (new content, not editing existing)

---

## Part 5: Region-Specific Prompting

What if you want DIFFERENT prompts for different regions?

Example:
- Left side: "sunset sky"
- Right side: "starry night"

**Solution:** Regional prompting nodes (custom nodes required).

**Common Implementations:**
- ComfyUI-Regional-Prompting (custom node pack)
- Allows defining regions with separate prompts
- More advanced than this chapter, but worth knowing exists

**Nyquil Cat's Note:** This gets complex fast. Master inpainting first, then explore regional prompting if you need it.

---

## Part 6: Practical Control Strategy

You now have MANY tools:
- Emphasis in prompts
- ControlNet for structure
- IPAdapter for style
- Inpainting for fixes
- Region prompting for complexity

**When to use what?**

**[CONTROL METHOD DECISION TREE]**

**Start Here: What do you need to control?**

→ **"I need a specific POSE/COMPOSITION"**
   → Use **ControlNet** (Pose, Depth, or Canny depending on source)

→ **"I need a specific STYLE/AESTHETIC"**
   → Use **IPAdapter** with style reference image

→ **"I need to FIX part of an image"**
   → Use **Inpainting** with mask

→ **"I need more focus on specific WORDS in my prompt"**
   → Use **Emphasis syntax** `(word:1.3)`

→ **"I need MULTIPLE different things in different regions"**
   → Use **Regional Prompting** or multiple inpainting passes

→ **"I need EVERYTHING controlled precisely"**
   → Use **ControlNet + IPAdapter + Detailed Prompt** together

---

### Combining Controls: Example Workflow

**Goal:** Fantasy portrait in specific pose and painting style

**Setup:**
1. **Reference Image A:** Photo of person in dramatic pose
2. **Reference Image B:** Oil painting with beautiful color palette
3. **Prompt:** "fantasy elf warrior, ornate armor, forest background"

**Workflow:**
1. Apply **ControlNet Pose** with Reference A (strength: 0.8)
2. Apply **IPAdapter** with Reference B (strength: 0.6)
3. Prompt with emphasis: "(fantasy elf warrior:1.2), (ornate armor:1.3), forest background, (oil painting:1.1)"
4. KSampler: 30 steps, CFG 7.5
5. Generate

**Result:** Elf in the pose from Reference A, painted in the style of Reference B, with fantasy details from prompt.

**Nyquil Cat's Analogy:** It's like giving the AI three sets of instructions:
- "Stand like THIS" (ControlNet)
- "Paint like THIS" (IPAdapter)
- "Make it look like THIS" (Prompt)

The AI juggles all three. Usually successfully.

---

## Part 7: Troubleshooting Advanced Controls

**[WHY ISN'T THIS WORKING?]**

### Problem: "ControlNet isn't affecting the image at all"

**Checklist:**
- [ ] Is control image actually connected to Apply ControlNet node?
- [ ] Is ControlNet model loaded and correct architecture (SD1.5 vs SDXL)?
- [ ] Is strength set appropriately (try 1.0 to test)?
- [ ] Does preprocessor output look correct? (Preview the control image)
- [ ] Are you using the CONDITIONED output from Apply ControlNet in KSampler?

**Most Common Cause:** Forgot to connect preprocessor output to Apply ControlNet.

---

### Problem: "IPAdapter makes everything look weird/wrong"

**Fixes:**
- Lower strength (try 0.3-0.5 instead of 1.0)
- Check reference image — is it too complex or abstract?
- Ensure IPAdapter model matches checkpoint architecture
- Try different IPAdapter model variant (some are trained for faces, some for general style)

---

### Problem: "Inpainting has visible seams/boundaries"

**Fixes:**
- Feather mask edges (Gaussian blur, 5-10px radius)
- Increase mask size slightly beyond problem area
- Lower denoise to 0.6 (blends better, but less regeneration)
- Use same seed/settings as original generation (for consistency)
- Check VAE — using same VAE as original generation helps

---

### Problem: "Combining ControlNet + IPAdapter, one dominates the other"

**Balance Strategy:**
- If ControlNet dominates: Lower ControlNet strength, raise IPAdapter strength
- If IPAdapter dominates: Lower IPAdapter strength, raise ControlNet strength
- Typical balance: ControlNet 0.8, IPAdapter 0.5
- Adjust CFG scale: Lower CFG (6-7) gives more freedom, higher CFG (8-10) follows controls more strictly

---

### Problem: "I don't have enough VRAM for ControlNet + everything else"

**Memory-Saving Tips:**
- Use GGUF quantized checkpoints (Chapter 4)
- Enable VAE tiling (for large images)
- Use FP8 ControlNet models if available
- Lower resolution (512x512 instead of 1024x1024 for testing)
- Generate in stages: ControlNet first, then upscale separately

---

## Chapter Summary: Controlling the Dream

*Okay. That was a LOT. Let me recap while my brain still functions.*

You started this chapter with basic prompts. Now you have:

**Advanced Prompting:**
- Emphasis syntax to boost/reduce word importance
- Prompt editing to morph concepts mid-generation
- Understanding of attention weighting

**ControlNet:**
- Structural control (pose, depth, edges)
- Different types for different needs
- Preprocessing to extract control signals
- Strength balancing

**IPAdapter:**
- Style transfer from reference images
- Aesthetic control without structural rigidity
- Combining with ControlNet for max control

**Inpainting:**
- Selective regeneration with masks
- Fixing specific regions
- Outpainting to extend images
- Denoise strength for blend control

**Strategy:**
- Knowing which tool for which problem
- Combining controls effectively
- Troubleshooting when controls conflict

---

### What You Learned

- [x] Use emphasis `(word:1.3)` to control prompt attention
- [x] Install and apply ControlNet for structural control
- [x] Choose correct ControlNet type (Pose, Depth, Canny, etc.)
- [x] Use IPAdapter for style transfer
- [x] Create masks for inpainting
- [x] Perform selective regeneration with inpainting
- [x] Combine multiple control methods
- [x] Troubleshoot control conflicts and VRAM issues
- [x] Understand when to use which control method

---

### Practice Exercises

**Exercise 1: Emphasis Practice**
- Generate an image with prompt: "cat, forest, sunset"
- Now generate with: "(cat:1.5), forest, (sunset:0.8)"
- Compare results. Notice the difference in focus?

**Exercise 2: ControlNet Pose**
- Find a reference photo of a person in an interesting pose
- Use OpenPose ControlNet to generate a character in that pose
- Try different prompts (fantasy, sci-fi, modern) with same pose

**Exercise 3: IPAdapter Style**
- Choose a favorite painting/artwork
- Use IPAdapter to generate new images in that style
- Experiment with strength (0.3, 0.6, 1.0) and see differences

**Exercise 4: Inpainting Fix**
- Generate a portrait
- Create a mask over the face
- Inpaint with denoise 0.7 and prompt focusing on face details
- Compare original vs inpainted

**Exercise 5: Combined Control**
- Use ControlNet for pose + IPAdapter for style on same generation
- Balance the strengths until you get a good result
- Document your strength settings for future reference

---

### Next Chapter Preview

You now know HOW to control generation. But you've been building workflows one node at a time, improvising as you go.

**Chapter 6** is about PATTERNS. Common node arrangements that ALWAYS work. Pre-tested recipes.

We'll cover:
- Img2img workflows (redreaming existing images)
- Highres Fix (two-pass for quality)
- Upscaling workflows (ESRGAN and beyond)
- Batch processing (many variations at once)
- Tiling (seamless textures)

Think of it as: You've learned the ingredients. Now you're learning the recipes.

But first, I need a nap. Controlling dreams is exhausting.

---

**[STRAIGHT ANSWERS: Chapter 5 Quick Reference]**

**Prompt Emphasis:**
- `(word)` = 1.1x | `((word))` = 1.21x | `(word:1.5)` = 1.5x
- `[word]` = 0.9x (reduction)
- Don't exceed 1.8 (causes distortion)

**ControlNet Types:**
- **Canny:** Edge control
- **Depth:** 3D structure control
- **Pose:** Human pose control
- **Scribble:** Sketch to image

**IPAdapter:**
- Style transfer from reference
- Strength 0.5-0.7 typical
- Combine with ControlNet for structure+style

**Inpainting:**
- Denoise 0.6-0.8 for fixes
- Feather mask edges (blur 5-10px)
- Use same checkpoint/VAE as original

**VRAM Tips:**
- ControlNet adds ~1-2GB
- Use quantized models
- Lower resolution for testing
- Enable VAE tiling for large images

---

*End of Chapter 5*

**Word Count:** ~3,200 words
**Status:** Ready for cat naps and lucid dreams

---

**Nyquil Cat's Final Thought:**

"You know what's weird? We just taught computers to follow invisible fences and paint like other paintings and edit specific parts of dreams. And somehow this all WORKS. Technology is wild. I'm going to sleep for 12 hours."

*— Nyquil Cat, Professional Dream Controller*
*Written at 2:47 AM, peak Nyquil clarity achieved*
