##############################################################################
# Eric Gan
# Term Project for 15-112
# Fall 2012 Semester
# Finished 12/4/12
# Many thanks to Professor David Kosbie and my mentor Asa Frank for guiding
#       me along the way.
##############################################################################
# NOTE: This is the AUDIO version of this game!

# This is the main file. Run this to run the game!
# File contains splash screen, instructions, and credits. 

from Board import Universe
from Tkinter import *
import random, time

class Avalanche(Universe):
    
    def splash(self, canvas):
    #displays the splash screen when the window loads up
        width = self.width
        height = self.height
        canvas.create_image(width/2, height/12, anchor = N, image = self.logo)
        canvas.create_text(width/2, height/4,
                           text="Based on the Actual Game!",
                           font="Helvetica, 32",
                           justify="center")
        canvas.create_image(width/2, height/2, anchor = S, image = self.image)
        canvas.create_text(width/2, 4*height/7,
                           text = "By Eric Gan",
                           font = "Helvetica, 20")
        canvas.create_text(width/2, 2*height/3,
                           text="Press 'Enter' to start playing! \n"+
                                "Press 'h' for Instructions. \n"+
                                "Press 'c' for Credits\n"+
                                "Press 'q' to return here!",
                           font="Helvetica, 24",
                           justify="center")
        
    def instructions(self, canvas):
        width = self.width
        height = self.height
        self.timerDelay = 100
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        
        header = "Instructions"
        
        instructions = """
        Objective: You are a little white pillow/marshmellow/
        tissue and you want to climb as high as you can without
        getting smashed or drowned!
        
        Use the arrow keys to move your little white rectangle
        around! But oh no! Looks like there is water creeping
        up below you! Thankfully, it just started raining
        blocks... Phew! Now you can jump on top of the blocks
        and avoid the water! Also, take advantage of the fact
        that you can wall jump too! 
        
        The higher you climb, the higher your score! 
        
        During the game, press 'r' at any time to restart.
        There is no pause button, because otherwise that'd be
        cheating :P!
        """
        directors = """
        Press 'q' to go back to the Welcome Page
        Press 'Enter' to start the game!
        """
        
        for i in xrange(len(header)):
            canvas.create_text(40+ i*width/18, height/10,
                               text = header[i],
                               font = "Helvetica, 36",
                               fill = colors[random.randint(0,5)])

        canvas.create_text(5*width/11, height/3,
                           text= instructions,
                           font="Helvetica, 18",
                           justify = "center")
        
        canvas.create_image(width/2, 7*height/11,
                            image = self.instructionsPicture)
        
        canvas.create_text(5*width/11, 4*height/5,
                           text= directors,
                           font="Helvetica, 18",
                           justify = "center")
    
    def creditsScreen(self, canvas):
        width = self.width
        height = self.height
        self.timerDelay = 100
        colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        
        header = "Credits"
        
        kosbie = """
        I would first and foremost like to acknowledge my Carnegie
        Mellon University 15-112 professor David Kosbie for drilling
        me with all the programming fundamentals I needed to know to
        survive this class. He is an awesome and the best instructor
        I have ever had in my academic career. His ideology of "carpe
        diem" and "You won't get good until you dive right in and
        practice, practice, practice!" challenged me extensively,
        and I feel significantly more empowered in my programming
        ability than I was before taking 15-112.
        """
        
        asa = """
        I would also like to thank my CA mentor Asa Frank for being
        extremely supportive of my (lack of) effort from me in the
        first week and a half this term project was assigned. As
        Professor Kosbie said, "Asa is a man with nine brains," and
        I can testify that he in fact does!
        """
        
        rest = """
        I would finally like to thank all my friends who helped me
        debug my code, especially my roommate. All of you helped make
        this project possible (albeit still a little buggy)!
        """
        for i in xrange(len(header)):
            canvas.create_text(40+ i*width/18, height/10,
                               text = header[i],
                               font = "Helvetica, 36",
                               fill = colors[random.randint(0,5)])
        
        canvas.create_text(5*width/11, height/4,
                           text = kosbie,
                           font = "Helvetica, 14",
                           justify = "center")
        
        canvas.create_text(5*width/11, 3*height/7,
                           text = asa,
                           font = "Helvetica, 14",
                           justify = "center")
        
        canvas.create_text(5*width/11, 6*height/11,
                           text = rest,
                           font = "Helvetica, 14",
                           justify = "center")
        
        canvas.create_image(width/3, 4*height/5, image = self.kosbie)
        canvas.create_image(2*width/3, 4*height/5, image = self.asa)
    
    def init(self):
        self.isLaunched = False
        self.isInstructions = False
        self.isCredits = False
        self.gameOver = False
        self.logo = PhotoImage(file = "avalanche_logo.gif")
        self.image = PhotoImage(file = "avalanchePicture.gif")
        self.instructionsPicture = PhotoImage(file = "avalanche.gif")
        self.kosbie = PhotoImage(file = "kosbie.gif")
        asaImage = PhotoImage(file = "asa.gif")
        largeAsa = asaImage.zoom(3, 3)
        self.asa = largeAsa.subsample(4,4)
        self.timerDelay = 15
        
    def timerFired(self):
        if self.isLaunched == True:
            super(Avalanche, self).timerFired()
    
    def redrawAll(self, canvas):
        if self.isLaunched == False:
            if self.isInstructions == True:
                self.instructions(self.canvas)
            elif self.isCredits == True:
                self.creditsScreen(self.canvas)
            else:
                self.splash(self.canvas)
        elif self.gameOver == True:
            self.gameOverScreen
        else:
            super(Avalanche, self).redrawAll(self.canvas)
    
    def keyEvent(self):
        if self.isLaunched == False:
            if "Return" in self.pressedKeys:
                # launch the game!
                self.isLaunched = True
                self.initUniverse()
            elif "h" in self.pressedKeys:
                # Instructions
                self.isInstructions = True
            elif "c" in self.pressedKeys:
                # Credits page!
                self.isCredits = True
            elif "q" in self.pressedKeys:
                # Back to home page!
                self.init()
        else:
            super(Avalanche, self).keyEvent()
            if "q" in self.pressedKeys:
                # quit the game!
                self.init()
                self.splash(self.canvas)

if __name__ == '__main__':
    Avalanche().run()