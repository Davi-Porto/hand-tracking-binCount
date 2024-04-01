pointValues=[0,0,0,0,1,0,0,0,2,0,0,0,4,0,0,0,8,0,0,0,16,0,0,0,0,32,0,0,0,64,0,0,0,128,0,0,0,256,0,0,0,512]

class Mao:
    def __init__(self, rightHand=False):
        self.rightHand = rightHand
        self.hand = "Right" if self.rightHand == True else "Left" if self.rightHand == False else None
        self.noHand()
    
    def tot(self):
        if self.stts():
            aux = [8,12,16,20]
            self.upFingers = []
            if self.cords[4][0] > self.cords[4-2][0]:
                self.totHandBArr[4]=1
                self.upFingers.append(4)
            else:
                self.totHandBArr[4]=0
            
            for id, x in enumerate(aux):
                i = int(x-(5*(id+1)))
                if self.cords[x][1] <= self.cords[x-2][1]:
                    self.totHandBArr[i] = 1
                    self.upFingers.append(x)
                else:
                    self.totHandBArr[i] = 0
            self.totHandB = "".join(list(map(lambda n: str(n), self.totHandBArr)))
            self.upFingers = list(map(lambda n: n+21,self.upFingers)) if not self.rightHand else self.upFingers
            self.binTD()
            return self.totHandD, self.totHandB
        return None, None
    
    def binTD(self):
        self.totHandD = 0
        for finger in self.upFingers:
            self.totHandD += pointValues[finger]

    def noHand(self):
        self.cords = [[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]]
        self.ok = False
        self.totHandD = 0
        self.totHandBArr = [0,0,0,0,0]
        self.upFingers = []
        self.totHandB = "00000"
        self.binTD()
    
    def stts(self):
        self.ok = False if self.cords.count([0, 0])==21 else True
        return self.ok
    
    def dots(self, pontos):
        if len(pontos)==21:
            self.cords = pontos
        self.stts()