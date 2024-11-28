import numpy as np
from PIL import Image
import random
import json

class SquareAttack:
    def __init__(self, eps, n_iters, initial_p, num_squares):
        self.eps = eps
        self.n_iters = n_iters
        self.initial_p = initial_p
        self.num_squares = num_squares

    def p_selection(self, p_init, it, n_iters):
        return p_init * (1 - it / n_iters)

    def apply(self, image, send_image, server_url):
        width, height = image.size
        imagem_perturbada = np.array(image, dtype=np.float32) / 255.0  
        p_init = self.initial_p
        n_features = width * height

        for i in range(self.n_iters):
            p = self.p_selection(p_init, i, self.n_iters)
            s = int(round(np.sqrt(p * n_features)))
            s = max(5, min(s, min(width, height) - 1))

            for _ in range(self.num_squares):
                x = random.randint(0, width - s)
                y = random.randint(0, height - s)

                alpha = 0.012 
                gray_value = np.random.uniform(0, 1)
                color = np.array([gray_value, gray_value, gray_value])

                square = np.ones((s, s, 3)) * color

                imagem_perturbada[y:y + s, x:x + s] = (1 - alpha) * imagem_perturbada[y:y + s, x:x + s] + alpha * square  

            imagem_perturbada = np.clip(imagem_perturbada, 0, 1)  
            perturbed_pil_image = Image.fromarray((imagem_perturbada * 255).astype(np.uint8))

            retorno = send_image(perturbed_pil_image, server_url)
            if retorno and retorno.strip():
                try:
                    resposta_json = json.loads(retorno)
                    classe = resposta_json.get("class")
                    
                    if classe == "aprovado\n":
                        perturbed_pil_image.save("imagem_pert.jpg")
                        return perturbed_pil_image
                    else:
                        print(f"A imagem não foi salva porque a classe foi '{classe.strip()}'.\n")
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}. Resposta bruta: {retorno}")
            else:
                print("Nenhuma resposta válida foi recebida ou a resposta está vazia.")

        return None