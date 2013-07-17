# 98% of the code here was written from scratch. 2% of it was from the 15-112
# website (namely the keypress/keyrelease events)

from Tkinter import *

class Animation(object):
    def mousePressed(self, event): pass
    def timerFired(self): pass
    def keyEvent(self): pass
    def redrawAll(self, canvas): pass
    def init(self): pass
        
    def keyPressed(self, event):
        #self.canvas = event.widget.canvas
        ctrl  = ((event.state & 0x0004) != 0)
        shift = ((event.state & 0x0001) != 0)
        if (event.keysym not in self.pressedKeys):
            self.pressedKeys.append(event.keysym)
    
    def keyReleased(self, event):
        #self.canvas = event.widget.canvas
        ctrl  = ((event.state & 0x0004) != 0)
        shift = ((event.state & 0x0001) != 0)
        if (event.keysym in self.pressedKeys):
            self.pressedKeys.remove(event.keysym)
    
    def run(self, width=500, height=800):
        # create the root and the canvas
        root = Tk()
        root.resizable(width=FALSE, height=FALSE)
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.timerDelay = 15
        self.pressedKeys = []
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.keyEvent()
            self.redrawAll(self.canvas)
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        def keyReleasedWrapper(event):
            self.keyReleased(event)
            redrawAllWrapper()
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            self.canvas.after(self.timerDelay, timerFiredWrapper)
        self.init()
        root.bind("<Button-1>", lambda event: mousePressedWrapper(event))
        root.bind("<KeyPress>", lambda event: keyPressedWrapper(event))
        root.bind("<KeyRelease>", lambda event: keyReleasedWrapper(event))
        timerFiredWrapper()
        root.mainloop()