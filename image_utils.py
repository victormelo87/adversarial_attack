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

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n"
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + image_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body))
    }

    try:
        print(f"Conectando ao host: {host}")
        connection = http.client.HTTPConnection(host)

        print("Enviando a imagem para o servidor...")
        connection.request("POST", path, body=body, headers=headers)
        response = connection.getresponse()

        response_data = response.read().decode("utf-8").strip()
        print(f"Resposta do servidor: {response_data}")
        return response_data if response.status == 200 else None
    except Exception as e:
        print(f"Erro durante a conexão ou envio: {e}")
        return None
    finally:
        connection.close()
