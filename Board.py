# This file contains the main Universe the platform Avalanche will be run on.
# It contains all the key movements and the events of the falling blocks.

# Collisions are from the perspective of item2
# ie.   isLeftCollision(item1, item2) means item1 collides item2 from the left.
#       isTopCollision(item1, item2) means item1 collides item2 from above


# I will say that some style rules have been broken here, unfortunately.
# Sorry!

from Animation import Animation
import time, random
from Objects import *
import pygame

class Universe(Animation):

####################################################################
# Initializing Variables
####################################################################

    def initUniverse(self):
        
        #debugging
        #self.fallenBlock = False
        
        self.initBaseVariables()
        self.initJumpEvents()
        self.initMoveEvents()
        self.initCollisionEvents()
        self.initCanvasDimensions()
        self.initFloor()
        self.initPlayerDimensions()
        self.initWater()
        
        # draw everything
        self.drawEverything(self.canvas)
        
        pygame.mixer.init()
        pygame.mixer.music.load("avalancheMusic.wav")
        pygame.mixer.music.play()
        
    
    def initBaseVariables(self):
        # key variables
        self.timerDelay = 15
        self.score = 0
        self.offset = 0
        self.timerCount = 0
        self.twoPlayer = False
        self.gravity = 4
        self.waterDelay = 5
        self.objects = []
        self.isGameOver = False
        self.drewDeath = False
        self.playedGameOverSound = False
        #self.collisionList = []
        self.pressedLetters = [] #set up key pressed features
    
    def initJumpEvents(self):
        # jumping events
        self.isJumping = False
        self.isJumpLegal = True
        self.skipNextJump = False
        self.initialJumpVel = 40
        self.jumpVel = self.initialJumpVel
    
    def initMoveEvents(self):
        # moving conditions
        self.isLeftLegal = True
        self.isRightLegal = True
        self.isLeft = False
        self.isRight = False
    
    def initCollisionEvents(self):
        # collision conditions
        self.isLeftCollision = False
        self.isRightCollision = False
        self.isTopCollision = False
        self.isBottomCollision = False
    
    def initCanvasDimensions(self):
        # center of the board
        self.canvasCenterx = self.width/2.0
        self.canvasCentery = self.height/2.0
    
    def initFloor(self):
        self.floorLeft = -self.width
        self.floorTop = self.canvasCentery
        self.floorRight = 2*self.width
        self.floorBottom = self.height
        self.floorCenter = (self.floorRight + self.floorLeft)/2.0
    
    def initPlayerDimensions(self):
        # player dimensions
        self.playerWidth = Player(0,0).playerWidth
        self.playerHeight = Player(0,0).playerHeight
        
        # starting location
        self.playercx = self.floorCenter #- self.playerWidth#/2.0
        self.playercy = self.floorTop - self.playerHeight/2.0
        
        # players!
        self.player1 = Player(self.playercx, self.playercy)
        self.player1.fill = Color(255,255,255)
        self.player2 = Player(self.playercx, self.playercy)
        self.player2.fill = Color(0,0,0)

    def drawEverything(self, canvas):
        self.drawFloor()
        self.addObject(self.player1)
        self.displayScore()
        if self.twoPlayer == True:
            self.addObject(self.player2)

    def drawFloor(self):
        self.floor = Rectangle(self.floorLeft, self.floorTop,
                                self.floorRight, self.floorBottom)
        self.floor.fill = Color(0, 0, 0)
        self.floor.isFalling = False  #Floors are sturdy!
        return self.addObject(self.floor)
    
    def initWater(self):
        self.water = Water(-self.width, self.height-10,
                           2*self.width, self.height)
        self.water.fill = Color(0, 175, 255)
        self.water.line = Color(0, 175, 255)
        self.water.isFalling = False #Water does not fall!
        return self.addObject(self.water)
    
####################################################################
# Main events
####################################################################
    
    def placeNewBlock(self):
        # big and small blocks
        sizeList = [45, 70]
        height = self.getHighestBlock()
        #print height
        
        # dimensions and size
        cx = random.randint(0, self.width)
        cy = min(-self.height/2, self.floor.top - height -
                 random.randint(0, self.height/2))  #want to be off-screen!
        randomIndex = random.randint(0, 1)
        size = sizeList[randomIndex]
        block = Block(cx, cy, size)
        color = Color.randomColor()
        block.fill = color
        block.line = color
        
        #now we add it to the board!
        self.addObject(block)
    
    def getHighestBlock(self):
        highestLevel = -1
        for item in self.objects:
            if isinstance(item, Block):
                height = self.floor.top - item.bottom
                if height > highestLevel:
                    highestLevel = height
        return highestLevel
    
    def getScore(self):
        score = self.floor.top - self.player1.bottom
        if score > self.score:
            self.score = score
        return self.score
            
    def displayScore(self):
        score = Score(self.width/2.0, 20, "%d" % (self.score))
        score.anchor = "n"
        score.font = "Helvetica 22"
        self.addObject(score)
    
    def movex(self, shift):
        # basic movement
        self.oldLeft = self.player1.left
        self.oldRight = self.player1.right
        self.player1.left += shift
        self.player1.right += shift
        
        # deal with wrap-around
        if self.player1.right > self.width:
            self.player1.left = 0
            self.player1.right = self.player1.playerWidth
            # If we collide, we undo the move!
            self.wrapAroundFix()
        elif self.player1.left < 0:
            self.player1.left = self.width - self.player1.playerWidth
            self.player1.right = self.width
            # If we collide, we undo the move!
            self.wrapAroundFix()


    def wrapAroundFix(self):
        for block in self.objects:
            if isinstance(block, Block) or block == self.floor:
                if (self.isCollision(self.player1, block)
                    and self.player1.bottom != block.top):
                    #print "hi"
                    self.player1.left = self.oldLeft
                    self.player1.right = self.oldRight
    
    def moveLeft(self):
        if self.isLeftLegal:
            self.movex(-10)
        
    def moveRight(self):
        if self.isRightLegal:
            self.movex(10)
        
    def moveUp(self, shift):
        for item in self.objects:
            if (not isinstance(item, Text)):
                item.bottom += shift
                item.top += shift
    
    def jump(self, shift):
        #print self.timerCount
        for item in self.objects:
            if (not isinstance(item, Player)
                and not isinstance(item, Text)):
                item.bottom += shift
                item.top += shift

    def land(self):
        self.isJumping = False
        self.isJumpLegal = True
        self.jumpVel = 0
        
    def timerFired(self):
        if (self.isSmashed(self.player1)
            or self.player1.bottom >= self.water.top
            or self.floor.top <= 0):
            self.isGameOver = True
            return
        
        self.timerCount += 1
        initialPlayerLocation = self.player1.bottom
        self.isLeftLegal = True
        self.isRightLegal = True
        
        # place a new block after some time
        self.placeNewBlockEvent()
        
        # T/D move events
        if self.skipNextJump == True:
            if self.timerCount % 20 == 0:
                self.skipNextJump = False
                
        self.jumpEvent(self.player1)
            
        # L/R move events
        self.makeMoveLegal(self.player1)
            
        # move left
        if self.isLeft:
            self.moveLeft()
            
        # move right
        if self.isRight:
            self.moveRight()
            
        self.blockTimerCollisionEvent()
        self.waterRise()
        
        # if a bug occurs...
        if self.player1.bottom != self.height/2:
            self.player1.bototm = self.height/2
    
    def placeNewBlockEvent(self):
        # places new block.
        if self.timerCount <= 1000:
            self.delay = random.randint(58,70)
        elif self.timerCount <= 2000:
            self.delay = random.randint(53,70)
        else:
            self.delay = random.randint(50,70)
        if self.timerCount % self.delay == 0:
            self.placeNewBlock()
        
            # for debugging
            #if self.fallenBlock == False:
            #    self.placeNewBlock()
            #    if self.timerCount > 100:
            #        self.fallenBlock = True
    
    def jumpEvent(self, player):
        # timer event when player is jumping
        if (self.isFlying(player)
               or (self.isJumping and not self.skipNextJump)):
            self.isJumpLegal = False
            self.jump(self.jumpVel)
            if (self.isCollision(player, self.floor)):
                self.land()
            elif self.blockLandCollision(player):
                pass
            elif self.wallJumpCondition(player):
                if "Left" in self.pressedKeys:
                    self.movex(10)
                elif "Right" in self.pressedKeys:
                    self.movex(-10)
                self.isJumpLegal = True
                self.jumpVel = -self.gravity
            self.jumpVel -= self.gravity
    
    def blockTimerCollisionEvent(self):
        # block event for timerFired (also stacks blocks)
        for block in self.objects:
            if isinstance(block, Block):
                block.top += self.gravity
                block.bottom += self.gravity
                if (self.blockLandCollision(block) 
                      or self.floorCollision(block)):
                    block.isFalling = False
                    
    def waterRise(self):
        if self.timerCount % self.waterDelay == 0:
            if self.timerCount <= 1000:
                self.water.top -= 3
            elif self.timerCount <= 2000:
                self.water.top -= 4
            else:
                self.water.top -= random.randint(4,5)
        
    def isFlying(self, player):
        #checks if a player is not landed.
        result = True
        if self.floorCollision(player) == True:
            return False
        if all(player.bottom != item.top for item in self.objects):
            return result
        for item in self.objects:
            if isinstance(item, Text): continue
            if (player.bottom == item.top
                   and player.right >= item.left
                   and player.left <= item.right):
                result = False
        return result

##################################################################
# The following functions are to fix a bug for L/R movement
##################################################################

    def pixelOffsetCollision(self, item1, item2):
        return (self.isHorizontalPixelCollision(item1, item2)
                and self.isVerticalCollision(item1, item2))
    
    def isHorizontalPixelCollision(self, item1, item2):
        return ((item2.left <= item1.left-1 <= item2.right)
             or (item2.left <= item1.right+1 <= item2.right)
             or (item1.left <= item2.left-1 <= item1.right))

##################################################################
# End hacky functions
##################################################################
    
    def makeMoveLegal(self, player):
        for block in self.objects:
            if isinstance(block, Block):
                if ((self.isCollision(player, block)
                     or self.pixelOffsetCollision(player, block))
                    and player.top != block.bottom
                    and player.bottom != block.top):
                    
                    if block.left < player.left-10 < block.right:
                        
                        # We bumped into a block via the left
                        self.isLeftCollision = True
                        self.isLeftLegal = False
                        player.left = block.right+1
                        player.right = block.right+1 + player.playerWidth
                        
                    elif block.left < player.right+10 < block.right:
                        
                        # We bumped into a block via the right
                        self.isRightCollision = True
                        self.isRightLegal = False
                        player.right = block.left-1
                        player.left = block.left-1 - player.playerWidth
                else:
                    self.isLeftCollision = False
                    self.isRightCollision = False
    
    def isPlayerVerticalCollision(self, player):
        # for vertical events only.
        for item in self.objects:
            if (isinstance(item, Block)
                   or item == self.floor):
                if self.isCollision(player, item):
                    return True
        return False
    
    def isPlayerHorizontalCollision(self, player):
        # for horizontal events only (abusing our hack)
        for item in self.objects:
            if isinstance(item, Block):
                if self.pixelOffsetCollision(player, item):
                    return True
        return False
    
    def blockLandCollision(self, item):
        if item == self.floor: pass
        initialPlayerLocation = self.player1.bottom
        for block in self.objects:
            if item == block: continue
            if (isinstance(block, Block)
                    and self.isCollision(item, block)):
                if (isinstance(item, Player)
                    and not self.isLeftCollision
                    and not self.isRightCollision):
                    player = item
                    
                    #top collision
                    if player.bottom + self.jumpVel -1 < block.top:
                        
                        self.isTopCollision = True
                        #print "top"
                        player.bottom = block.top
                        player.top = block.top - player.height
                        self.land()
                        
                    #bottom collision
                    elif (block.top < player.top < block.bottom
                          and player.top + self.jumpVel*2 > block.bottom):
                        
                        self.isBottomCollision = True
                        #print "bottom"
                        player.top = block.bottom
                        player.bottom = block.bottom + player.height
                        self.jumpVel = 0
                    
                    else:
                        self.isBottomCollision = False
                        self.isTopCollision = False
                        
                    #top/bottom affects offset, so we repair it:
                    offset = initialPlayerLocation - player.bottom
                    self.moveUp(offset)
                    
                else: # these are just blocks, so stack them on each other
                    item.bottom = block.top
                    item.top = block.top - item.height
                return True
        return False

    def wallJumpCondition(self, player):
        result = False
        for block in self.objects:
            if (isinstance(block, Block)
                and self.pixelOffsetCollision(player, block)):
                #and player.top + 5 > block.bottom
                #and player.bottom - 5 < block.top):
                result = True
        return result
    
    def isSmashed(self, player):
        for block1 in self.objects:
            if ((isinstance(block1, Block)
                 or block1 == self.floor)
                 and self.isCollision(player, block1)):
                for block2 in self.objects:
                    if ((isinstance(block2, Block)
                         or block2 == self.floor)
                         and self.isCollision(player, block2)):
                        #if they're the same item, just skip it!
                        if block1 == block2: continue
                        elif (block1.isFalling == True
                             and block2.isFalling == False
                             and block1.bottom-self.gravity < player.top):
                            # We don't want to confuse side-bottom collisions
                            # with smash ones!
                            return True
                        
                        #elif ((block1.top == self.player1.bottom
                        #      and block2.bottom == self.player1.top)
                        #    or (block1.bottom == self.player1.top
                        #      and block2.top == self.player1.bottom)):
                        #    # Oh no! We got smashed by a block!
                        #        return True
        return False
    
    def isHorizontalCollision(self, item1, item2):
        return ((item2.left <= item1.left <= item2.right)
             or (item2.left <= item1.right <= item2.right)
             or (item1.left <= item2.left <= item1.right))
    
    def isVerticalCollision(self, item1, item2):
        return ((item1.top <= item2.top <= item1.bottom)
             or (item1.top <= item2.bottom <= item1.bottom)
             or (item2.top <= item1.top <= item2.bottom))
    
    def isContainsCollision(self, item1, item2):
        if (not self.isHorizontalCollision(item1, item2)
               and not self.isVerticalCollision(item1, item2)):
            if (item2.left <= item1.left <= item2.right
                   and item2.left <= item1.right <= item2.right
                   and item2.top <= item1.bottom <= item2.bottom
                   and item2.top <= item1.top <= item2.bottom):
                return True
        return False
    
    def isCollision(self, item1, item2):
        if ((self.isVerticalCollision(item1, item2)
            and self.isHorizontalCollision(item1, item2))):
            #or self.isContainsCollision(item1, item2)):
            return True
        return False
    
    def floorCollision(self, item):
        initialPlayerLocation = self.player1.bottom
        if self.isCollision(item, self.floor):
            item.bottom = self.floor.top
            item.top = self.floor.top - item.height
            if isinstance(item, Player):
            # fix the offset
                offset = initialPlayerLocation - item.bottom
                self.moveUp(offset)
            return True
        return False
        
    def keyEvent(self):
        if "r" in self.pressedKeys:
            self.initUniverse()
        if "Left" in self.pressedKeys:
            self.isLeft = True
        else: self.isLeft = False
        if "Right" in self.pressedKeys:
            self.isRight = True
        else: self.isRight = False
        if "Up" in self.pressedKeys:
            if self.isJumpLegal:
                self.jumpVel = self.initialJumpVel
                self.isJumping = True
                #print self.player1.bottom
    
    def addObject(self, objects):
        self.objects.append(objects)
        return objects
    
    def gameOverScreen(self, canvas):
        pygame.mixer.music.stop()
        width = self.width
        height = self.height
        canvas.create_text(width/2, height/4,
                           text="GAME OVER",
                           font="Helvetica, 60", justify="center",
                           fill = "orange red")
        canvas.create_text(width/2, 2*height/3,
                           text = "Your score: %d" % (self.score),
                           font = "Helvetica, 44",
                           justify = "center", fill = "orange red")
        canvas.create_text(width/2, 4*height/5,
                           text = "Press 'r' to restart!\n"+
                                  "Press 'q' to quit!",
                           font = "Helvetica, 36",
                           justify = "center", fill = "orange red")
        
    def redrawAll(self, canvas):
        self.getScore()
        for item in self.objects[::-1]:
            #print type(item)
            item.draw(self.canvas)
            if isinstance(item, Score):
                item.text = "Score: %d" % (self.score)
                
            ## for debugging
            #elif isinstance(item, Block):
            #    print self.timerCount
            #    print item.isFalling,
                
        if self.isGameOver:
            self.player1.fill = Color(255, 0, 0)
            #self.player1.line = Color(255, 0, 0)
            pygame.mixer.music.stop()
            if self.drewDeath == False: 
                self.drewDeath = True
                self.redrawAll(self.canvas)
            if self.playedGameOverSound == False:
                self.playedGameOverSound = True
                pygame.mixer.music.load("Death.wav")
                pygame.mixer.music.play()
                time.sleep(1.2)
            return self.gameOverScreen(self.canvas)
        
    def createText(self, left, top, text=None):
        return self.addObject(Text(left, top, text))
    
    def addPlayer(self, left, top):
        return self.addObject(Player(left, top))
    
if __name__ == '__main__':
    Universe().run()