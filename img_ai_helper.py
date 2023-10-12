# img_ai_helper.py
import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login
import rembg
import re

# If pixel-art-xl lora, need base-model: "stabilityai/stable-diffusion-xl-base-1.0"
pipe = None


def model_pipe(base_model_id):
    use_access_token = base_model_id.startswith("marian3860")
    if use_access_token:
        access_token = "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"
        login(token=access_token)
    global pipe
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained(
            base_model_id,
            variant="fp16",
            torch_dtype=torch.float16
        ).to("cuda")
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_attention_slicing()

        # Disables safety checks
        def disabled_safety_checker(images, clip_input):
            if len(images.shape) == 4:
                num_images = images.shape[0]
                return images, [False] * num_images
            else:
                return images, False

        pipe.safety_checker = disabled_safety_checker
    return pipe


def generate_character_image(character_info):
    prompt = f"{character_info}, full body, game character, 100% white background, pixelart"
    n_steps = 30
    negative_prompt = "text, wrong, watermark"
    num_samples = 1
    height = 512
    width = 256
    guidance_scale = 7
    generator = torch.Generator(device='cuda')
    seed = generator.seed()
    generator = generator.manual_seed(seed)
    mini_sd_pipe = "marian3860/miniSD"
    image = model_pipe(mini_sd_pipe)(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=n_steps,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_samples,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images[0]
    prompt = sanitize_filename(prompt.strip())
    image.save(f"./Images/{prompt}-{seed}.png")
    torch.cuda.empty_cache()
    return image


def generate_bg_image(story, width=1024, height=1024):
    prompt = f"Wide panoramic view with no people, {story}"
    n_steps = 20
    negative_prompt = "text, wrong, watermark, fog"
    num_samples = 1
    guidance_scale = 5
    generator = torch.Generator(device='cuda')
    seed = generator.seed()
    generator = generator.manual_seed(seed)
    xl_base_pipe = "stabilityai/stable-diffusion-xl-base-1.0"
    image = model_pipe(xl_base_pipe)(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=n_steps,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_samples,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images[0]
    prompt = sanitize_filename(prompt.strip())
    image.save(f"./Images/{story}-{seed}.png")
    torch.cuda.empty_cache()
    return image


def sanitize_filename(filename, word_limit=20):
    # Define a dictionary to map invalid characters to their replacements
    replace_dict = {
        '\\': '-',
        '\n': '-',
        '/': '-',
        ':': '¦',
        '*': '¤',
        '?': '¿',
        '"': 'ˮ',
        '<': '«',
        '>': '»',
        '|': '│',
    }
    # Replace invalid characters with their corresponding replacements
    for char, replacement in replace_dict.items():
        filename = filename.replace(char, replacement)
    # Remove extra spaces and limit the filename to a certain number of words
    words = re.findall(r'\S+', filename)
    limited_filename = ' '.join(words[:word_limit])
    return limited_filename


def remove_background(img):
    return rembg.remove(img)
