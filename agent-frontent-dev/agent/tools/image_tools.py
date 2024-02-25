import base64
import os
import tempfile
from PIL import Image

import openai


def encode_image(image_path: str) -> str:
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def save_and_encode_image(image: Image.Image) -> str:
    """Save an image and return the base64 string."""
    with tempfile.TemporaryDirectory() as temp_dir:
        image_path = os.path.join(temp_dir, "temp_image.jpg")
        image.save(image_path)
        return encode_image(image_path)


class OpenAIVisionModel:
    def __init__(self):
        self.model = "gpt-4-vision-preview"
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
    
    def analyse_image(self, message: str, image: Image.Image) -> str:
        """Analyse an image and return the result as a string."""
        base64_image = save_and_encode_image(image)
        response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": message
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                }
                },
            ],
            }
        ],
        max_tokens=1024,
        )

        return response.choices[0].message.content


def analyse_image_tool(image: Image.Image):
    message = "Describe the image in the deepest detail possible."
    image_model = OpenAIVisionModel()
    image_description = image_model.analyse_image(message, image)
    return image_description
