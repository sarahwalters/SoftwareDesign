# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:54:55 2014

@author: Sarah Walters and Jenny Vaccaro
"""

#Final game

import pygame
from pygame.locals import *
import random
import time

class ArrowModel:
    '''
        This class encodes the game state.
        Attributes: boxes on screen, size of screen, box side length, lives, score, arrow key options, speed updater
    '''
    def __init__(self, size):
        self.boxes = []
        (self.sx, self.sy) = size
        self.side = (self.sx-10)/10 #box is 1/10 width of screen, leaving 5px border on each side
        self.lives = 5
        self.score = 0
        self.arrowlist = ['K_UP','K_DOWN','K_LEFT','K_RIGHT']
        self.speedFactor = 0
            
    def makeBox(self):
        ''' helper method which creates a box with random color, column location, and arrow '''
        color = (0, random.randint(50,150), random.randint(50,150)) # green/blue
        box = Box(color, 
                  (self.side/2+5)+random.randint(1,8)*self.side, # places box horizontally
                  -self.side/2, # starts just off the screen vertically
                  self.side, 
                  1 + self.speedFactor, # boxes start faster over course of game
                  self.arrowlist[random.randint(0,3)]) # randomizes arrow orientation
        self.boxes.append(box)
         
    def update(self):
        ''' Updates the game state, adding and subtracting boxes and changing their colors/functionalities '''   
        for box in self.boxes:
            box.centery += box.vy
            box.vy += box.ay
            
            # start of target range
            if box.centery > self.sy - 5*self.side/2 and box.hitLine == False:
                box.color = (0,box.color[1]+100,box.color[2]+100)
                box.hitLine = True
                
            # end of target range
            if box.centery > self.sy - 2*self.side + 5 and box.hitLine2 == False:
                box.color = (200, 20, 50)
                self.lives -= 1
                box.hitLine2 = True
                
            # hits bottom of screen - take box out of list to keep self.boxes to only boxes which are on screen
            if box.centery > self.sy + self.side/2:
                self.boxes.remove(box)
                
        # randomizes when a new box appears
        chance = random.randint(0,500)
        if chance < 3:
            self.speedFactor += .05
            self.makeBox()
        
class Box:
    '''
        This defines a box.
        Attributes: color, center position, side length, fall speed, acceleration, arrow, line location.
    '''
    def __init__(self, color, centerx, centery, side, vy, arrow):
        self.color = color
        self.centerx = centerx #center x coordinate
        self.centery = centery #center y coordinate
        self.side = side #side length, assuming square
        self.vy = vy
        self.ay = .005
        self.arrow = arrow
        self.hitLine = False
        self.hitLine2 = False

class ArrowViewPyGame:
    '''
        This class renders a display of the game in PyGame.
    '''
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
        self.arrowImageDict = {'K_UP':'arrowU.png','K_DOWN':'arrowD.png','K_LEFT':'arrowL.png','K_RIGHT':'arrowR.png'}
        
    def draw(self):
        ''' Renders current state of model '''
        self.screen.fill(pygame.Color(0,0,0)) # fill with black to clear previous frame   
        for b in self.model.boxes:
            # draw colored box
            cx = b.centerx - b.side/2
            cy = b.centery - b.side/2
            box_rect = pygame.Rect(cx, cy, b.side, b.side)
            pygame.draw.rect(self.screen,
                             pygame.Color(b.color[0], b.color[1], b.color[2]),
                             box_rect)
                             
            # draw arrow onto colored box
            arrowImage = pygame.image.load(self.arrowImageDict[b.arrow])
            arrowImage = pygame.transform.scale(arrowImage, (int(b.side),int(b.side)))
            self.screen.blit(arrowImage, box_rect)
        
        # display score and lives remaining
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.model.score) + "   Lives: " + str(self.model.lives), 1, pygame.Color(255,255,255))
        textrect = text.get_rect()
        textrect.centerx = self.model.sx/2
        textrect.centery = self.model.sy-50
        self.screen.blit(text, textrect)
        
        # draw lines which define target range
        pygame.draw.rect(self.screen, pygame.Color(255,255,255), pygame.Rect(self.model.side/2,self.model.sy-3*self.model.side, self.model.sx-self.model.side, 5))
        pygame.draw.rect(self.screen, pygame.Color(255,255,255), pygame.Rect(self.model.side/2,self.model.sy-1.5*self.model.side, self.model.sx-self.model.side, 5))
        
        pygame.display.update()
    
    
class ArrowControllerPyGame:
    '''
        This class allows for control of the PyGame rendering using a keyboard.
    '''
    def __init__(self,model):
        self.model = model
        self.arrowEventDict = {'K_UP':pygame.K_UP, 'K_DOWN':pygame.K_DOWN, 'K_LEFT':pygame.K_LEFT, 'K_RIGHT':pygame.K_RIGHT}
        
    def handle_arrow_event(self, event):
        ''' Responds to player arrow key input '''
        if event.type != KEYDOWN: # catchall for events which are not arrow presses
            return
        for box in self.model.boxes:
            # check whether box is in target range
            if box.centery > self.model.sy - 5*self.model.side/2 and box.centery < self.model.sy - 2*self.model.side:
                # check whether key pressed was correct key
                if event.key == self.arrowEventDict[box.arrow]:
                    # remove and update score
                    self.model.boxes.remove(box)
                    self.model.score += 1

    
if __name__ == '__main__':
    '''
        This is where the game runs. Creates screen, builds MVC, controls whether game is running.
    '''
    pygame.init()

    size = (1000,800) #make sure sx-10 is multiple of 20
    screen = pygame.display.set_mode(size)
    
    model = ArrowModel(size) 
    view = ArrowViewPyGame(model, screen)
    controller = ArrowControllerPyGame(model)

    running = True # on/off switch

    while running:
        if model.lives <= 0: # player has lost
            running = False
        for event in pygame.event.get():
            if event.type == QUIT: # player closed window
                running = False
            if event.type == KEYDOWN: # arrow key press
                controller.handle_arrow_event(event)
                
        model.update()
        view.draw()
        time.sleep(.001) #game speed limit

    pygame.quit() # closes open pygame window once game is over