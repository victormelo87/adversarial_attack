from PIL import Image
from io import BytesIO
import http.client
import numpy as np


def load_image(image_path):
    try:
        image = Image.open(image_path)
        print(f"Imagem carregada com sucesso: {image_path}")
        return image
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return None

def save_image(image, file_path):
    try:
        image.save(file_path, format="JPEG")
        print(f"Imagem salva com sucesso: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")


def send_image(image, url):
    if url.startswith("http://"):
        url = url.replace("http://", "")
    elif url.startswith("https://"):
        url = url.replace("https://", "")

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0) 
    image_data = buffer.read()

    connection = http.client.HTTPConnection(host)
    headers = {
        "Content-Type": "image/jpeg",
        "Content-Length": str(len(image_data))
    }

    connection.request("POST", path, body=image_data, headers=headers)
    response = connection.getresponse()

    if response.status == 200:
        print("Imagem enviada com sucesso!")
        response_data = response.read().decode("utf-8")
        return response_data  
    else:
        print(f"Erro ao enviar a imagem. Status: {response.status}")
        return None