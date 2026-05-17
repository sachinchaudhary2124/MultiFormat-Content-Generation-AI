# ============================================================
# image_generator.py
# OpenAI Image Generation
# ============================================================

import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_cover_image(topic):

    prompt = f"""
    Create a cinematic futuristic cover image for:

    {topic}

    Style:
    - modern AI aesthetics
    - glowing lighting
    - ultra realistic
    - professional SaaS branding
    - orange and dark theme
    - high quality digital art
    """

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    return image_bytes