import matplotlib.pyplot as plt
from diffusers import DiffusionPipeline
import torch

def generate_image(prompt:str, negative_prompt:str=None, seed:int=42, base_sdxl=None, refiner=None):
  """Generate image given a textual prompt and a negative prompt. We use stable-diffusion-xl-base-1.0 as base model
    and stable-diffusion-xl-refiner-1.0 as a refiner model, both available on huggingface."""
  
  print(f"SEED: {seed} - PROMPT: {prompt}")
  torch.manual_seed(seed)

  # How to employ the mixture of experts model
  n_steps = 40
  high_noise_frac = 0.8

  # Run the base first
  image = base_sdxl(
      prompt=prompt,
      num_inference_steps=n_steps,
      denoising_end=high_noise_frac,
      output_type="latent",
      negative_prompt=negative_prompt
  ).images

  # Run the refiner next
  image = refiner(
      prompt=prompt,
      num_inference_steps=n_steps,
      denoising_start=high_noise_frac,
      image=image,
  ).images[0]

  return image


def load_image_models():
  """Load models"""
  # SDXL 1.0 - BASE MODEL + REFINER MODEL
  # Load model - stable-diffusion-xl-base-1.0
  base_sdxl = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                          torch_dtype=torch.float16,
                                          use_safetensors=True,
                                          variant="fp16",
                                          force_download=True,
                                          resume_download=False)
  base_sdxl.to("cuda")
  base_sdxl.enable_attention_slicing()

  # Load model - stable-diffusion-xl-refiner-1.0
  refiner = DiffusionPipeline.from_pretrained(
      "stabilityai/stable-diffusion-xl-refiner-1.0",
      text_encoder_2=base_sdxl.text_encoder_2,
      vae=base_sdxl.vae,
      torch_dtype=torch.float16,
      use_safetensors=True,
      variant="fp16",
  )
  refiner.enable_attention_slicing()
  refiner.enable_model_cpu_offload()

  return base_sdxl, refiner


def generate_cover(prompt:str, negative_prompt:str=None, seed:int=42, save_filename:str=None):
  """Generates a cover for our podcast. It load models, generate image given prompts and return image."""
  base_sdxl, refiner = load_image_models()
  image = generate_image(prompt,
                          negative_prompt=negative_prompt,
                          seed=seed,
                          base_sdxl=base_sdxl,
                          refiner=refiner)
  if save_filename:
    image.save(save_filename)
  return image