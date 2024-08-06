import cv2
import numpy as np
from parking import Parking
import time

video_path = r"best2_video_el.mp4"
#video_path = r"Estacionamento - Daniel.mp4"
park_points_file = r"park_points1.txt"
reference_frame_file = r"reference_frame1.png"
target_height = 800

cap = cv2.VideoCapture(video_path)

reference_frame = cv2.imread(reference_frame_file)
parking = Parking(park_points_file, reference_frame)

def scale_image(image, target_height):
    height, width, _ = image.shape
    scale = target_height / height
    image_resized = cv2.resize(image, (int(width * scale), target_height))
    scale_width = width / (width * scale)
    scale_height = height / target_height

    return image_resized, scale_width, scale_height

def get_spots_polygons(parking, shape):
    spots_polygons = np.zeros((shape[0], shape[1], 3), dtype='uint8')
    
    for spot in parking.parking_spots:
        if spot.occupied:
            spots_polygons = cv2.add(spots_polygons, spot.occupied_polygon)
        else:
            spots_polygons = cv2.add(spots_polygons, spot.empty_polygon)
    
    return spots_polygons
index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo.")
        break

    height, width, _ = frame.shape

    polygons_image = get_spots_polygons(parking, (height, width))
    
    asd = parking.compare_colored_frames(frame)
    for spot in parking.parking_spots:
        spot_diff = spot.get_spot_diff(asd)
        spot.check_spot(spot_diff)

    reference_with_polygons = cv2.addWeighted(reference_frame, 1, polygons_image, 1, 0)
    
    output_image = np.zeros_like(frame)
    cv2.copyTo(frame, asd, output_image)
    
    cv2.copyTo(reference_with_polygons, 255 - asd, output_image)
    
    resized_image, _, _ = scale_image(output_image, 800)
    
    cv2.imshow('Video', resized_image)

    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # Barra de espaço
        continue
    elif key == 27:  # Tecla Esc para sair
        break