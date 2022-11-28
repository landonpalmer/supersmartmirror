class Outfit:
    def __init__(self):
        self.count = 0
        self.top = None
        self.bottom = None
        self.colors = []
        self.isColdOriented = False
        self.isWarmOriented = False
    def setColors(self, colorList):
        self.colors = colorList
    def setOutfit(self, itemList):
        tops = ["short sleeve top", "long sleeve top", "short sleeve outwear", "long sleeve outwear", "vest", "sling"]
        bottoms = ["shorts", "trousers", "skirt"]
        warm = ["short sleeve top","short sleeve outwear","sling","shorts", "skirt", "short sleeve dress", "vest dress", "sling dress"]
        cold = ["trousers", "long sleeve dress", "vest",  "long sleeve top", "long sleeve outwear"]
        WarmCount = 0
        ColdCount = 0
        for clothing in itemList:
            if clothing in warm:
                WarmCount+=1
            elif clothing in cold:
                ColdCount+=1
            self.count+=1
        if WarmCount >= ColdCount:
            self.isWarmOriented = True
        if ColdCount >= WarmCount:
            self.isColdOriented = True
        if ColdCount == WarmCount:
            self.isColdOriented = True
            self.isWarmOriented = True
        if self.count == 1:
            if itemList[0] in bottoms:
                self.bottom = itemList[0]
            elif itemList[0] in tops:
                self.top = itemList[0]
            else:
                self.top = itemList[0]
                self.bottom = itemList[0]
        else:
            for clothing in itemList:
                if clothing in tops:
                    self.top = clothing
                elif clothing in bottoms:
                    self.bottom = clothing
        

class Person: 
    def __init__(self, name, favoriteColors):
        self.Outfits = [Outfit]
        self.Name = name
        self.favoriteColors = favoriteColors
    def setOutfit(self, newOutfit):
        self.Outfits.append(newOutfit)
    def setNewColors(self, newColors):
        self.favoriteColors = newColors
    
