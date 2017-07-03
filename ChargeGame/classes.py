import random
import pygame
import functions


__author__ = 'Charles'

class map:
    def __init__(self, stuff, screenSize):
        self.items = stuff
        self.screenSize = screenSize
        self.sun = [.5,1]
    def update(self):
        for each in self.items:
            each.update(self.items)

    def disp(self, surface):

        for each in self.items:
            if each.type in ["wall", "platform"]:
                sX = self.sun[0] * self.screenSize[0]
                sY = self.sun[1] * self.screenSize[1]


                points = [[each.x, each.y]]
                points.append([each.x + each.length, each.y])
                points.append([(each.x + each.length) + sX ,   each.y + sY ])
                points.append([each.x + sX,   each.y + sY  ])

                pygame.draw.polygon(surface, (255,0,0), points)

        for each in self.items:

            #objects
            if each.type == "player":
                pygame.draw.rect(surface, each.color, [each.x-(each.size[0]/2), each.y-(each.size[1]),each.size[0],each.size[1]])
            if each.type in ["wall", "platform"]:
                pygame.draw.rect(surface, each.color, [each.x, each.y, each.length, each.height])
            if each.type == "node":
                pygame.draw.circle(surface, each.color, [each.x, each.y], each.size)


class player:
    def __init__(self, spawnX, spawnY ,m):
        self.speedlimit = 20
        self.canJump = True
        self.charge = 10
        self.chargeRate = 0.01
        self.maxCharge = 25
        self.g = 1.01
        self.friction = 0.9
        self.jumpstrength = 15 # about 100 pix jump
        self.type = "player"
        self.speed = 5
        self.acc = 1
        self.size = (20,50)
        self.color = (max(-10*self.charge, 0),0,max(10*self.charge,0))
        self.spawnX = spawnX
        self.spawnY = spawnY
        self.x = spawnX
        self.y = spawnY
        self.lastX = spawnX
        self.lastY = spawnY

        (self.maxX, self.maxY) = m
        self.vx = 0
        self.vy = 0

    def update(self, stuff):
        self.charge += self.chargeRate
        if self.charge > self.maxCharge:
            self.charge = self.maxCharge
        self.color = (int(max(-10*self.charge, 0)),0,int(max(10*self.charge,0)))
        #print(self.charge)
        self.lastX = self.x
        self.lastY = self.y

        self.y += self.vy
        self.x += self.vx

        self.vy += self.g
        self.vx *= self.friction

        if self.y >= self.maxY:
            self.y = self.maxY
            self.vy = 0
            self.canJump=True
        #check interaction
        for each in stuff:
            if each.type == "platform":
                if (self.y > each.y) & (self.lastY < each.y) & (self.x+ self.size[0]/2 > each.x) & (self.x - self.size[0]/2 < each.x + each.length):
                    self.y = each.y -1
                    self.vy = 0
                    self.canJump=True
            if each.type == "wall":
                #top
                if (self.y > each.y) & (self.lastY < each.y) & (self.x+ self.size[0]/2 > each.x) & (self.x - self.size[0]/2 < each.x + each.length):
                    self.y = each.y -1
                    self.vy = 0
                    self.canJump=True
                #bottom
                if (self.y - self.size[1] < each.y + each.height) & (self.lastY - self.size[1] > each.y + each.height) & (self.x > each.x) & (self.x < each.x + each.length):
                    self.y = each.y + each.height + self.size[1] + 5
                    self.vy = 0.1
                    self.vy = 0.1
                    #print(each.y)
                #left
                if (self.lastX + self.size[0]/2 < each.x) & (self.x + self.size[0]/2 > each.x) & (each.y + each.height > self.y - self.size[1]) & (each.y < self.y):
                    self.x = each.x -self.size[0]/2
                    self.vx = - self.vx -1
                    print(self.x)
                #right
                if (self.lastX - self.size[0]/2 > each.x + each.length) & (self.x - self.size[0]/2 < each.x + each.length) & (each.y + each.height > self.y - self.size[1]) & (each.y < self.y):
                    self.x = each.x + each.length + self.size[0]/2
                    self.vx = -self.vx +1
                    print(self.x)
            if each.type == "node":
                [r,px,py] = functions.distance(self, each)
                if r < each.range:
                    self.charge *= 0.999
                    force = (10*self.charge * each.charge)/(r*r)
                else:
                    force = 0
                self.vx += force * px
                self.vy += force * py

        if abs(self.vx) > self.speedlimit:
            self.vx *= self.speedlimit / abs(self.vx)
            self.vy *= self.speedlimit / abs(self.vy)


    def jump(self):
        if self.canJump:
            self.canJump=False
            self. vy -= self.jumpstrength

    def run(self, direction):
        change  = self.acc*direction
        new = self.vx + change

        if (new <= self.speed )& (new >= -self.speed):
            self.vx = new
        elif (self.vx < 0) & (change > 0):
            self.vx = new
        elif (self.vx > 0) & (change < 0):
            self.vx = new

        if self.vx < -self.speed:
            self.vx = -self.speed
        if self.vx > self.speed:
            self.vx = self.speed

    def stop(self):
        self.vx = 0


class wall:
    def __init__(self,x,y,length, platform = False):
        self.color = (200,200,200)
        self.x = x
        self.y = y
        self.length = length
        self.height = 25
        if platform:
            self.type = "wall"
            self.color = (200,200,200)
        else:
            self.type = "platform"
            self.color = (100,100,100)

    def update(self, stuff):
        None

class node:
    def __init__(self, x,y, size = 3):
        self.size = size
        self.charge = 10
        self.color = (max(-10*self.charge,0),0,max(10*self.charge,0))
        self.x = x
        self.y = y
        self.type = "node"
        self.range = 100
    def update(self, stuff):
        None