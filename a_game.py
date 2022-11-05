import pygame
from pygame.draw import *
from random import randint
pygame.init()

text_font = pygame.font.SysFont("Comic Sans", 24)

FPS = 30
LENGTH = 720
HEIGHT = 480
sc = pygame.display.set_mode((LENGTH, HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50,50,50)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

properties = [] #массив с данными о шариках и квадратах, координаты, радиус, скорости, цвет

def new_ball(): #создание шарика
    global x, y, r, properties
    x = randint(100,500) #координата х
    y = randint(100,400) #координата у
    r = randint(30,50) #радиус шарика
    vx = randint(-5,5)
    vy = randint(-5,5)
    color = COLORS[randint(0, 5)] #рандомный цвет
    properties.append([x,y,r,color,vx,vy,0])

def new_rect(): #Создание квадратика
    global x, y, r, properties
    x = randint(100,500) #координата х
    y = randint(100,400) #координата у
    r = randint(30,50) #сторона квадрата x2
    vx = randint(10,15) #квадратики движутся быстрее шариков
    vy = randint(10,15)
    color = COLORS[randint(0, 5)] #рандомный цвет
    properties.append([x,y,r,color,vx,vy,1]) 

def click(event):
    gotcha = False
    global properties
    if properties:
        l = len(properties)
        for i in range(l):
            x = properties[i][0]
            y = properties[i][1]
            r = properties[i][2]
            if ((event[0]-x)**2+(event[1]-y)**2) <= r**2: 
                gotcha = True
                break
    if gotcha: return i+1
    else: return False

for i in range(randint(1,3)): #начальные шарики
    new_ball()
pygame.display.update()

clock = pygame.time.Clock()
finished = False
score = 0

while not finished:
    clock.tick(FPS)
    sc.fill(GRAY)
    clicked = False
    ball = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ball = click(event.pos)
            if ball and not(clicked): #если мы нажали не на пустое место и не нажимали за этот тик до этого
                clicked = True
                if properties[ball-1][6]==0: score+=1 #начисление очков за шарик или квадратик
                else: score+=5

                properties.remove(properties[ball-1]) #создаём шарик или квадрат (шарик 100%, квадрат 50%)
                for i in range(randint(1,1)):
                    new_ball()
                for i in range(randint(0,1)):
                    new_rect()
                
    for i in range(len(properties)):
        properties[i][0]+=properties[i][4]
        properties[i][1]+=properties[i][5]
        x = properties[i][0]
        y = properties[i][1]
        r = properties[i][2]
        
        if x+r>=LENGTH or x-r<=0: #если достигли одной из страниц
            properties[i][4] = -properties[i][4]
        if y+r>=HEIGHT or y-r<=0:
            properties[i][5]= -properties[i][5]
        if properties[i][6]==0:
            circle(sc, BLACK, (x, y), properties[i][2]) #граница шарика
            circle(sc, properties[i][3], (x, y), properties[i][2]-3) #отрисовка шарика
        else:
            rect(sc, BLACK, (x-r, y-r, 2*r, 2*r)) #отрисовка границ
            rect(sc, properties[i][3], (x-r+3, y-r+3, 2*r-6, 2*r-6)) #отрисовка квадратика

    score_text = text_font.render('Your score: '+ str(score), 1, RED)
    score_rect = score_text.get_rect(topleft = (20, 20))
    sc.blit(score_text, score_rect)

    pygame.display.update()

pygame.quit()