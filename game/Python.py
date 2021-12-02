import time
import random
import pygame,sys
from pygame import mixer
from pygame import freetype
from pygame.locals import *
pygame.init()
pygame.freetype.init()
#initialization
WIN= pygame.display.set_mode((861,651))
pygame.display.set_caption("Python")
ICO=pygame.image.load('assets/python.png').convert()
FRAME=pygame.image.load('assets/frame.png').convert()
FONT=pygame.freetype.Font('assets/UpheavalPro.ttf')
pygame.display.set_icon(ICO)
#initialization of some sprites 
#game loop
def main():
    global levelo
    run=True
    while run:
        WIN.fill((12,45,72))
        start()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
               

def start():
    PYTHON=pygame.image.load('assets/python.png').convert()
    LOGO=pygame.image.load('assets/logo.png').convert()
    WIN.fill((12,45,72))
    WIN.blit(FRAME,(0,0))
    WIN.blit(PYTHON,(21,21))
    WIN.blit(LOGO,(25,567))
    FONT.render_to(WIN,(81 ,400),'PYTHON',(208,8,0),None,0,0,128)
    FONT.render_to(WIN,(300,500),'PRESS ENTER TO PLAY',(208,8,0),None,0,0,50)
    if levelo > 1:
        FONT.render_to(WIN,(300,550),'YOU WILL START FROM LEVEL ' + str(levelo-1),(208,8,0),None,0,0,25)
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    pygame.mixer.init()
                    mixer.music.load('assets/ost.mp3')
                    mixer.music.play(-1)
                    transition()
                    time.sleep(1)
                    if levelo==1:
                        FONT.render_to(WIN,(300,300),'LEVEL ' + str(levelo),(208,8,0),None,0,0,50)
                    else:
                        FONT.render_to(WIN,(300,300),'LEVEL ' + str(levelo-1),(208,8,0),None,0,0,50)
                    pygame.display.update()
                    time.sleep(2)
                    if levelo==1:
                        game(levelo)
                    else:
                        game(levelo-1)
        pygame.display.update()

def transition():
    width=1
    while width <= 800:
        pygame.draw.line(WIN,(12,45,72),(0,0),(861,0),width)
        pygame.draw.line(WIN,(12,45,72),(0,651),(861,651),width)
        width+=20
        time.sleep(0.01)
        pygame.display.update()
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
    
snake_size=20

def draw_snake(snake_speed,snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(WIN,(208,8,0),[pixel[0],pixel[1],snake_size,snake_size])

def game(level):
    global levelo
    points_needed=level*2
    POINT=pygame.image.load('assets/point.png')
    HEAD1=pygame.image.load('assets/head.png')
    HEAD2=pygame.transform.rotate(HEAD1,180)
    HEAD3=pygame.transform.rotate(HEAD1,90)
    HEAD4=pygame.transform.rotate(HEAD1,270)
    UP=True
    DOWN=False
    LEFT=False
    RIGHT=False
    clock=pygame.time.Clock()
    snake_speed=1
    x=800/2
    y=600/2
    x_speed=0
    y_speed=0
    snake_pixels=[]
    snake_length=1
    target_x=round(random.randrange(50,800-snake_size)/10.0)*10
    target_y=round(random.randrange(50,600-snake_size)/10.0)*10
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_speed=-snake_size
                    y_speed=0
                    LEFT=True
                    UP=False
                    DOWN=False
                    RIGHT=False
                if event.key==pygame.K_RIGHT:
                    x_speed=snake_size
                    y_speed=0
                    RIGHT=True
                    UP=False
                    LEFT=False
                    DOWN=False
                if event.key==pygame.K_UP:
                    x_speed=0
                    y_speed=-snake_size
                    UP=True
                    DOWN=False
                    LEFT=False
                    RIGHT=False
                if event.key==pygame.K_DOWN:
                    x_speed=0
                    y_speed=snake_size
                    DOWN=True
                    UP=False
                    LEFT=False
                    RIGHT=False
        if x >801 or x<21 or y> 611 or y<21:
            mixer.music.stop()
            mixer.music.load('assets/crash.wav')
            mixer.music.play(1)
            transition()
            time.sleep(1)
            levelo=level
            FONT.render_to(WIN,(300,300),'GAME OVER',(208,8,0),None,0,0,50)
            pygame.display.update()
            time.sleep(2)
            start()
        x+=x_speed
        y+=y_speed
        WIN.fill((12,45,72))
        WIN.blit(FRAME,(0,0))
        FONT.render_to(WIN,(21,21),str(points_needed),(208,8,0),None,0,0,50)
        WIN.blit(POINT,(target_x,target_y))
        snake_pixels.append([x,y])
        if len(snake_pixels)>snake_length:
            del snake_pixels[0]
        for pixel in snake_pixels[:-1]:
            if pixel ==[x,y]:
                mixer.music.stop()
                mixer.music.load('assets/crash.wav')
                mixer.music.play(1)
                transition()
                time.sleep(1)
                levelo=level
                FONT.render_to(WIN,(300,300),'GAME OVER',(208,8,0),None,0,0,50)
                pygame.display.update()
                time.sleep(2)
                start()
        draw_snake(snake_size,snake_pixels)
        if(UP==True):WIN.blit(HEAD1,(x,y))
        if(DOWN==True):WIN.blit(HEAD2,(x,y))
        if(LEFT==True):WIN.blit(HEAD3,(x,y))
        if(RIGHT==True):WIN.blit(HEAD4,(x,y))
        pygame.display.update()
        if x==target_x and y==target_y or x==target_x+10 and y==target_y+10 or x==target_x-10 and y==target_y-10 or x==target_x and y==target_y-10 or x==target_x-10 and y==target_y or x==target_x and y==target_y+10 or x==target_x+10 and y==target_y:
            point_sound=mixer.Sound('assets/point.wav')
            point_sound.play()
            target_x=round(random.randrange(50,800-snake_size)/10.0)*10
            target_y=round(random.randrange(50,600-snake_size)/10.0)*10
            snake_length+=1
            snake_speed+=2
            points_needed-=1
            if points_needed==0:
                levelo=level
                level+=1
                transition()
                time.sleep(1)
                FONT.render_to(WIN,(300,300),'LEVEL ' + str(level),(208,8,0),None,0,0,50)
                pygame.display.update()
                time.sleep(2)
                game(level)

        clock.tick(snake_speed)
    pygame.quit()

if __name__ == "__main__":
    levelo=1
    main()