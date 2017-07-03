__author__ = 'Charles'
import random
import pygame
import classes
import functions
pygame.init()

screenSize = (1300,800)
gameDisplay = pygame.display.set_mode(screenSize)   #use tuple (width,height)



white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,100)
objects = []
rectColor = green
state = 0
mouseButtons = [0,0,0]
moveButtons = [0,0,0,0] #w,a,s,d

pygame.display.set_caption("screen title")
clock = pygame.time.Clock()

global mX
global mY
mX = 0
mY = 0
gameExit = False



p1 = classes.player(400,400,screenSize)
w1 = classes.wall(400,700,200)
w2 = classes.wall(500,600,200, True)# true is hard wall, false is soft platform
w3 = classes.wall(500,600,50, True)
w3.height = 100
n1 = classes.node(700,700)
n2 = classes.node(720,750)
n3 = classes.node(740,750)
n4 = classes.node(760,750)
n5 = classes.node(780,750)
n6 = classes.node(800,700)



m1 = classes.map([p1, w1, w2, w3, n1, n2, n3,n4,n5,n6], screenSize)
#m1 = classes.map([p1, w1, w2], screenSize)


while not gameExit:
    gameDisplay.fill((50,50,50))#essentially wipes bg

    #get events, mouse movement, clicks, keyboard etc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            (mX,mY) = pygame.mouse.get_pos()
            print(mX,mY)

        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == pygame.K_q:
                print("q")
                pygame.quit()
                quit()
            if event.key == pygame.K_w:
                moveButtons[0] = 1
            if event.key == pygame.K_a:
                moveButtons[1] = 1
            if event.key == pygame.K_s:
                moveButtons[2] = 1
            if event.key == pygame.K_d:
                moveButtons[3] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moveButtons[0] = 0
            if event.key == pygame.K_a:
                moveButtons[1] = 0
            if event.key == pygame.K_s:
                moveButtons[2] = 0
            if event.key == pygame.K_d:
                moveButtons[3] = 0

    if moveButtons[0]:
        p1.jump()
    if moveButtons[1] & (not moveButtons[3]):
        p1.run(-1)
    if moveButtons[2]:
        p1.stop()
    if moveButtons[3] & (not moveButtons[1]):
        p1.run(1)


    #pygame.draw.circle(gameDisplay, rectColor, b1.getPos(), b1.size, width=0)
    if ((mX != 0) & (mY != 0)):
        pygame.draw.rect(gameDisplay, rectColor, [mX,mY,100,100])# where, color, [x,y,width height]

    m1.update()
    m1.disp(gameDisplay)

    pygame.display.update()
    clock.tick(60)#fps



pygame.quit()#closes window
quit()#quits python program