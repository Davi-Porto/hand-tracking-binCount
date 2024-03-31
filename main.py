# Libs

import cv2
import mediapipe as mp
import mao as m



# Initializing

video = cv2.VideoCapture(1)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils
lH = m.Mao()
rH = m.Mao(True)
msgTela = "Hands not found"
sttsH = ["Wrong position", "Wrong position"]

# Functions

def msg(msg=""):
    global msgTela
    if not msg=="":
        msgTela = msg
    return msgTela


def statusH(op=None, stts=None):
    global sttsH
    if op==0 or op==1:
        if stts==True or stts==False:
            sttsH[op] = "Wrong position" if stts==False else "Right position"
        else:
            return sttsH[op]
    elif op==2:
        sttsH = ["Wrong position", "Wrong position"] if stts==False else ["Right position", "Right position"]
    return sttsH

def reconhecedor(img):
    if len(pontos)==42:
        pontos[:] = pontos[21:]+pontos[:21] if pontos[0][0]>pontos[21][0] else pontos
        lH.dots(pontos[:21])
        rH.dots(pontos[21:])
        msg("All right")
    elif len(pontos)==21:
        aux = msg(("Right" if not pontos[0][0]>w/2 else "Left")+" hand not found").split(" ")[0]
        if aux=="Right":
            rH.noHand()
            lH.dots(pontos)
        else:
            lH.noHand()
            rH.dots(pontos)
    
    if handsStts(0):
        if lH.cords[4][0] > lH.cords[20][0]:
            statusH(0, True)
        else:
            statusH(0, False)
    
    if handsStts(1):
        if rH.cords[4][0] > rH.cords[20][0]:
            statusH(1, True)
        else:
            statusH(1, False)

def handsStts(op=2):
    response = (lH.stts(), rH.stts(), True if lH.stts() and rH.stts() else False)
    return response[op]

def colorDots(op):
    aux = list(map(lambda n: True if n=="Right position" else False, sttsH))
    toSend = [(0,255,0) if aux[0] else (0,0,255), (0,255,0) if aux[1] else (0,0,255)]
    return toSend[op]

def handsPointsFunc(h, w):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    handsPoints = Hand.process(imgRGB).multi_hand_landmarks
    if handsPoints:
        for points in handsPoints:
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x*w), int(cord.y*h)
                pontos.append((cx, cy))
        
        # Recognizing points
        reconhecedor(img)
        for id, points in enumerate(handsPoints):
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=colorDots(id)))
    else:
        msg("No hands find")
        lH.noHand()
        rH.noHand()

# Main Code

while 1:
    # Config cam and image
    
    check, img = video.read()
    if not check:
        print("No cam")
        exit()
    
    # Finding the hands
    pontos=[]
    h, w, _ = img.shape
    handsPointsFunc(h, w)
    
    
    # Hands find or not
    rect = cv2.rectangle(img, (0, h), (w, h-60), (51,51,51), -1)
    cv2.putText(img, msg(), (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 170, 255), 1)
    
    # Line to orientation
    cv2.line(img, (int(w/2), 70), (int(w/2), h-70), (255, 255, 255), 1, cv2.LINE_4)
    
    # Wrong or Right
    if handsStts(0):
        cv2.putText(img, f"{lH.totHandB}", (lH.cords[0][0], lH.cords[0][1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    if handsStts(1):
        cv2.putText(img, f"{lH.totHandB}", (rH.cords[0][0], rH.cords[0][1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Show final img
    cv2.imshow("Imagem", img)
    
    # Simple delay to work well
    if cv2.waitKey(1) == 27: 
        break