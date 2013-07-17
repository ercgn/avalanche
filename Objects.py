# This file contains all the objects that the Universe in Board will use to
# run the game Avalanche.

from Animation import Animation
import random
from Tkinter import N,NW,W,SW,S,SE,E,NE,CENTER

class Color(object):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        
    @classmethod
    def randomColor(cls):
        red = random.randint(50, 230)
        blue = random.randint(50, 230)
        green = random.randint(50, 230)
        return Color(red, green, blue)
    
    def rgbString(self):
        return "#%02x%02x%02x" % (self.red, self.green, self.blue)

class Shape(object):
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
        self.height = bottom - top
        self.width = right - left
        
        self.cx = (self.right - self.left)/2.0
        self.cy = (self.bottom - self.top)/2.0
        
        # corners
        self.NW = (self.left, self.top)
        self.NE = (self.right, self.top)
        self.SW = (self.left, self.bottom)
        self.SE = (self.right, self.bottom)
        
        self.fill = None
        self.line = Color(0, 0, 0)
        self.lineWidth = 1
    
    def getFill(self):
        if self.fill == None:
            return None
        else:
            return self.fill.rgbString()
    
    def getLine(self):
        if self.line == None:
            return None
        else:
            return self.line.rgbString()

class Rectangle(Shape):
    def draw(self, canvas):
        canvas.create_polygon(self.left, self.top,
                              self.right, self.top,
                              self.right, self.bottom,
                              self.left, self.bottom,
                                fill=self.getFill(),
                                outline=self.getLine(), width=self.lineWidth)

class Player(Rectangle):
    def __init__(self, cx, cy):
        # player dimensions are 30x50
        self.playerWidth = 30
        self.playerHeight = 50
        
        # location
        self.playercx = cx
        self.playercy = cy
        
        # dimensions
        self.playerLeft = cx-self.playerWidth/2.0
        self.playerTop = cy-self.playerHeight/2.0
        self.playerRight = cx+self.playerWidth/2.0
        self.playerBottom = cy+self.playerHeight/2.0
        
        # call __init__ from Rectangle
        super(Player, self).__init__(self.playerLeft, self.playerTop,
                                     self.playerRight, self.playerBottom)
        
        # Misc.
        self.lineWidth = 1
        self.isWallJump = False

class Block(Rectangle):
    def __init__(self, cx, cy, r):
        self.isSturdy = False
        self.isFalling = True
        super(Block, self).__init__(cx-r, cy-r, cx+r, cy+r)
        self.lineWidth = 0

class Font(object):
    ##This class creates a font string for text-based objects.
    ##Default font is Helvetica 12
    
    def __init__(self):
        #initialize all variables
        self.size = 12
        self.italic = False
        self.underline = False
        self.bold = False
        self.face = "Helvetica"

    def __str__(self):
        #creates the str for the Font object
        fontString = str(self.face) + " " + str(self.size)
        if self.italic == True:
            fontString += " italic"
        if self.bold == True:
            fontString += " bold"
        if self.underline == True:
            fontString += " underline"
        return fontString

class Text(Shape):
    ##This class creates the text object on a canvas. It is also a "Shape"
    
    def __init__(self, left, top, text=None):
        #initializes all base variables
        self.left = left
        self.top = top
        self.fill = Color(0, 0, 0)
        self.text = text
        self.anchor = CENTER
        self.font = Font()

    def draw(self, canvas):
        #draws the actual text on the canvas
        canvas.create_text(self.left, self.top, text = self.text,
                           font=str(self.font), fill=self.getFill(),
                           anchor = self.anchor)

class Score(Text):
    # purpose of this class is to differentiate between normal text and
    # the score that appears on the top of the screen. Just inherits Text.
    pass

class Water(Rectangle):
    # purpose of this class is to differentiate between water and blocks and
    # floors
    pass