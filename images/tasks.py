# tasks.py
from celery import shared_task
import requests
from django.conf import settings
from .models import GeneratedImage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from PIL import Image
import io
import base64

@shared_task
def generate_image(prompt):
    print("Starting image generation for prompt:", prompt)
    api_key = settings.STABILITY_API_KEY
    api_url = 'https://api.stability.ai/v2beta/stable-image/generate/ultra'

    try:
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            },
            files={
                'prompt': (None, prompt),
                'output_format': (None, 'webp')
            }
        )
        response.raise_for_status()

        response_json = response.json()
        image_base64 = response_json.get('image')

        if not image_base64:
            raise ValueError("No image data found in response")

        image_content = base64.b64decode(image_base64)
        print("-----4-------")
        print(generate_image.request.id)
        image_url = save_image(image_content)
        print("-----5---------", image_url)
        print(type(generate_image.request.id))
        if image_url:
            print("----------------")
            try:
                print(generate_image.request.id)
                print(image_url)
                print(prompt)
                GeneratedImage.objects.create(task_id=generate_image.request.id,prompt=prompt,image=image_url)
            except Exception as Err:
                print(str(Err))
            print("Image successfully saved with URL:", image_url)
        else:
            print("Failed to save image.")
    except requests.RequestException as e:
        print("Request error:", e)
    except Exception as e:
        print("An error occurred:", e)

def save_image(image_content):
    try:
        print("----1---------")
        image = Image.open(io.BytesIO(image_content))
        image = image.convert("RGB")
        filename = f"generated_image_{uuid.uuid4()}.jpg"
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        file_path = default_storage.save(f"images/{filename}", ContentFile(buffer.read()))
        print("------2----------------")
        return default_storage.url(file_path)
    except Exception as e:
        print("Error saving image:", e)
        return None
