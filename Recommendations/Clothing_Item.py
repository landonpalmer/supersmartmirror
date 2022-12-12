class Clothing_Item:

    def __init__(self, name):
        self.name = name
        self.colors = []

    def addColor(self, color):
        self.colors.append(color)
    
    def addAllColors(self, colors):
        self.colors.extend(colors)
    
    def getColors(self):
        return self.colors

    def getName(self):
        return self.name