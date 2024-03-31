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
rH = m.Mao(True)
msgTela = "Hands not found"
sttsH = ["Wrong position", "Wrong position"]

# Funções

def msg(msg=""):
    global msgTela
    if not msg=="":
        msgTela = msg
    return msgTela


def statusH(op=-1, stts=False):
    global sttsH
    if op==0 or op==1:
        sttsH[op] = "Wrong position" if stts==False else "Right position"
    elif op==2:
        sttsH = ["Wrong position", "Wrong position"]
    return sttsH

def reconhecedor(img):
    if len(pontos)==42:
        pontos[:] = pontos[21:]+pontos[:20] if pontos[0][0]>pontos[21][0] else pontos
        msg("All right")
        lH.dots(pontos[:20])
        rH.dots(pontos[21:])
        lHRightPos()
        rHRightPos()
    elif len(pontos)==21:
        aux = msg(("Right" if not pontos[0][0]>w/2 else "Left")+" hand not found").split(" ")[0]
        if aux=="Right": # Left
            lH.dots(pontos)
            lHRightPos()
        else: # Right
            rH.dots(pontos)
            rHRightPos()

def lHRightPos():
    statusH(0, lH.cords[4][0] > lH.cords[20][0])

def rHRightPos():
    statusH(1, rH.cords[4][0] > rH.cords[20][0])

def handsStts():
    lH.stts()
    rH.stts()
    return True if lH.ok == True and rH.ok == True else False

def handsPointsFunc(h, w):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    handsPoints = Hand.process(imgRGB).multi_hand_landmarks
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for cord in points.landmark:
                cx, cy = int(cord.x*w), int(cord.y*h)
                pontos.append((cx, cy))
        #Fazendo reconhecimento dos pontos
        reconhecedor(img)
    else:
        msg("No hands find")

# Código principal

while 1:
    
    # Configurações de camera e imagem
    
    check, img = video.read()
    if not check:
        print("No cam")
        exit()
    
    # Encontrando as mãos
    pontos=[]
    h, w, _ = img.shape
    handsPointsFunc(h, w)
    
    # Mostrando resultados na tela
    
    rect = cv2.rectangle(img, (0, h), (w, h-60), (51,51,51), -1)
    cv2.putText(img, msg(), (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 170, 255), 1)
    cv2.putText(img, statusH()[0], (10, h-70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    (textSize, _), _ = cv2.getTextSize(statusH()[1], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.putText(img, statusH()[1], (w - textSize - 10, h - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.line(img, (int(w/2), 70), (int(w/2), h-70), (255, 255, 255), 1, cv2.LINE_4)
    cv2.imshow("Imagem", img)
    if cv2.waitKey(1) == 27:
        break