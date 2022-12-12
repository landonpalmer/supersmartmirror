from Color_Wheel import Color_Wheel

class Outfit:
    wheel = ["red", "red-orange", "orange", "yellow-orange", "yellow", "yellow-green", "green", "blue-green", "blue", "blue-violet", "violet", "red-violet"]
    neutralColors = ["black", "white", "gray", "beige"]
    cw = Color_Wheel(wheel)

    def __init__(self):
        self.clothingItems = []
        self.colors = []
        self.hadNeutral = False
    

    def addColor(self, color):
        if color in self.neutralColors:
            self.hadNeutral = True
        elif not (color in self.colors):
            self.colors.append(color)
    
    def addAllColors(self, colors):
        for color in colors:
            self.addColor(color)

    def addClothingItem(self, clothingItem):
        self.clothingItems.append(clothingItem)
        self.addAllColors(clothingItem.getColors())
    
    def addAllClothingItems(self, clothingItems):
        self.clothingItems.extend(clothingItems)

        for item in clothingItems:
            self.addAllColors(item.getColors())
    

    def getColors(self):
        return self.colors
    
    def getHadNeutral(self):
        return self.hadNeutral

    def getRecommendations(self):
        returnObj = {}

        if len(self.colors) <= 1 and self.hadNeutral:
            print("Colors Match!!")
            returnObj["colors_match"] = True
        elif (len(self.colors) == 2):
            if (self.cw.do2ColorsMatch(self.colors[0], self.colors[1])):
                print("Colors Match!!")
                returnObj["colors_match"] = True
            else:
                print("Colors don't match :(")
                print("Try theese color combinatios:")

                print("Color combination(s) for", self.colors)
                thirdColorSug = self.cw.thirdColorSuggestion(self.colors[0], self.colors[1])
                secondColorSug_1 = self.cw.secondColorSuggestion(self.colors[0])
                secondColorSug_2 = self.cw.secondColorSuggestion(self.colors[0])

                for colors in thirdColorSug:
                    print(colors)

                print("Color combination(s) for", self.colors[0])
                for colors in self.cw.secondColorSuggestion(self.colors[0]):
                    print(colors)
                
                print("Color combination(s) for", self.colors[1])
                for colors in self.cw.secondColorSuggestion(self.colors[1]):
                    print(colors)
                
                returnObj["colors_match"] = False
                
                returnObj["suggestions"] = []

                if len(thirdColorSug) > 0:
                    for colors in thirdColorSug:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
                if len(secondColorSug_1) > 0 and len(returnObj["suggestions"]) < 3:
                    for colors in secondColorSug_1:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
                if len(secondColorSug_2) > 0 and len(returnObj["suggestions"]) < 3:
                    for colors in secondColorSug_2:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
        elif (len(self.colors) == 3):
            if (self.cw.do3ColorsMatch(self.colors[0], self.colors[1], self.colors[2])):
                print("Colors Match!!")
                returnObj["colors_match"] = True
            else:
                print("Colors don't match :(")
                print("Try theese color combinatios:")

                thirdColorSug_1 = self.cw.thirdColorSuggestion(self.colors[0], self.colors[1])
                thirdColorSug_2 = self.cw.thirdColorSuggestion(self.colors[0], self.colors[2])
                thirdColorSug_3 = self.cw.thirdColorSuggestion(self.colors[1], self.colors[2])

                print("Color combination(s) for (" + self.colors[0] + ", " + self.colors[1] + ")")
                for colors in thirdColorSug_1:
                    print(colors)

                print("Color combination(s) for(" + self.colors[0] + ", " + self.colors[2] + ")")
                for colors in thirdColorSug_2:
                    print(colors)
                
                print("Color combination(s) for(" + self.colors[1] + ", " + self.colors[2] + ")")
                for colors in thirdColorSug_3:
                    print(colors)
                
                returnObj["colors_match"] = False

                returnObj["suggestions"] = []

                if len(thirdColorSug_1) > 0:
                    for colors in thirdColorSug_1:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
                if len(thirdColorSug_2) > 0 and len(returnObj["suggestions"]) < 3:
                    for colors in thirdColorSug_2:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
                if len(thirdColorSug_3) > 0 and len(returnObj["suggestions"]) < 3:
                    for colors in thirdColorSug_3:
                        if (len(returnObj["suggestions"]) > 2):
                            break
                        returnObj["suggestions"].append(colors)
        
        return returnObj



