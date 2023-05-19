import base64
import os
import requests
from PIL import Image
import io

engine_id = "stable-diffusion-v1-5"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = "sk-IlMCIbwsCPBuzh5LI7mtw41sUtnGIS19ghmV8INKhDGNYcat"
if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/text-to-image",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "text_prompts": [
            {
                "text": "A shining,attractive man,like a greek god,make women workship him,ugly:-1.0, too many fingers:-1.0"
            }
        ],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30,
    },
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

if not os.path.exists('out'):
    os.makedirs('out')
    
#for i, image in enumerate(data["artifacts"]):
   # with open(f"./out/v1_txt2img_{i}.png", "wb") as f:
    #    f.write(base64.b64decode(image["base64"]))
        
image_data = data["artifacts"][0]["base64"]

# decode the base64 image data
decoded_image_data = base64.b64decode(image_data)

# create a Pillow image object from the decoded image data
pil_image = Image.open(io.BytesIO(decoded_image_data))

# display the image
pil_image.show()
print(image_data)
        



