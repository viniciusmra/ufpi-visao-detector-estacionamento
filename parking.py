from spots import Spot
import cv2
import numpy as np

class Parking:
    def __init__(self, file,reference_frame):
        self.file = file
        self.parking_spots = []
        self.reference_frame = reference_frame
        height, width, _ = self.reference_frame.shape
        self.shape = (height, width)
        self.load_parking_spots()
        self.reference_frame_blurred = cv2.medianBlur(self.reference_frame, 7)
        
    def load_parking_spots(self):
        index = 1
        with open(self.file, 'r') as file:
            point_number = 1
            points = []
            for line in file:
                x, y = map(float, line.strip().split(','))
                points.append((x, y))
                if(point_number == 4):
                    spot = Spot(index, points, self.shape)
                    self.parking_spots.append(spot)
                    index += 1
                    points = []
                    point_number = 1
                else:
                    point_number += 1
    
    def compare_colored_frames(self, frame):
        current_frame_blurred = cv2.medianBlur(frame, 5)  # Kernel 5x5
        diff_r = cv2.absdiff(current_frame_blurred[:, :, 2], self.reference_frame_blurred[:, :, 2])  # Canal vermelho
        diff_g = cv2.absdiff(current_frame_blurred[:, :, 1], self.reference_frame_blurred[:, :, 1])  # Canal verde
        diff_b = cv2.absdiff(current_frame_blurred[:, :, 0], self.reference_frame_blurred[:, :, 0])  # Canal azul
        diff_gray = (diff_r.astype(np.float32) + diff_g.astype(np.float32) + diff_b.astype(np.float32)) /3
        diff_max = np.maximum(np.maximum(diff_r, diff_g), diff_b)

        diff_gray = diff_max#np.uint8(diff_gray)
        binary_frame = cv2.threshold(diff_gray, 12, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(binary_frame, cv2.MORPH_OPEN, kernel)
        
        return opening

    

