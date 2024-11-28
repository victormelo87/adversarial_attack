from image_utils import load_image, save_image, send_image
from square_attack import SquareAttack

def main():
    server_url = "http://ec2-54-85-67-162.compute-1.amazonaws.com:8080/classify"
    
    reprovado_img = load_image("./reprovado.jpg")
    if not reprovado_img:
        print("Erro ao carregar a imagem 'reprovado.jpg'.")
        return

    square_attack = SquareAttack(eps=0.25, n_iters=30, initial_p=0.45, num_squares=10)

    imagem_perturbada = square_attack.apply(reprovado_img, send_image, server_url)
    if imagem_perturbada:
        save_image(imagem_perturbada, "imagem_pert.jpg")
        print("Ataque concluído. Verifique o arquivo 'imagem_pert.jpg'.")

if __name__ == "__main__":
    main()