tops = ["Short sleeve top", "Long sleeve top", "Short sleeve outwear", "Long sleeve outwear", "Vest", "Sling"]
bottoms = ["Shorts", "Trousers", "Skirt"]
neither = ["Short sleeve dress","Long sleeve dress", "Vest dress", "Sling dress"]
warm = ["Short sleeve top","Short sleeve outwear","Sling","Shorts", "Skirt", "Short sleeve dress", "Vest dress", "Sling dress"]
cold = ["Trousers", "Long sleeve dress", "Vest",  "Long sleeve top", "Long sleeve outwear"]
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
    def setOutfit(self, itemList, colorList):
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
        elif ColdCount >= WarmCount:
            self.isColdOriented = True
        if self.count == 1:
            self.top = itemList[0]
            self.bottom = itemList[0]
        else:
            for clothing in itemList:
                if clothing in tops:
                    self.top = clothing
                elif clothing in bottoms:
                    self.bototm = clothing
        

class Person: 
    def __init__(self, name, favoriteColors):
        self.Outfits = [Outfit]
        self.Name = name
        self.favoriteColors = favoriteColors
    def setOutfit(self, newOutfit):
        self.Outfits.insert(newOutfit)
    def setNewColors(self, newColors):
        self.favoriteColors = newColors
    
