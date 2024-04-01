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
trocado = None
mapa=[rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,rH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH,lH]

font = cv2.FONT_HERSHEY_SIMPLEX
branco = (255, 255, 255)
azul = (255, 0, 0)
verde = (0, 255, 0)
vermelho = (0, 0, 255)
cinza = (51,51,51)
laranja = (0, 170, 255)


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
    global trocado
    if len(pontos)==42:
        pontos[:], trocado = (pontos[21:]+pontos[:21], True) if pontos[0][0]>pontos[21][0] else (pontos, False)
        lH.dots(pontos[:21])
        rH.dots(pontos[21:])
        msg("All hands find, check position")
        count()
        _,_,ok = handsStts(2)
        if ok:
            upFingers = lH.upFingers + rH.upFingers
            for finger in upFingers: # id: 4-41
                val = str(m.pointValues[finger])
                cx, cy = mapa[finger].cords[finger-21 if finger > 20 else finger]
                size, _ = cv2.getTextSize(val, font, 0.7, 1)
                cv2.putText(img, val, (int(cx-size[0]/2), cy-20), font, 0.7, verde, 1)
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
    response2 = list(map(lambda n: True if n=="Right position" else False,sttsH))
    response2.append(True if response2[0] and response2[1] else False)
    return response[op], response2[op], (response[op] and response2[op])

def colorDots(op):
    aux = list(map(lambda n: True if n=="Right position" else False, sttsH))
    toSend = [verde if aux[0] else vermelho, verde if aux[1] else vermelho]
    if op==0 or op==1:
        return toSend[op]
    else:
        return vermelho

def count():
    _,_, ok = handsStts(2)
    if ok:
        lHD, lHB = lH.tot()
        rHD, rHB = rH.tot()
        return (lHD, lHB), (rHD, rHB)

def handsPointsFunc(img, h, w):
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
            id = id if not trocado else 1 if id==0 else 0
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
    
    pontos=[] # Reset points before find new ones
    h, w, _ = img.shape # Set Width and Height of img from cam
    handsPointsFunc(img, h, w)
    
    _,_,ok = handsStts(2)
    
    # Hands find or not
    rect = cv2.rectangle(img, (0, h), (w, h-60), cinza, -1)
    cv2.putText(img, msg(), (20, h-20), font, 1, laranja, 1)
    
    # Total Top
    rect = cv2.rectangle(img, (0, 0), (w, 60), cinza, -1)
    
    cv2.putText(img, "0000000000" if not ok else lH.totHandB + rH.totHandB, (20, 40), font, 1, laranja, 1)
    
    text = "0" if not ok else str(lH.totHandD + rH.totHandD)
    (size, _), _ = cv2.getTextSize(text, font, 1, 1)
    cv2.putText(img, text, (int(w/2 - size/2), 40), font, 1, laranja, 1)
    
    # Line to orientation
    cv2.line(img, (int(w/2), 70), (int(w/2), h-70), branco, 1, cv2.LINE_4)
    
    # Show final img
    cv2.imshow("Imagem", img)
    
    # Simple delay to work well
    if cv2.waitKey(1) == 27: 
        break