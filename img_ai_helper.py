# img_ai_helper.py
import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login

# Read token to access marian3860 Huggingface
access_token = "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"
login(token=access_token)

base_model_id = "marian3860/miniSD"  # If pixel-art-xl lora, need base-model: "stabilityai/stable-diffusion-xl-base-1.0"
pipe = DiffusionPipeline.from_pretrained(
    base_model_id,
    variant="fp16",
    torch_dtype=torch.float16
).to("cuda")
# pipe.load_lora_weights("nerijs/pixel-art-xl", weight_name="pixel-art-xl.safetensors")
pipe.enable_xformers_memory_efficient_attention()
pipe.enable_attention_slicing()


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

    image = pipe(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=n_steps,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_samples,
        guidance_scale=guidance_scale,
        generator=generator,
    ).images[0]

    image.save(f".\Images\{prompt}-{seed}.png")

    return image
