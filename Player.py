import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Player:
    def __init__(self):
        self.Position = [0, 2, 0]
        self.theta = 0
        self.Direction = [0, 0, 0]
        self.newDir = [0, 5, 1]
        self.jump_speed = 0.4
        self.gravity = 0.018
        self.on_ground = True
        self.y_velocity = 0
        self.prevPos = []
        self.preEyeY = 0
        self.pr = None
        self.freecam = True
        self.camPosDir = [self.Position, self.Direction] 
        self.especial = False
        
    def rotating(self):
        dir = [0.0, 0.0, 1.0]
        newx = dir[0] * math.cos(math.radians(self.theta)) + math.sin(math.radians(self.theta)) * dir[2]
        newz = dir[0] * math.sin(math.radians(self.theta)) + math.cos(math.radians(self.theta)) * dir[2]
        newdir = [newx, self.Position[1], newz]
        return newdir

    def update(self):
        self.prevPos = self.Position.copy()
        keys = pygame.key.get_pressed()
        if self.freecam:
            if keys[pygame.K_w]:
                self.newDir = self.rotating()
                self.Position[0] += self.newDir[0]
                self.Position[2] += self.newDir[2]
                
            if keys[pygame.K_s]:
                self.newDir = self.rotating()
                self.Position[0] -= self.newDir[0]
                self.Position[2] -= self.newDir[2]
                
            if keys[pygame.K_d]:
                self.theta -= 1*2
                self.newDir = self.rotating()
                
            if keys[pygame.K_a]:
                self.theta += 1*2
                self.newDir = self.rotating()
                
            if keys[pygame.K_SPACE]:
                self.Position[1] += 1
                self.newDir = self.rotating()
                
            if keys[pygame.K_LSHIFT]:
                if self.Position[1] > 2:
                    self.Position[1] -= 1
                    self.newDir = self.rotating()
            
            self.camPosDir = [self.Position.copy(), self.newDir.copy()]
            
        if keys[pygame.K_1]:
            self.freecam = True
            self.Position = self.camPosDir[0].copy()
            self.newDir = self.camPosDir[1].copy()
            self.especial = False
        if keys[pygame.K_2]:
            self.freecam = False
            self.Position = [2564, 200, 3714]
            self.newDir = [-0.56, 200, 0.83]
            self.especial = False


                    
                    
                    
