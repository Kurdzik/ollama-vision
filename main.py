from fastapi import FastAPI
from fastapi import UploadFile
import os
from ollama import Client

app = FastAPI()


@app.post("/upload")
async def upload_image(image: UploadFile):

    file_bytes = await image.read()

    os.makedirs('/tmp_images', exist_ok=True)

    save_path = f'/tmp_images/{image.filename}'
    with open(save_path, 'wb') as f:
        f.write(file_bytes)

    return {f'image saved to {save_path}'}


@app.get("/ask")
async def analyze_image(prompt: str, img_path, model: str = "llava:7b"):
    ollama_client = Client(host='http://ollama:11434')

    ollama_client.pull(model)

    res = ollama_client.chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [img_path]
            }
        ]
    )

    return {res['message']['content']}