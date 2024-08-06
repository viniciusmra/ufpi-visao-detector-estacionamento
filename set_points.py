import cv2
import numpy as np

# Variáveis globais para armazenar os pontos clicados
video_path = r"best2_video_el.mp4"
#video_path = r"Estacionamento - Daniel.mp4"

points = []
number_spots = 3
max_height = 800
reference_frame_index = 1

H_spots_points = []
spots_points = []

# Função de callback do mouse
def click_event(event, x, y, flags, param):
    # se os quatro pontos ja tiverem sido marcados, para
    if len(points) == 4:
        return
    
    image_copy = image_resized.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(image_resized, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('Imagem', image_resized)
        if len(points) == 4:
            draw_grid(points, number_spots)

    if event == cv2.EVENT_MOUSEMOVE:
        if len(points) == 0:
            return
        if len(points) > 1:
            for i in range(0, len(points) - 1):
                cv2.line(image_copy, points[i], points[i+1], (0, 255, 0), 2)
        cv2.line(image_copy, (x, y), points[-1], (0, 255, 0), 2)
        cv2.line(image_copy, (x, y), points[0], (0, 255, 0), 2)
        cv2.imshow('Imagem', image_copy)

# Função para desenhar o quadriculado
def draw_grid(raw_points, number_of_spots):
    # Ajustar os pontos para a escala da imagem original
    source_points = np.array([(int(x * scale_width), int(y * scale_height)) for x, y in raw_points], dtype='float32')
    
    # Definir os pontos correspondentes na imagem destino (destino será uma grade regular)
    grid_size = 500 # pixels
    width_grid = grid_size * number_of_spots
    height_grid = 2*grid_size
    destination_points = np.array([[0, 0], [width_grid, 0], [width_grid, height_grid], [0, height_grid]], dtype='float32')
    
    # Calcular a transformação de perspectiva
    M = cv2.getPerspectiveTransform(source_points, destination_points)
    M_inv = np.linalg.inv(M)
    
    # Criar uma imagem vazia para o quadriculado
    grid_image = np.zeros((height_grid, width_grid, 3), dtype='uint8')
    
    index = 1
    
    for index in range(number_of_spots):
        points = [(destination_points[0][0] + index * grid_size, destination_points[0][1]), 
                  (destination_points[0][0] + (index + 1) * grid_size, destination_points[1][1]), 
                  (destination_points[0][0] + (index + 1) * grid_size, destination_points[2][1]),
                  (destination_points[0][0] + index * grid_size, destination_points[3][1])]
        H_spots_points.append(points)

    for spot in H_spots_points:
        points = []
        for point in spot:
            point_homogeneous = np.array([point[0], point[1], 1.0])  # Converte para coordenadas homogêneas
            transformed_point_homogeneous = M_inv @ point_homogeneous  # Aplica a matriz inversa
            transformed_point = transformed_point_homogeneous[:2] / transformed_point_homogeneous[2]  # Converte de volta para coordenadas cartesianas
            points.append(tuple(transformed_point.astype(int)))
        spots_points.append(points)
    
    index = 1
    for i in range(0, width_grid, grid_size):
        text = str(index)
        index += 1

        # Propriedades do texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 13
        font_thickness = 20
        text_color = (0, 0, 0)
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
        rect_x, rect_y = i, 0
        rect_w, rect_h = grid_size, height
        text_x = rect_x + (rect_w - text_width) // 2
        text_y = rect_y + (rect_h + text_height) // 2

        # Preenchimento
        cv2.rectangle(grid_image, (i, 0), (i + grid_size, height_grid), (0, 80, 0), -1)

        # Borda
        cv2.rectangle(grid_image, (i, 0), (i + grid_size, height_grid), (255, 255, 255), 12)

        # Texto
        cv2.putText(grid_image, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)



    
    # Aplicar a transformação inversa para obter o quadriculado na perspectiva original
    grid_warped = cv2.warpPerspective(grid_image, np.linalg.inv(M), (width, height))

    # transformed_image = cv2.warpPerspective(image, M, (width_grid, height_grid))
    # print("primeira mensagem")
    # print(transformed_image.shape)
    # print("segunda")
    # print(grid_image.shape)
    # combined2 = cv2.addWeighted(transformed_image, 1, grid_image, 1, 0)

    
    # Sobrepor o quadriculado verde na imagem original
    combined = cv2.addWeighted(image, 1, grid_warped, 1, 0)
    
    # Redimensionar a imagem final para exibição
    combined_resized = cv2.resize(combined, (int(width * scale), int(height * scale)))
    
    # Mostrar a imagem resultante
    cv2.imshow('Imagem', combined_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Carregar a imagem
cap = cv2.VideoCapture(video_path)

# Verificar se o vídeo foi aberto com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()
index = 0
while index < reference_frame_index:
    ret, frame = cap.read()
    index += 1

image = frame

#image = cv2.imread('img1.jpg')
height, width, _ = image.shape

# Redimensionar a imagem para uma altura máxima de 800 pixels mantendo a proporção

scale = max_height / height
image_resized = cv2.resize(image, (int(width * scale), max_height))

# Escala para ajustar os pontos de volta para a imagem original
scale_width = width / (width * scale)
scale_height = height / max_height

# Mostrar a imagem redimensionada e capturar os cliques do mouse
cv2.imshow('Imagem', image_resized)
cv2.setMouseCallback('Imagem', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("reference_frame.png", frame)
with open("points.txt", 'w') as arquivo:
    print(spots_points)
    for spot in spots_points:
        for point in spot:
            arquivo.write(str(point[0]) + ", " + str(point[1]) + "\n")

    # points = np.array([(int(x * scale_width), int(y * scale_height)) for x, y in points], dtype='float32')

    # arquivo.write(str(number_spots) + "\n")
    # for item in points:
    #     linha = ', '.join(map(str, item))  # Converte os elementos da tupla para strings e os junta com ', '
    #     arquivo.write(linha + "\n")


