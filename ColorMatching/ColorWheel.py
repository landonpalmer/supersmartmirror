class ColorWheel:
    def __init__(self, wheel):
        self.wheel = wheel


    def isExistingColor(self, color):
        return color in self.wheel
    

    def getComplement(self, color):
        # Returns a string that is the complimentary color of the parameter
        if not self.isExistingColor(color):
            raise Exception("Cant find color", color, "in color wheel:", self.wheel)

        colorIndex = self.wheel.index(color)

        complimentIndex = int((colorIndex + (len(self.wheel) / 2)) % len(self.wheel))

        return self.wheel[complimentIndex]
    

    def isComplement(self, color1, color2):
        # Returns true if colors is the complimentary color of color1, false otherwise
        if not self.isExistingColor(color1) or not self.isExistingColor(color2):
            raise Exception("Cant find color(s)", color1, "or", color2, "in color wheel:", self.wheel)
        
        return color2 == self.getComplement(color1)
    

    def getAllAnalogous(self, color):
        # Returns array of tuples that are the set of all analagous colors that the parameter color are a part of
        if not self.isExistingColor(color):
            raise Exception("Cant find color", color, "in color wheel:", self.wheel)

        colorIndex = self.wheel.index(color)
        color1Index = (colorIndex + len(self.wheel) - 2) % len(self.wheel)
        color2Index = (colorIndex + len(self.wheel) - 1) % len(self.wheel)

        result = []

        result.append(sorted((color, self.wheel[color1Index], self.wheel[color2Index])))

        color1Index = (colorIndex + 1) % len(self.wheel)

        result.append(sorted((color, self.wheel[color1Index], self.wheel[color2Index])))

        color2Index = (colorIndex + 2) % len(self.wheel)

        result.append(sorted((color, self.wheel[color1Index], self.wheel[color2Index])))

        return result


    def isAnalogous(self, color1, color2, color3):
        # returns true if the three colors are analogous
        if not self.isExistingColor(color1) or not self.isExistingColor(color2) or not self.isExistingColor(color3):
            raise Exception("Cant find color(s)", color1, "or", color2, "in color wheel:", self.wheel)

        color1Index = self.wheel.index(color1)
        color2Index = self.wheel.index(color2)
        color3Index = self.wheel.index(color3)

        indexes = [color1Index, color2Index, color3Index]
        indexes.sort()

        return (indexes[0] + 1) == indexes[1] and (indexes[1] + 1) == indexes[2]
    

    def getAllSplitComplements(self, color):
        # Returns array of tuples where each tuple is a split compliment triple
        if not self.isExistingColor(color):
            raise Exception("Cant find color", color, "in color wheel:", self.wheel)

        result = []

        # Split color's compliment
        complementIndex = self.wheel.index(self.getComplement(color))

        color2 = ""

        if complementIndex - 1 < 0:
            color2 = self.wheel[len(self.wheel) - 1]
        else:
            color2 = self.wheel[complementIndex - 1]
        
        color3 = self.wheel[(complementIndex + 1) % len(self.wheel)]

        result.append(sorted((color, color2, color3)))

        # Split compliment with color index + 1
        complementIndex = (self.wheel.index(color) + 1) % len(self.wheel)

        color2 = self.getComplement(self.wheel[complementIndex])
        color3 = self.wheel[(complementIndex + 1) % len(self.wheel)]

        result.append(sorted((color, color2, color3)))

        # Split compliment with color index - 1
        complementIndex = self.wheel.index(color) - 1
        if (complementIndex < 0):
            complementIndex = len(self.wheel) - 1
        
        color2Index = complementIndex - 1
        if (color2Index < 0):
            color2Index = len(self.wheel) - 1
        
        color2 = self.wheel[color2Index]
        color3 = self.getComplement(self.wheel[complementIndex])

        result.append(sorted((color, color2, color3)))

        return result
    

    def isSplitCompliment(self, color1, color2, color3):
        if not self.isExistingColor(color1) or not self.isExistingColor(color2) or not self.isExistingColor(color3):
            raise Exception("Cant find color(s)", color1, "or", color2, "in color wheel:", self.wheel)

        actualColors = sorted((color1, color2, color3))

        # Find which two colors are only separated by 2 indexes
        for possibleCombo in self.getAllSplitComplements(color1):
            if actualColors == possibleCombo:
                return True
        
        return False

    def getTriadic(self, color):
        # Returns sorted tuple of triadic colors
        if not self.isExistingColor(color):
            raise Exception("Cant find color", color, "in color wheel:", self.wheel)
        
        incBy = int(len(self.wheel) / 3)

        colorIndex = self.wheel.index(color)
        color2Index = (colorIndex + incBy) % len(self.wheel)
        color3Index = (color2Index + incBy) % len(self.wheel)

        return sorted((color, self.wheel[color2Index], self.wheel[color3Index]))

    def isTriadic(self, color1, color2, color3):
        # Returns true if the colors are triadic
        triadic = self.getTriadic(color1)

        colors = sorted((color1, color2, color3))

        return triadic == colors


    def do2ColorsMatch(self, color1, color2):
        return self.isComplement(color1, color2)
    

    def do3ColorsMatch(self, color1, color2, color3):
        return self.isAnalogous(color1, color2, color3) or self.isSplitCompliment(color1, color2, color3) or self.isTriadic(color1, color2, color3)
    

    def secondColorSuggestion(self, color):
        # Returns array of tuples each showing a sugested color(s) 
        if not self.isExistingColor(color):
            raise Exception("Cant find color", color, "in color wheel:", self.wheel)
        
        result = []

        # complimentary color scheme:
        result.append((color, self.getComplement(color)))

        # Analagous color scheme:
        analgousTuples = self.getAllAnalogous(color)

        for colors in analgousTuples:
            result.append(colors)

        # Triadic color shceme:
        triadicColors = self.getTriadic(color)
            
        result.append(triadicColors)

        # Split complement color scheme:
        splitComplements = self.getAllSplitComplements(color)

        # remove color from tuple
        for colors in splitComplements:
            result.append(colors)
        
        return result


    def thirdColorSuggestion(self, color1, color2):
        if not self.isExistingColor(color1) or not self.isExistingColor(color2):
            raise Exception("Cant find color(s)", color1, "or", color2, "in color wheel:", self.wheel)
        
        suggestions = []

        # Check analogous possibles
        analogousColors = self.getAllAnalogous(color1)

        for colors in analogousColors:
            if color2 in colors:
                # make color tuple
                suggestions.append(colors)
        

        # Check split complementary possibilities
        splitColors = self.getAllSplitComplements(color1)

        for colors in splitColors:
            if color2 in colors:
                suggestions.append(colors)
        
        # Check triadic colors
        triadicColors = self.getTriadic(color1)

        if color2 in triadicColors:
            suggestions.append(triadicColors)
        
        return suggestions
        



        
    
    


