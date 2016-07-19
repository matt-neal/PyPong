# Pong Game Attempt, Rev. 3.0
# Matthew Neal
# CSCI 230 Final Project
# Due 12/9/14

from random import *
import random
import pygame as pg
import gameEngine as gE

#creates a ball SuperSprite
#space bar makes the ball move
#from the center position
class Ball(gE.SuperSprite):
    def __init__(self,carrier):
        gE.SuperSprite.__init__(self,carrier)
        self.setImage("ball.gif")
        self.setPosition((320,240))
        self.setBoundAction(self.BOUNCE)
        self.randAngle = random.randint(30,60)
        pg.mixer.init()
        self.sndYay = pg.mixer.Sound("yay.ogg")
        self.sndBoing = pg.mixer.Sound("bounce.wav")
        self.sndBounce = pg.mixer.Sound("boing.wav")
        self.sndFail = pg.mixer.Sound("fail.wav")
        self.sndDrop = pg.mixer.Sound("drop.wav")
                                
    def checkEvents(self):
        keys = pg.key.get_pressed()
        if self.speed == 0:
            if keys[pg.K_SPACE]:
                self.sndDrop.play()
                self.serve = -9
                self.setSpeed(self.serve)
                self.setAngle(self.randAngle)

    def reset(self):
        self.setPosition((320,240))
        self.setSpeed(0)
            
#creates a upper boundary line
class FieldUpper(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("horzBar.gif")
        self.setPosition((320,20))
                                
#creates a lower boundary line        
class FieldLower(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("horzBar.gif")
        self.setPosition((320,460))
        
#creates a line that allows the computer to score        
class FieldScoreP1(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("vertBar.gif")
        self.setPosition((10,240))
        
#creates a line that allows the player to score
class FieldScoreCPU(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("vertBar.gif")
        self.setPosition((630,240))
       
#creates a moveable bumper to protect the score zone        
class BumperP1(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("bumper.gif")
        self.setPosition((25,240))
            
    def checkEvents(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.moveBy((0,-7.5))
            if self.y <= 50:
                self.y = 50
        if keys[pg.K_DOWN]:
            self.moveBy((0,7.5))
            if self.y >= 430:
                self.y = 430

#creates a computer opponent bumper
#which moves per the balls y location
class BumperCPU(gE.SuperSprite):
    def __init__(self,scene):
        gE.SuperSprite.__init__(self, scene)
        self.setImage("bumper.gif")
        self.setPosition((615,240))
        self.setSpeed(0)
        self.moveBy((0,0))
        
    def checkEvents(self):
        self.ball = Ball(self)
        if self.y <= 50:
            self.y = 50
        if self.y >= 430:
            self.y = 430
       
#creates a game scene that calls
#all of the other classes and
#also creates the scores for each side
#sets groups from classes and defines
#sprites, as well as caption for game
#then defines collisions and computer AI.
class Game(gE.Scene):
    def __init__(self, carrier):
        gE.Scene.__init__(self)
        self.bumperP1 = BumperP1(self)
        self.bumperCPU = BumperCPU(self)
        self.fieldUpper = FieldUpper(self)
        self.fieldLower = FieldLower(self)
        self.fieldScoreP1 = FieldScoreP1(self)
        self.fieldScoreCPU = FieldScoreCPU(self)
        self.ball = Ball(self)
        self.carrier = carrier
        
        self.bounce = [self.fieldUpper, self.fieldLower]
        self.bounceGroup = self.makeSpriteGroup(self.bounce)
        self.addGroup(self.bounceGroup)

        self.pointsP1 = 0
        self.pointsP1 -= 1
        self.pointsCPU = 0
        self.pointsCPU -= 1
        self.lbl = gE.Label()
        self.lbl.center = (320, 60)
        self.lbl.text = ("{}       {}".format(self.pointsP1,self.pointsCPU))
        self.lbl.fgColor = (0,255,0)
        self.lbl.bgColor = (0,0,0)

        self.sprites = [self.fieldScoreCPU, self.fieldScoreP1, self.bounce,
                        self.bumperP1, self.bumperCPU, self.lbl, self.ball]
        self.setCaption("Pong")
                
    def update(self):
        #Defines boundary bouncing action
        ballHitBound = self.ball.collidesGroup(self.bounce)
        if ballHitBound:
            dy = self.ball.dy * -1
            self.ball.setDY(dy)
            if self.ball.speed != 0:
                self.ball.sndBounce.play()

        #defines player bumper bounces
        #and restricts speed
        ballHitBumperP1 = self.ball.collidesWith(self.bumperP1)
        if ballHitBumperP1:
            dy = self.ball.dy + ((self.ball.y - self.bumperP1.y) / 11)
            self.ball.setDY(dy)

            dx = self.ball.dx * -1
            self.ball.setDX(dx)
            if self.ball.speed != 0:
                self.ball.sndBoing.play()

        #defines computer bumper bounces
        #and restricts speed
        ballHitBumperCPU = self.ball.collidesWith(self.bumperCPU)
        if ballHitBumperCPU:
            dy = self.ball.dy + ((self.ball.y - self.bumperCPU.y) / 11)
            self.ball.setDY(dy)
            
            dx = self.ball.dx * -1
            self.ball.setDX(dx)
            if self.ball.speed != 0:
                self.ball.sndBoing.play()

        #defines score line for computer
        #resets ball upon score
        #randomizes ball launch
        ballHitScoreP1 = self.ball.collidesWith(self.fieldScoreP1)
        if ballHitScoreP1:
            if self.ball.speed != 0:
                self.ball.sndFail.play()
            self.ball.reset()
            self.pointsCPU += 1
            self.lbl.text = ("{}       {}".format(self.pointsP1,self.pointsCPU))
            self.ball.randAngle += random.choice((0,90))
            
        #defines score line for player
        #resets ball upon score
        #randomizes ball launch
        ballHitScoreCPU = self.ball.collidesWith(self.fieldScoreCPU)
        if ballHitScoreCPU:
            if self.ball.speed != 0:
                self.ball.sndYay.play()
            self.ball.reset()
            self.pointsP1 += 1
            self.lbl.text = ("{}       {}".format(self.pointsP1,self.pointsCPU))
            self.ball.randAngle += random.choice((180,270))
                        
        #computer "AI" functions
        if self.ball.x >= 320:
            if self.ball.y >= self.bumperCPU.y + 20:
                self.bumperCPU.moveBy((0,7.5))
            elif self.ball.y <= self.bumperCPU.y - 20:
                self.bumperCPU.moveBy((0,-7.5))
        
#introduction scene that lets the player
#know how to play and what to expect.
class Intro(gE.Scene):
    def __init__(self):
        gE.Scene.__init__(self)
        instructions = gE.MultiLabel()
        instructions.textLines = [
            "You are stuck in a",
            "NEVERENDING game of",
            "PONG. Use your up and",
            "down arrows to move",
            "your paddle and press",
            "the spacebar to launch",
            "the ball. Good luck..."]
        instructions.size = (400,300)
        instructions.fgColor = (0,255,0)
        instructions.bgColor = (0,0,0)
        instructions.center = (320,240)

        self.button = gE.Button()
        self.button.center = (320,420)
        self.button.text = ("BEGIN")

        self.sprites = [instructions, self.button]
        self.setCaption("Pong")

    def update(self):
        if self.button.clicked:
            self.stop()

class Report(gE.Scene):
    def __init__(self):
        gE.Scene.__init__(self)
        self.carrier = carrier

        lblFinal = gE.Label()
        lblFinal.center = (320,240)
        lblFinal.fgColor = (0,255,0)
        lblFinal.bgColor = (0,0,0)
        lblFinal.size = (300,200)
        lblFinal.text = ("{}       {}".format(self.pointsP1,self.pointsCPU))

        self.btnAgain = gE.Button()
        self.btnAgain.text = ("Play Again")
        self.btnAgain.center = (100,400)

        self.btnQuit = gE.Button()
        self.btnQuit.text = ("Quit")
        self.button.center = (540,400)

        self.sprites = [lblFinal, self.btnAgain, self.btnQuit]
    def update(self):
        if self.btnAgain.clicked:
            self.carrier.goAagain = True
            self.stop()
        if self.btnQuit.clicked:
            self.carrier.goAgain = False
            self.stop()

class Carrier(object):
    def __init__(self, status, goAgain):
        self.status = status
        self.goAgain = goAgain

#calls game class and begins app                        
def main():
    intro = Intro ()
    intro.start()

    carrier = Carrier("",True)

    while carrier.goAgain:
        game = Game(carrier)
        game.start()

        report = Report(carrier)
        report.start()
    
    #game = Game()
    #game.start()
    
if __name__ == "__main__":
    main()
