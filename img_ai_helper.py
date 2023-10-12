# img_ai_helper.py
import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login
import rembg

# Read token to access marian3860 Huggingface
access_token = "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"
login(token=access_token)
base_model_id = "marian3860/miniSD"
# If pixel-art-xl lora, need base-model: "stabilityai/stable-diffusion-xl-base-1.0"
pipe = None


def model_pipe():
    global pipe
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained(
            base_model_id,
            variant="fp16",
            torch_dtype=torch.float16
        ).to("cuda")
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_attention_slicing()
        # disables safety checks
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
    n_steps = 40
    negative_prompt = "text, wrong, watermark"
    num_samples = 1
    height = 512
    width = 256
    guidance_scale = 7
    generator = torch.Generator(device='cuda')
    seed = generator.seed()
    generator = generator.manual_seed(seed)

    image = model_pipe()(
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
    image.save(f".\Images\{prompt}-{seed}.png")

    return image


def sanitize_filename(filename):
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
    return filename


def remove_background(img):
    return rembg.remove(img)
