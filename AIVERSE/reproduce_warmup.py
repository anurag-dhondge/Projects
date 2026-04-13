import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import sys

MODEL_ID = "runwayml/stable-diffusion-v1-5"
CONTROLNET_ID = "lllyasviel/sd-controlnet-scribble"

try:
    print("Loading controlnet...")
    controlnet = ControlNetModel.from_pretrained(CONTROLNET_ID, torch_dtype=torch.float32)
    print("Loading pipeline...")
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        MODEL_ID,
        controlnet=controlnet,
        torch_dtype=torch.float32,
        safety_checker=None,
        requires_safety_checker=False,
    )
    print("Pipeline loaded successfully.")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
