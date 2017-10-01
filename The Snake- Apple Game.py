import pygame
import time
import random

pygame.init()

display_width=1000
display_height=700

white=(255,255,255)
red=(200,0,0)
light_red=(255,0,0)
light_green=(0,255,0)
green=(0,150,0)
blue=(0,0,200)
sky_blue=(153,217,234)
black=(0,0,0)

game_Display=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The Snake-Apple Game')

game_Icon = pygame.image.load('icon.png')
body_head=pygame.image.load('snakehead.png')
body=pygame.image.load('body.png')
tail_left=pygame.image.load('tailleft.png')
tail_right=pygame.image.load('tailright.png')
arena=pygame.image.load('arena.png')
apple=pygame.image.load('apple.png')

pygame.mixer.music.load("music.mp3")
crash_sound=pygame.mixer.Sound("Crash.wav")

snake_block=50
apple_block=50
frame_width=31
FPS=15

pygame.display.set_icon(game_Icon)

clock=pygame.time.Clock()

def message_Display( text ,p1 ,p2 ,sz ,color ):
    font=pygame.font.SysFont('Comic Sans MS',sz)
    TextSurf=font.render(text,True,color)
    TextRect=TextSurf.get_rect()
    TextRect.center=(p1*display_width,p2*display_height)
    game_Display.blit(TextSurf,TextRect)

def buttons( text, x, y, w, h, in_color, ac_color, sz, color,flag):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if 0<=mouse[0]-x<=w and 0<=mouse[1]-y<=h:
        pygame.draw.rect(game_Display,ac_color,[x,y,w,h])
    else:
        pygame.draw.rect(game_Display,in_color,[x,y,w,h])
    message_Display(text,(x+w/2)/float(display_width),(y+h/2)/float(display_height),sz,color)
    if 0<=mouse[0]-x<=w and 0<=mouse[1]-y<=h and click[0]==1:
        if text!='Quit':
            return False
        else:
            pygame.quit()
            quit()
    return flag
def pause():
    paused=True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        message_Display('Paused', 0.5, 0.1, 90, red)
        paused=buttons('Continue',200,450,150,70,red,light_red,25,green,paused)
        paused=buttons('Quit',724,450,100,70,red,light_red,25,green,paused)
        pygame.display.update()
        clock.tick(FPS)
def overScreen():
    Over=True
    pygame.mixer.Sound.play(crash_sound)
    while Over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        message_Display('Game Over :(', 0.5, 0.1, 90, red)
        Over=buttons('Play Again',200,450,150,70,red,light_red,25,green,Over)
        Over=buttons('Quit',724,450,100,70,red,light_red,25,green,Over)
        pygame.display.update()
        clock.tick(FPS)

def gameIntro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        game_Display.fill(light_green)
        message_Display('THE SNAKE-APPLE GAME',0.5,0.2,50,red)
        intro=buttons('Play Game',200,450,150,70,red,light_red,25,green,intro)
        intro=buttons('Quit',724,450,100,70,red,light_red,25,green,intro)
        pygame.display.update()
        clock.tick(FPS)
def draw_snake(snake_list,dir_list,state):
    for i in range(len(snake_list)):
        XnY=[]
        XnY.append(snake_list[i][0])
        XnY.append(snake_list[i][1])
        if dir_list[i]=='left':
            degree=90
        elif dir_list[i]=='right':
            degree=270
        elif dir_list[i]=='up':
            degree=0
        elif dir_list[i]=='down':
            degree=180
        if i==0:
            if len(snake_list)&1:
                if state==0:
                    game_Display.blit(pygame.transform.rotate(tail_right,degree),(XnY[0],XnY[1]))
                else:
                    game_Display.blit(pygame.transform.rotate(tail_left,degree),(XnY[0],XnY[1]))
            else:
                if state==0:
                    game_Display.blit(pygame.transform.rotate(tail_left,degree),(XnY[0],XnY[1]))
                else:
                    game_Display.blit(pygame.transform.rotate(tail_right,degree),(XnY[0],XnY[1]))
                
        else:
            if i==len(snake_list)-1:
                game_Display.blit(pygame.transform.rotate(body_head,degree),(XnY[0],XnY[1]))
            else:
                game_Display.blit(pygame.transform.rotate(body,degree),(XnY[0],XnY[1]))

def gameLoop():
    gameOver=False
    pygame.mixer.music.play(-1)
    eaten=0
    length=3
    snake_list=[]
    dir_list=[]
    snake_head=[]

    xpos=display_width/2
    ypos=display_height/2
    snake_list.append((xpos-2*snake_block,ypos))
    snake_list.append((xpos-snake_block,ypos))
    snake_head.append(xpos)
    snake_head.append(ypos)
    snake_list.append(snake_head)


    appleX=round(random.randrange(frame_width,display_width-frame_width-apple_block)/float(apple_block))*apple_block
    appleY=round(random.randrange(frame_width,display_height-frame_width-apple_block)/float(apple_block))*apple_block
    
    x_change=snake_block
    y_change=0
    direction='right'

    dir_list.append(direction)
    dir_list.append(direction)
    dir_list.append(direction)
    state=0

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    pause()
                    pygame.mixer.music.unpause()
                if event.key==pygame.K_LEFT and x_change==0:
                    x_change=-snake_block
                    direction='left'
                    y_change=0
                if event.key==pygame.K_RIGHT and x_change==0:
                    x_change=snake_block
                    direction='right'
                    y_change=0
                if event.key==pygame.K_UP and y_change==0:
                    y_change=-snake_block
                    direction='up'
                    x_change=0
                if event.key==pygame.K_DOWN and y_change==0:
                    y_change=snake_block
                    direction='down'
                    x_change=0


        game_Display.blit(arena,(0,0))
        message_Display('Score: '+str(eaten),0.85,0.06,31,red)
        game_Display.blit(apple,(appleX,appleY))

        xpos+=x_change
        ypos+=y_change
        snake_head=[]
        snake_head.append(xpos)
        snake_head.append(ypos)
        snake_list.append(snake_head)
        dir_list.append(direction)
        if length<len(snake_list):
            del snake_list[0]
            del dir_list[0]

        draw_snake(snake_list,dir_list,state)
        state=state^1
        pygame.display.update()
        if appleX<=xpos+snake_block/2.0<=appleX+apple_block and appleY<=ypos+snake_block/2.0<=appleY+apple_block :
            eaten+=1
            length+=1
            appleX=round(random.randrange(frame_width,display_width-frame_width-apple_block)/float(apple_block))*apple_block
            appleY=round(random.randrange(frame_width,display_height-frame_width-apple_block)/float(apple_block))*apple_block
        if xpos<=frame_width or xpos>=display_width-frame_width-snake_block or ypos<=frame_width or ypos>=display_height-frame_width-snake_block:
            pygame.mixer.music.stop()
            overScreen()
            gameLoop()
        for eachsegment in snake_list[:-1]:
            if eachsegment==snake_head:
            	pygame.mixer.music.stop()
                overScreen()
                gameLoop()
        clock.tick(0.5*FPS)

gameIntro()
gameLoop()
pygame.quit()
quit()
