dedos=[[[4,"Dedão direito",1],[8,"Indicador direito",2],[12,"Dedo do meio direito",4],[16,"Anelar direito",8],[20,"Mindinho direito",16],],[[25,"Dedão esquerdo",32],[29,"Indicador esquerdo",64],[33,"Dedo do meio esquerdo",128],[37,"Anelar esquerdo",256],[41,"Mindinho esquerdo",512],],]

class Mao:
    def __init__(self):
        self.noHand()
    
    def tot(self):
        if self.cords.count(None)==0:
            adcFH, dOE = 0, 0 if self.rightHand==True else 21, 1
            aux = [8,12,16,20]
            self.totHandD = 0
            if self.cords[4][0] > self.cords[4-1][0]:
                self.totHandD += 1 if self.rightHand==True else 32
                self.totHandBArr[0]=1
            else:
                self.totHandBArr[0]=0
            for x in aux:
                if self.cords[x][1] > self.cords[x-2][1]:
                    for dedo in dedos[dOE]:
                        self.totHandD += dedo[2] if dedo[0]==x+adcFH else 0
                    self.totHandBArr[x/4-1]=1
                else:
                    self.totHandBArr[x/4-1]=0
            self.dTBin()
            return self.totHandD, self.totHandB
        return None, None
    
    def noHand(self):
        self.cords = [[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None],[None, None]]
        self.rightHand = None
        self.totHandD = 0
        self.totHandBArr = [0,0,0,0,0]
        self.dTBin()
    
    
    def dTBin(self):
        if len(self.totHandBArr)>5:
            print(f"[ERRO] Mais que 5 números na array binária -> ({len(self.totHandBArr)})")
            while len(self.totHandBArr)>5:
                self.totHandBArr.pop()
            print("Utilizando apenas os 5 primeiros números em binário")
        self.totHandB = "".join(map(lambda n : str(n) if n==0 or n==1 else "0" if n <= 0 else "1", self.totHandBArr))
    
    def stts(self):
        self.ok = True if self.cords.count(None)==0 else False
        
    def dots(self, pontos):
        if len(pontos)==20:
            self.cords = pontos
        self.stts()