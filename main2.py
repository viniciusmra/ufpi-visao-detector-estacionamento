import cv2
import numpy as np
import copy

def draw_roi(frame, roi):
    center_x, center_y, w, h = roi[0]
    y = center_y - h//2
    x = center_x - w//2 
    is_empty = roi[4]

    if(is_empty == True):
        color = (0,255,0)
    else:
        color = (0,0,255)

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 8)

def analyze_roi(frame, roi):
    threshold = 20
    center_x, center_y, w, h = roi[0]
    y = center_y - h//2
    x = center_x - w//2 

    


    #current_roi = frame[top_left[1]:top_left[1]+square_size[0], top_left[0]:top_left[0]+square_size[1]] #atual
    
    current_roi = frame[y:y+h, x:x+w] #atual
    if(roi[1] is None):
        last_roi = current_roi
        reference_roi = current_roi
    else:
        last_roi = roi[1] #anterior
        reference_roi = roi[2] #referencia

    is_changing = roi[3]
    is_empty = roi[4]

    gray_curent_roi = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)
    gray_last_roi = cv2.cvtColor(last_roi, cv2.COLOR_BGR2GRAY)
    diff_image = cv2.absdiff(gray_curent_roi, gray_last_roi) # diferenca entre um imagem e outra
    
        
    diff_mean = np.mean(diff_image)
    #diff_image = cv2.cvtColor(diff_image, cv2.COLOR_GRAY2BGR)

    if(diff_mean < threshold):
        if is_changing:
            is_changing = False
            after_changing_diff = cv2.absdiff(current_roi, reference_roi)
            after_changing_diff_mean = np.mean(after_changing_diff)
            print(after_changing_diff_mean)
            if(after_changing_diff_mean > threshold):
                is_empty = False #not is_empty
            else:
                is_empty = True #is_empty
                #reference_roi = copy.deepcopy(current_roi)
        # else:
        #     #reference_roi = copy.deepcopy(current_roi)
    else:
        is_changing = True
    if(w == 52):
        diff_image = cv2.cvtColor(diff_image, cv2.COLOR_GRAY2BGR)
        result = cv2.vconcat([current_roi, diff_image, last_roi])
        result = cv2.resize(result,(200,600))
        cv2.imshow('result', result)
    return [roi[0], current_roi, reference_roi, is_changing, is_empty]


# Função principal
def main(video_file):
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print("Erro ao abrir o arquivo de vídeo.")
        return


    #roi_dimentions = [(420,820,50,50), (560,820,50,50), (1200,820,50,50), (1600,820,52,52), (170,980,50,50), (800,980,50,50), (950,980,50,50)]
    roi_dimentions = [(70,650,52,52)]
    rois = []
    for dimentions in roi_dimentions:
        center_x, center_y, w, h = dimentions
        new_roi = [dimentions, None, None, False, True]
        rois.append(new_roi)

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Fim do vídeo.")
            break

        # Defina o ponto superior esquerdo e o tamanho do quadrado verde
        
        #frame do objeto atual
        # current_roi = frame[top_left[1]:top_left[1]+square_size[0], top_left[0]:top_left[0]+square_size[1]] #atual
        # if(is_first_frame):
        #     reference_roi = copy.deepcopy(current_roi)
        #     last_roi = copy.deepcopy(current_roi)
        #     is_first_frame = False
        

        # gray_curent_roi = cv2.cvtColor(current_roi, cv2.COLOR_BGR2GRAY)
        # gray_last_roi = cv2.cvtColor(last_roi, cv2.COLOR_BGR2GRAY)
        # diff = cv2.absdiff(gray_curent_roi, gray_last_roi) # diferenca entre um imagem e outra
        
        # diff_mean = np.mean(diff)
        # diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
        
        # print(f'Média: {diff_mean}')


        # if(diff_mean < 15):
        #     print("Media < 10")
        #     if is_changing:
        #         print("is_changing era true")
        #         is_changing = False
        #         after_changing_diff = cv2.absdiff(current_roi, reference_roi)
        #         after_changing_diff_mean = np.mean(after_changing_diff)
        #         print(f'after_changing_diff_mean: {after_changing_diff_mean}')
        #         if(after_changing_diff_mean > 15):
        #             print("media menor que 30")
        #             is_empty = not is_empty
        #             print("Estado mudou")
        #             reference_roi = copy.deepcopy(current_roi)
        #             print("atualiza o reference_roi 1")
        #     else:
        #         reference_roi = copy.deepcopy(current_roi)
        #         print("atualiza o reference_roi 2")
        # else:
        #     is_changing = True
        #     print("is_changing ficou true")

        # print('\n\n')
        # resized_current_roi = cv2.resize(current_roi, (240, 240))
        # resized_diff = cv2.resize(diff, (240, 240))
        # resized_reference_roi = cv2.resize(reference_roi, (240, 240))

        


        # combined_roi = cv2.vconcat([resized_current_roi, resized_diff, resized_reference_roi])
        # last_roi = copy.deepcopy(current_roi)

        # # Desenhe o quadrado verde no frame atual
        # if is_empty:
        #     color = (0, 255, 0)
        # else:
        #     color = (0, 0, 255)

        # #draw_square(frame, top_left, square_size, color)
        # draw_roi(frame, roi_dimentions, [True, False])

        # # Exiba o frame com o quadrado
        # frame = cv2.resize(frame, (1280, 720))
        # combined_image = cv2.hconcat([frame, combined_roi])
        # cv2.putText(combined_image, f"{frame_count*0.033} s", (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness=2)
        new_rois =[]
        new_frame = copy.deepcopy(frame)
        for roi in rois:
            new_roi = analyze_roi(new_frame, roi)
            draw_roi(frame, new_roi)
            new_rois.append(new_roi)

        rois = new_rois
        

        frame = cv2.resize(frame, (1280, 720))
        cv2.putText(frame, f"{frame_count*0.033} s", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), thickness=4)
        cv2.imshow('Video', frame)

        frame_count += 1
        # Aguarda pela tecla e verifica se é a barra de espaço (para avançar frame por frame)
        key = cv2.waitKey(0) & 0xFF
        if key == 32:  # Barra de espaço
            continue
        elif key == 27:  # Tecla Esc para sair
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #video_file = 'video1.mp4'  
    video_file = 'video2.avi'
    main(video_file)
