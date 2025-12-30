# Chapter 3: Your First Workflow (Actually Making an Image)

> *"We're going to make a picture. From text. Using math. I don't get it either, but watch this."*

## Opening: The Moment of Truth

So. You have ComfyUI running. You can see the interface. You've clicked around nervously, maybe accidentally deleted a node and panicked.

Now comes the part where we actually... make something.

I'm going to be honest with you. The first time I watched the default workflow run, I felt like I was witnessing sorcery. You type words into a box, click a button, wait about 30 seconds, and suddenly there's a PICTURE. A picture that didn't exist before. Made from... what? Math? Probability? The compressed dreams of a million images?

Yes. All of that. And also: it doesn't matter.

What matters is that you're about to learn the canonical text-to-image workflow—the fundamental pattern that everything else in ComfyUI builds on. Once you understand these seven nodes and how they connect, you'll understand 80% of what ComfyUI does.

The other 20% is just... more complicated versions of this same thing.

Let's make a picture.

---

## The Default Workflow: Your New Best Friend

When you first open ComfyUI, you see THIS:

```
[SCREENSHOT: Default workflow with all nodes visible]
```

Seven nodes. Six connections. One purpose: turn text into image.

Let me explain each node, left to right, because ComfyUI workflows read like a book (if books were written by engineers who hate linear storytelling).

---

## Node 1: Load Checkpoint (The Big Dream Machine)

**Location:** Far left, usually at the top
**What it does:** Loads the AI model that will generate your image
**Cat Metaphor:** This is the big sleepy file that knows how to dream pictures

```
╔════════════════════════════╗
║    Load Checkpoint         ║
╟────────────────────────────╢
║ ckpt_name: [dropdown]      ║
║  - v1-5-pruned.safetensors ║
║  - dreamshaper_8.safetensors║
║  - etc.                    ║
╠════════════════════════════╣
║ Outputs:                   ║
║ • MODEL                    ║
║ • CLIP                     ║
║ • VAE                      ║
╚════════════════════════════╝
```

**What is a checkpoint?**

A checkpoint is a file—usually 2-7GB—that contains a trained AI model. Someone (or some company) fed millions of images to a neural network and said "learn what things look like." The result is this file. When you load it, you're essentially waking up a very specialized artist who only knows how to paint in one particular style.

Different checkpoints = different art styles:
- SD 1.5 models: Versatile, fast, lower resolution (512x512 native)
- SDXL models: Higher quality, slower, higher resolution (1024x1024 native)
- Specialty models: Photorealistic, anime, painterly, whatever people trained

**Action Step:**
Click the dropdown on your Load Checkpoint node. You should see at least one .safetensors file. If you see NOTHING, you forgot to download a model (go back to Chapter 1, the section about "The Folder Where Dreams Live").

Pick one. Any one. We're not being picky yet.

---

### STRAIGHT ANSWERS: What are MODEL, CLIP, and VAE?

The Load Checkpoint node outputs three separate things:

**MODEL:** The actual image generator. Takes noise + instructions, outputs less noise.

**CLIP:** The text encoder. Translates your words into numbers the MODEL understands. Named after the OpenAI tech it's based on.

**VAE:** The translator between "latent space" (compressed math) and "pixel space" (actual pictures). Variational Autoencoder. You don't need to understand it.

All three come bundled in the checkpoint file. We split them into separate outputs because sometimes you want to swap just one piece (like using a different VAE for better colors).

---

## Node 2 & 3: CLIP Text Encode (Describing Your Dream)

**Location:** Middle-left, two of them (positive and negative)
**What it does:** Converts your text prompt into mathematical instructions
**Cat Metaphor:** You're describing what you want to dream about (and what you DON'T want)

```
╔════════════════════════════╗
║ CLIP Text Encode (Prompt)  ║
╟────────────────────────────╢
║ text: [large text box]     ║
║                            ║
║ "a cat sleeping on a       ║
║  keyboard, digital art,    ║
║  detailed, trending on     ║
║  artstation"               ║
║                            ║
╠════════════════════════════╣
║ Input: CLIP ←─────────────┼── from Load Checkpoint
╠════════════════════════════╣
║ Output: CONDITIONING       ║
╚════════════════════════════╝
```

You'll have TWO of these nodes:

**Positive Prompt (top one):** What you WANT in the image
**Negative Prompt (bottom one):** What you DON'T WANT in the image

**Your First Prompt:**

Let's start simple. In the positive prompt box, type:

```
a cozy coffee shop interior, warm lighting, plants on shelves,
wooden furniture, morning sunlight, detailed, high quality
```

In the negative prompt box, type:

```
blurry, low quality, distorted, ugly, watermark, text
```

**Why this works:**

The positive prompt is descriptive and specific. It tells the AI:
- Subject: coffee shop interior
- Mood: cozy, warm, morning
- Details: plants, wooden furniture, lighting
- Quality markers: detailed, high quality

The negative prompt tells the AI common failure modes to avoid. AI models sometimes generate blurry messes, weird distortions, or random text. By explicitly saying "not these things," you guide it away from mistakes.

---

### SPECIAL SECTION: Prompt Engineering for Sleepy Cats

**The Basic Formula:**
```
[Main Subject] + [Style/Medium] + [Details] + [Lighting] + [Quality Tags]
```

**Examples:**

**Portrait:**
```
POSITIVE: portrait of an elderly wizard, oil painting style,
long white beard, wise expression, magical atmosphere,
soft lighting, highly detailed, masterpiece

NEGATIVE: ugly, distorted face, bad anatomy, blurry,
low quality, cartoon
```

**Landscape:**
```
POSITIVE: mountain landscape at sunset, dramatic clouds,
alpine lake in foreground, pine trees, orange and purple sky,
photorealistic, 8k quality

NEGATIVE: people, buildings, text, watermark, oversaturated,
blurry
```

**Creature:**
```
POSITIVE: cute baby dragon, sitting on a pile of books,
library setting, fantasy art, detailed scales,
curious expression, warm lighting

NEGATIVE: scary, realistic, dark, horror, distorted anatomy
```

**Prompt Tips:**

1. **Be specific, not vague**
   - BAD: "a nice scene"
   - GOOD: "a sunset over ocean waves, golden hour"

2. **Front-load important words**
   - The model pays more attention to earlier words
   - Put your main subject first

3. **Use style markers**
   - "digital art," "oil painting," "photograph," "pencil sketch"
   - Helps the model understand what aesthetic you want

4. **Quality tags actually work**
   - "detailed," "high quality," "masterpiece," "trending on artstation"
   - These were tags in the training data associated with good images

5. **Commas separate concepts**
   - Think of prompts as tags, not sentences
   - "forest, mushrooms, fog" works better than "There is a forest with mushrooms and fog"

---

## Node 4: Empty Latent Image (The Starting Canvas)

**Location:** Middle section, connected to KSampler
**What it does:** Creates a blank starting point for image generation
**Cat Metaphor:** This is the fuzzy nap dimension where the dream begins

```
╔════════════════════════════╗
║    Empty Latent Image      ║
╟────────────────────────────╢
║ width: 512                 ║
║ height: 512                ║
║ batch_size: 1              ║
╠════════════════════════════╣
║ Output: LATENT             ║
╚════════════════════════════╝
```

**What is latent space?**

Okay. This is where it gets weird.

The AI doesn't actually work with pixels. It works with a compressed mathematical representation of images called "latent space." Think of it like... if regular images are high-resolution photographs, latent space is a blurry thumbnail made of pure math.

The AI generates in this blurry math space because it's faster and more efficient. Then, at the very end, the VAE translates it back to actual pixels you can see.

You don't need to understand the math. You just need to know:
- Empty Latent Image = starting point of pure noise
- Width/Height = final image dimensions
- This gets passed to the sampler, which gradually turns noise into image

**Settings:**

**width / height:** The resolution of your output image

For **SD 1.5 models:**
- Native resolution: 512x512
- Can go higher, but quality may suffer
- Common: 512x512, 512x768 (portrait), 768x512 (landscape)

For **SDXL models:**
- Native resolution: 1024x1024
- Common: 1024x1024, 768x1344, 1344x768

**Important:** Use resolutions divisible by 8. The model works in 8-pixel chunks. 512, 768, 1024 are safe. 513, 750, 1000 will cause errors.

**batch_size:** How many images to generate at once. Start with 1. Increase later when you want variations.

---

## Node 5: KSampler (Where the Magic Happens)

**Location:** Center of the workflow, biggest node
**What it does:** The actual image generation process
**Cat Metaphor:** This is how long you let the dream cook

```
╔════════════════════════════╗
║         KSampler           ║
╟────────────────────────────╢
║ seed: 156680208848723      ║
║ control_after_generate:    ║
║   randomize               ║
║ steps: 20                  ║
║ cfg: 8.0                   ║
║ sampler_name: euler        ║
║ scheduler: normal          ║
║ denoise: 1.0               ║
╠════════════════════════════╣
║ Inputs:                    ║
║ • model ←─────────────────┼── from Load Checkpoint
║ • positive ←──────────────┼── from CLIP Text Encode (positive)
║ • negative ←──────────────┼── from CLIP Text Encode (negative)
║ • latent_image ←──────────┼── from Empty Latent Image
╠════════════════════════════╣
║ Output: LATENT             ║
╚════════════════════════════╝
```

This is the heart of the workflow. Let's break down every setting.

---

### SPECIAL SECTION: KSampler Demystified

| Setting | What It Does | Recommended Starting Value | What Happens If You Change It |
|---------|-------------|---------------------------|-------------------------------|
| **seed** | Random number that determines image variation | Any number (randomize) | Same seed + same settings = identical image. Change seed = different image with same prompt |
| **control_after_generate** | What to do with seed after generation | randomize | "randomize" = new image each time. "fixed" = repeat same image |
| **steps** | How many refinement passes the AI makes | 20-30 | More steps = more refined (diminishing returns after 30). Fewer = faster but rougher |
| **cfg** (Classifier Free Guidance) | How strictly AI follows your prompt | 7-9 | Lower (4-6) = creative/loose. Higher (10-15) = strict but sometimes worse quality |
| **sampler_name** | The algorithm used for generating | euler, euler_a, dpmpp_2m | Different samplers = slightly different aesthetic. Start with euler or dpmpp_2m_karras |
| **scheduler** | How steps are distributed | normal | normal works. "karras" is also popular. Don't worry about this yet |
| **denoise** | How much noise to remove | 1.0 | 1.0 = start from pure noise (txt2img). Lower values for img2img (covered later) |

**Deep Dive: Seed**

The seed is a random number that determines ALL the randomness in generation. If you:
- Use the same seed
- Use the same prompt
- Use the same settings
- Use the same model

You will get the EXACT same image. Pixel-for-pixel identical.

Why does this matter? Because when you generate an image you like, you can note the seed, change ONE thing (like a word in the prompt), and see what changes. This is how you iterate toward the perfect image.

**Set to "randomize"** while exploring. **Set to "fixed"** when you want to iterate on a specific image.

**Deep Dive: Steps**

Each "step" is the AI looking at the noisy image and asking "what should this be?" then making it slightly less noisy.

Step 1: Pure static → "I think I see a shape?"
Step 5: Rough blobs → "Okay, that's a tree, that's sky"
Step 10: Recognizable → "Tree with leaves, blue sky"
Step 20: Detailed → "Oak tree, cumulus clouds, grass texture"
Step 50: Extremely detailed → "...honestly looks the same as step 30"

**Diminishing returns:** Most improvement happens in the first 20 steps. Going to 50 takes longer but doesn't improve much.

**Start with 20.** Increase to 30 if results look rough. Don't go above 50 unless you have a specific reason.

**Deep Dive: CFG (Classifier Free Guidance)**

CFG is "how much should the AI care about your prompt vs just making a nice-looking image?"

- **CFG 1:** Ignores prompt almost entirely, makes pretty pictures of whatever
- **CFG 7-8:** Balanced. Follows prompt, stays creative
- **CFG 15:** VERY strict prompt following, but sometimes adds artifacts or oversaturation
- **CFG 30:** You told it to make a cat and by god there will be a cat even if it looks weird

**Sweet spot: 7-9** for most use cases.

Lower CFG if your images look oversaturated or have weird artifacts.
Higher CFG if the AI isn't following your prompt at all.

**Deep Dive: Sampler**

The sampler is the actual algorithm that removes noise. Different samplers use different math approaches. You don't need to understand the math. You just need to know:

**Recommended samplers:**
- **euler_a:** Fast, good quality, slightly unpredictable (ancestral = adds randomness)
- **dpmpp_2m_karras:** High quality, consistent, slightly slower
- **ddim:** Fast, deterministic, good for img2img
- **euler:** Like euler_a but more predictable

**Start with euler_a or dpmpp_2m_karras.** Experiment later.

---

## Node 6: VAE Decode (Dream-to-Picture Translator)

**Location:** Right side, between KSampler and Save Image
**What it does:** Converts latent space math back into actual pixels
**Cat Metaphor:** The fancy food processor that turns dream-math into pictures

```
╔════════════════════════════╗
║        VAE Decode          ║
╟────────────────────────────╢
║ [no settings]              ║
╠════════════════════════════╣
║ Inputs:                    ║
║ • samples ←───────────────┼── from KSampler
║ • vae ←───────────────────┼── from Load Checkpoint
╠════════════════════════════╣
║ Output: IMAGE              ║
╚════════════════════════════╝
```

This node has no settings. It does one thing: takes the LATENT output from KSampler and translates it to IMAGE.

**What is a VAE?**

Variational Autoencoder. It's two neural networks:
1. Encoder: Image → Latent (compress)
2. Decoder: Latent → Image (decompress)

During generation, we only use the decoder half. We take the latent representation the KSampler created and decode it into pixels.

**Why do we care?**

Different VAEs produce different color/sharpness characteristics. The default VAE bundled with your checkpoint is usually fine, but sometimes you'll swap in a different VAE for better results (more vibrant colors, sharper details).

For now: Just let it do its thing. Don't touch it.

---

## Node 7: Save Image (Making It Real)

**Location:** Far right
**What it does:** Saves the generated image to disk
**Cat Metaphor:** Remembering the dream before you forget it

```
╔════════════════════════════╗
║        Save Image          ║
╟────────────────────────────╢
║ filename_prefix: ComfyUI   ║
╠════════════════════════════╣
║ Input:                     ║
║ • images ←────────────────┼── from VAE Decode
╠════════════════════════════╣
║ [Preview area shows image] ║
╚════════════════════════════╝
```

**Settings:**

**filename_prefix:** What to name your images. Default is "ComfyUI"

The actual filename will be:
```
ComfyUI_00001_.png
ComfyUI_00002_.png
etc.
```

You can change this to organize your images:
- "portrait_" → portrait_00001_.png
- "fantasy_landscape_" → fantasy_landscape_00001_.png

**Where do images save?**

```
ComfyUI/
  output/
    ComfyUI_00001_.png
    ComfyUI_00002_.png
    etc.
```

The preview will also show in the node itself, so you can see your result immediately in the browser.

---

## RUNNING THE WORKFLOW: The Moment of Truth

Okay. Deep breath. Let's actually DO this.

**Step-by-step:**

1. **Verify all connections**
   - Load Checkpoint → CLIP connects to both CLIP Text Encode nodes
   - Load Checkpoint → MODEL connects to KSampler
   - Load Checkpoint → VAE connects to VAE Decode
   - CLIP Text Encode (positive) → CONDITIONING connects to KSampler positive
   - CLIP Text Encode (negative) → CONDITIONING connects to KSampler negative
   - Empty Latent Image → LATENT connects to KSampler latent_image
   - KSampler → LATENT connects to VAE Decode samples
   - VAE Decode → IMAGE connects to Save Image

2. **Check your prompt**
   - Positive: something descriptive
   - Negative: "blurry, low quality"

3. **Check your settings**
   - Empty Latent: 512x512 (if using SD 1.5) or 1024x1024 (if using SDXL)
   - KSampler steps: 20
   - KSampler cfg: 8
   - KSampler sampler: euler_a

4. **Click "Queue Prompt"**
   - It's the big button in the top-right of the interface (or sidebar)

**What happens:**

- The Queue panel will show progress
- You'll see a percentage counter (0% → 100%)
- On your computer, fans may spin up (GPU is working hard)
- After 20-60 seconds (depending on your hardware), the image appears

**It worked!** You'll see a picture in the Save Image node preview.

**It failed?** Jump to "When Your Picture Looks Wrong" section below.

---

## Your First Image: What Now?

Congratulations! You just turned words into pixels using math you don't fully understand. That's INCREDIBLE.

Now let's iterate.

**Exercise 1: Change the seed**
- Click the dice icon next to the seed number in KSampler
- This randomizes the seed
- Click "Queue Prompt" again
- You'll get a different image with the same prompt

Generate 5 images. Notice how they're all different but share similar composition/style.

**Exercise 2: Modify the prompt**
- Change one word in your positive prompt
- Example: "coffee shop interior" → "bookstore interior"
- Keep the seed FIXED (don't randomize)
- Generate again
- Notice what changed vs what stayed the same

**Exercise 3: Adjust CFG**
- Try cfg: 5 (loose/creative)
- Try cfg: 12 (strict/literal)
- Compare to your cfg: 8 result
- Which do you prefer?

**Exercise 4: Adjust steps**
- Try steps: 10 (fast but rough)
- Try steps: 30 (refined)
- Try steps: 50 (very refined)
- Notice diminishing returns after 30

**Exercise 5: Change the sampler**
- Try: euler_a
- Try: dpmpp_2m_karras
- Try: ddim
- Same prompt, same seed, different sampler = slightly different aesthetic

---

## SPECIAL SECTION: When Your Picture Looks Wrong

**Problem:** The image is just noise/static

**Diagnosis:** Something broke in the pipeline

**Fix:**
- Check all connections (are they all connected?)
- Verify you selected a checkpoint in Load Checkpoint
- Make sure width/height are divisible by 8
- Check the console for error messages

---

**Problem:** The image is blurry and low quality

**Diagnosis:** Several possible causes

**Fix:**
- Add quality tags to positive prompt: "detailed, high quality, sharp"
- Add negative prompt: "blurry, low quality, distorted"
- Increase steps to 30
- Check if you're using the right resolution for your model (512 for SD1.5, 1024 for SDXL)
- Try a different checkpoint (some are trained better than others)

---

**Problem:** The image has weird anatomy (extra fingers, distorted faces)

**Diagnosis:** This is a known AI weakness

**Fix:**
- Add to negative prompt: "bad anatomy, distorted, extra limbs, disfigured"
- Increase CFG to 9-10 (stricter prompt following)
- Try a different seed (some seeds just produce weird results)
- Use a checkpoint trained on better anatomy (photorealistic models tend to be better)
- Later: Use ControlNet for pose guidance (Chapter 5)

---

**Problem:** The image doesn't match my prompt at all

**Diagnosis:** CFG too low, or prompt too vague

**Fix:**
- Increase CFG to 10-12
- Make prompt more specific and descriptive
- Front-load important words (put main subject first)
- Add emphasis (covered in Chapter 5)
- Check that you're actually using the positive prompt, not accidentally leaving it blank

---

**Problem:** The image is oversaturated with weird colors

**Diagnosis:** CFG too high, or checkpoint has color issues

**Fix:**
- Lower CFG to 6-7
- Add to negative prompt: "oversaturated, artificial colors"
- Try a different VAE (covered in Chapter 4)
- Try a different checkpoint

---

**Problem:** Generation is VERY slow (minutes per image)

**Diagnosis:** Hardware limitation or inefficient settings

**Fix:**
- Lower resolution (try 512x512)
- Reduce steps to 15-20
- Check if you're using CPU instead of GPU (Chapter 7)
- Close other applications using GPU
- Consider quantized models (Chapter 7)

---

**Problem:** "CUDA Out of Memory" error

**Diagnosis:** Your GPU doesn't have enough VRAM

**Fix:**
- Lower resolution to 512x512
- Reduce batch_size to 1
- Use a smaller checkpoint (SD 1.5 instead of SDXL)
- Enable --lowvram launch flag (Chapter 7)
- Use quantized models (Chapter 7)

---

## Finding Your Output Images

Your generated images are saved to:

```
ComfyUI/output/
```

Each image includes metadata (embedded in the PNG file):
- The exact prompt you used
- All KSampler settings
- The checkpoint name
- The seed

**To re-use settings:**
- Drag the PNG image back into ComfyUI
- It will load the entire workflow that created it
- This is INCREDIBLY useful for sharing workflows or revisiting old images

---

## Saving Your Workflow

You just created an image. You want to remember this setup.

**To save:**
1. Click "Save" button (top menu, or Ctrl+S)
2. Choose a filename: "my_first_workflow.json"
3. It saves to your downloads folder (or wherever your browser saves files)

**To load:**
1. Click "Load" button
2. Select your saved .json file
3. The entire workflow appears on the canvas

**Workflow files are TINY** (a few kilobytes). Save variations often. Organize them in folders:
- portraits/
- landscapes/
- creatures/
- experiments/

---

## Understanding the Pipeline: Why This Order?

Let's zoom out. Why is the workflow structured this way?

**Text → Math → Image**

1. **Load Checkpoint:** Wake up the AI
2. **CLIP Text Encode:** Turn your words into math the AI understands
3. **Empty Latent Image:** Create a starting canvas of noise
4. **KSampler:** Gradually turn noise into a structured image (in latent space)
5. **VAE Decode:** Turn latent-space math into actual pixels
6. **Save Image:** Write pixels to disk

This is the CANONICAL pipeline. Almost everything else in ComfyUI is a variation on this:
- Want to start with an existing image? Replace "Empty Latent Image" with "Load Image"
- Want more control? Add ControlNet before KSampler
- Want higher resolution? Add upscaling after VAE Decode
- Want to refine details? Add a second KSampler pass

But the core flow is always: **Prompt → Latent → Sample → Decode → Image**

---

## Tips for Better Results

**Tip 1: Use reference phrases from good images**

If you find an image you like (on CivitAI, ArtStation, etc.), read its prompt. Note phrases that work well. Build your own library of effective tags.

**Tip 2: Prompt templates**

Create text files with formula templates:

```
PORTRAIT TEMPLATE:
portrait of [subject], [style], [clothing/features],
[expression], [lighting], highly detailed, [quality tags]

LANDSCAPE TEMPLATE:
[location] landscape, [time of day], [weather],
[foreground elements], [background elements],
[style], [quality tags]
```

Fill in the brackets, paste into ComfyUI.

**Tip 3: Keep a generation log**

When you get a good result, note:
- Checkpoint used
- Prompt (positive and negative)
- Settings (steps, cfg, sampler)
- Seed

This becomes your personal recipe book.

**Tip 4: Test in batches**

Want to explore variations quickly?
- Keep everything fixed
- Set seed to "randomize"
- Set batch_size to 4
- Generate once → get 4 variations
- Pick the best, note the seed, iterate on that one

**Tip 5: Less is often more**

Beginner instinct: "More words = better image"
Reality: "Specific, concise words = better image"

Compare:
- **BAD:** "a beautiful amazing gorgeous stunning landscape with mountains and trees and a river and sunset and clouds and it's really pretty and detailed"
- **GOOD:** "mountain landscape at sunset, river valley, pine trees, dramatic clouds, oil painting style"

The second is clearer, more directed, and will produce better results.

---

## CAT TAKES OFF THE MASK: What Is Actually Happening?

Okay. Real talk. No metaphors.

**Diffusion models work backwards from noise.**

The AI was trained on millions of images that were DELIBERATELY NOISED—made progressively blurrier and more static-filled until they were pure random noise.

The model learned to REVERSE this process. Given a noisy image, it predicts "what would this look like one step less noisy?"

When you generate an image:
1. Start with 100% noise (random static)
2. The model looks at it through your prompt and predicts "one step less noisy"
3. Apply that prediction, creating a slightly-less-noisy image
4. Repeat 20 times (or however many steps you set)
5. By step 20, the noise has been refined into a coherent image matching your prompt

**The prompt guides each denoising step.** At each step, the AI asks "given this text description, what should this noise become?"

**The seed determines the starting noise pattern.** Same seed = same starting static = same final image (if all other variables are equal).

**CFG controls how much the prompt influences each step** vs the model just making aesthetically pleasing choices.

That's it. Everything else is variations on this core loop.

---

## Chapter Summary: What You Learned

You can now:
- ✓ Understand the seven nodes of the default txt2img workflow
- ✓ Write effective prompts using the basic formula
- ✓ Configure KSampler settings (seed, steps, CFG, sampler)
- ✓ Generate your first image from text
- ✓ Iterate on prompts and settings to improve results
- ✓ Find your generated images in the output folder
- ✓ Debug common issues (blurry images, anatomy problems, etc.)
- ✓ Save and load workflows for reuse

**The Workflow in Three Sentences:**
Load a model. Describe what you want. The AI gradually refines noise into an image matching your description.

**The Most Important Thing to Remember:**
Same seed + same settings + same prompt = identical image. Change ONE variable at a time to understand what each setting does.

---

## Practice Exercises

**Exercise Set 1: Prompt Practice**

Generate images for each of these prompts. Use the same seed for all five. Notice how the prompt structure affects results.

1. "cat"
2. "orange tabby cat, sitting"
3. "orange tabby cat sitting on a wooden table, morning sunlight"
4. "portrait of an orange tabby cat sitting on a wooden table, morning sunlight streaming through window, cozy home interior, detailed fur, photorealistic"
5. Take #4, add negative prompt: "blurry, cartoon, painting, low quality"

**Exercise Set 2: Settings Exploration**

Use this prompt for all:
```
POSITIVE: fantasy castle on a cliff, dramatic sunset, ocean below,
detailed architecture, epic scale, digital art

NEGATIVE: blurry, low quality, people, modern
```

Generate with:
1. steps: 10, cfg: 8
2. steps: 20, cfg: 8
3. steps: 30, cfg: 8
4. steps: 20, cfg: 5
5. steps: 20, cfg: 12
6. steps: 20, cfg: 8, sampler: euler_a
7. steps: 20, cfg: 8, sampler: dpmpp_2m_karras

Keep the same seed for all. Note differences.

**Exercise Set 3: Seed Variation**

Use this prompt:
```
POSITIVE: steampunk airship, floating in clouds, intricate machinery,
brass and copper details, fantasy art, detailed

NEGATIVE: blurry, modern, low quality
```

Settings: steps 20, cfg 8, sampler euler_a

Generate 10 times with randomized seed. Notice how composition varies but style stays consistent.

**Exercise Set 4: Resolution Experiments**

Same prompt, same seed, different resolutions:
1. 512x512 (square)
2. 512x768 (portrait)
3. 768x512 (landscape)
4. 1024x1024 (if using SDXL)

Notice how aspect ratio affects composition.

---

## Next Chapter Preview

You can now make pictures. One at a time. With one model.

But there are HUNDREDS of models. Thousands. Some dream in anime, some in photorealism, some in watercolor. And there are these little files called LoRAs that add specific styles or characters to any model.

Chapter 4 is about the Model Zoo: where to find these dream machines, how to install them, how to use them, and how to not fill your hard drive with 500GB of checkpoints you'll never use.

(Spoiler: You'll still fill your hard drive. But at least you'll understand why.)

---

## Nyquil Cat's Final Thoughts

You made a picture from words. FROM WORDS.

I know I'm supposed to be drowsy and unimpressed, but honestly? This is absurd and wonderful. Ten years ago this was science fiction. Now you can do it on your computer in 30 seconds.

The default workflow is your foundation. Master it. Understand it. Experiment with it. Because every complicated workflow you'll encounter later is just... this, with extra steps.

Seven nodes. Six connections. Infinite possibilities.

Now go make weird art. I'm taking a nap.

*— Nyquil Cat*

---

**Chapter 3 Complete**
**Word Count:** ~3,500 words
**Status:** Ready for review and integration
**Next Steps:** Chapter 4 (The Model Zoo)

---

### Quick Reference: Default Workflow Checklist

```
□ Load Checkpoint
  - Selected a .safetensors model

□ CLIP Text Encode (Positive)
  - Written descriptive prompt
  - Used formula: subject + style + details + quality

□ CLIP Text Encode (Negative)
  - Added: blurry, low quality, distorted

□ Empty Latent Image
  - Width/Height divisible by 8
  - 512x512 for SD1.5, 1024x1024 for SDXL

□ KSampler
  - seed: randomize (or fixed for iteration)
  - steps: 20-30
  - cfg: 7-9
  - sampler_name: euler_a or dpmpp_2m_karras

□ VAE Decode
  - No settings to check

□ Save Image
  - filename_prefix: whatever you want

□ All connections verified

□ Queue Prompt clicked

□ Image appeared in preview

□ Image saved to ComfyUI/output/
```

---

**APPENDIX: Sampler Comparison Chart**

| Sampler | Speed | Quality | Consistency | Best For |
|---------|-------|---------|-------------|----------|
| euler | Fast | Good | High | General use, fast iteration |
| euler_a | Fast | Good | Medium | Creative variation |
| dpmpp_2m | Medium | Excellent | High | High-quality final renders |
| dpmpp_2m_karras | Medium | Excellent | High | High-quality final renders |
| ddim | Fast | Good | Very High | Img2img, reproducibility |
| dpmpp_sde | Slow | Excellent | Low | Artistic, varied results |
| dpm_2 | Medium | Good | Medium | General use |
| lms | Fast | Good | Medium | Fast generation |
| heun | Slow | Excellent | High | Maximum quality, slow |

**Recommendation:** Start with **euler_a** for experimenting, **dpmpp_2m_karras** for final renders.

---

**APPENDIX: CFG Scale Visual Guide**

```
CFG 1-3:   [Abstract, ignores prompt, artistic freedom]
CFG 4-6:   [Loose interpretation, creative, varied]
CFG 7-9:   [Balanced, follows prompt, natural look] ← START HERE
CFG 10-12: [Strict prompt following, occasional artifacts]
CFG 13-20: [Very literal, often oversaturated/distorted]
CFG 20+:   [Extreme artifacts, not recommended]
```

Most workflows live in the 7-9 range. Adjust based on results.

---

*End of Chapter 3*
