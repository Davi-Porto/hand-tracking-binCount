# Bibliotecas

import cv2
import mediapipe as mp
import mao as m



# Inicializações

video = cv2.VideoCapture(1)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils
lH = m.Mao()
rH = m.Mao()


# Funções

def reconhecedor(pontos):
    if len(pontos)==42:
        primeira, segunda = ("direita", "esquerda") if pontos[0][0] > pontos[21][0] else ("esquerda", "direita")
        if pontos[4][0] > pontos[20][0] and pontos[25][0] > pontos[41][0]:
            direita = []
            esquerda = []
            if pontos[0][0] > pontos[21][0]:
                for i, vl in enumerate(pontos):
                    if i>=0 and i<=20:
                        direita.append(vl)
                    else:
                        esquerda.append(vl)
            else:
                for i, vl in enumerate(pontos):
                    if i>=0 and i<=20:
                        esquerda.append(vl)
                    else:
                        direita.append(vl)
            print("Posição correta")
        elif pontos[4][0] > pontos[20][0]:
            print(f"Mão {segunda} ao contrário")
        elif pontos[25][0] > pontos[41][0]:
            print(f"Mão {primeira} ao contrário")
    else:
        print("Coloque as duas mãos")


# Código principal

while 1:
    check, img = video.read()
    if not check:
        print("No cam")
        exit()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    handsPoints = Hand.process(imgRGB).multi_hand_landmarks
    h, w, _ = img.shape
    pontos = []
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x*w), int(cord.y*h)
                pontos.append((cx, cy))
        reconhecedor(pontos)
        
    cv2.imshow("Imagem", img)
    if cv2.waitKey(1) == 27:
        break