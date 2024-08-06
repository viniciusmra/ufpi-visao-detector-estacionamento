import numpy as np
import cv2

class Spot():
    def __init__(self, number, points, shape):
        self.number = number
        self.points = np.array([(int(x), int(y)) for x, y in points], dtype='float32')
        H_matrix = np.array([[0, 0], [200, 0], [200, 400], [0, 400]], dtype='float32')
        self.M = cv2.getPerspectiveTransform(self.points, H_matrix)
        self.M_inv = np.linalg.inv(self.M)
        self.occupied = False
        self.occupied_polygon = self.get_polygon(shape, True)
        self.empty_polygon = self.get_polygon(shape, False)


    def get_polygon(self, shape, occupied):
        planar_image = np.zeros((400, 200, 3), dtype='uint8')
        text = str(self.number)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 5
        font_thickness = 8
        text_color = (0, 0, 0)
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

        rect_w, rect_h = 200, 400
        text_x = (rect_w - text_width) // 2
        text_y = (rect_h + text_height) // 2

        if(occupied == False):
            color = (0, 80, 0)
        else:
            color = (0, 0, 80)
            
        cv2.rectangle(planar_image, (0, 0), (200, 400), color, -1)
        cv2.rectangle(planar_image, (0, 0), (200, 400), (255, 255, 255), 12)
        cv2.putText(planar_image, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        pespective_image = cv2.warpPerspective(planar_image, self.M_inv, (shape[1], shape[0]))

        return pespective_image
    
    def get_spot_diff(self, diff_mask):
        planar_image = cv2.warpPerspective(diff_mask, self.M, (200, 400))
        return planar_image
    def check_spot(self, spot_diff):
        mean = spot_diff.mean()
        if (mean > 80):
            self.occupied = True
        else:
            self.occupied = False
        

