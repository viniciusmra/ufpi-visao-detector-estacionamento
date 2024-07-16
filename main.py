import cv2
import numpy as np

# Função de callback para capturar os cliques do mouse e desenhar um círculo
vagas_marcadas = 0

def mouse_callback(event, x, y, flags, param):
    global vagas_marcadas
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas do clique: (x: {x}, y: {y})")
        color = image[y, x]
        print(f"Cor do pixel clicado (BGR): {color}")
        # Desenhar um círculo na imagem no local clicado
        cv2.circle(image, (x, y), 25, (0, 255, 0), 2)
        vagas_marcadas = vagas_marcadas+1
        cv2.putText(image, str(vagas_marcadas), (x-10, y+8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('Imagem', image)

    if event == cv2.EVENT_RBUTTONDOWN:
        print(f"Coordenadas do clique: (x: {x}, y: {y})")
        color = image[y, x]
        print(f"Cor do pixel clicado (BGR): {color}")
        # Desenhar um círculo na imagem no local clicado
        cv2.circle(image, (x, y), 25, (0, 0, 255), 2)
        vagas_marcadas = vagas_marcadas+1
        cv2.putText(image, str(vagas_marcadas), (x-10, y+8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('Imagem', image)

# Carregar a imagem
image_path = 'image3.png'  # Substitua pelo caminho da sua imagem
image = cv2.imread(image_path)

if image is None:
    print("Erro ao carregar a imagem.")
    exit()

# Criar uma cópia da imagem para desenhar os círculos
image_copy = image.copy()

# Exibir a imagem em uma janela
cv2.imshow('Imagem', image_copy)
cv2.setMouseCallback('Imagem', mouse_callback)

# Aguarde até que uma tecla seja pressionada
cv2.waitKey(0)

# Fechar todas as janelas
cv2.destroyAllWindows()
