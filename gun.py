import math
from random import choice
from random import randint

import pygame

pygame.init()
score_font = pygame.font.SysFont("Comic Sans", 40)

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
DARK_GREEN = (31,85,0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

ticker = 0
gticker = 0
points = 0

balls = []
bombs = []

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=HEIGHT-40, type = 0, r = 10, vx = 0, vy = 0):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = choice(GAME_COLORS)
        self.live = 0
        self.bounces = 0
        self.g = 0.5
        self.type = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        
        if self.x + self.r + self.vx>= WIDTH: #Страшное описание движения шарика
            self.vx = -self.vx*0.5
        if self.y + self.r - self.vy + self.g>= HEIGHT:
            self.vy = -self.vy*0.5
            self.vx = self.vx*0.5
            self.bounces+=1
        if self.bounces>=6: 
            self.vy = 0
            self.vx = 0
            self.g = 0
            self.bounces = 0
            

        vy = self.vy-self.g
        self.x += self.vx
        self.y -= self.vy
        self.vy = vy

    def draw(self):
        global GAME_COLORS
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r
        )
        if self.type == 0:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r-2
            )
        else:
            pygame.draw.circle(
                self.screen,
                GAME_COLORS[randint(0,5)],
                (self.x, self.y),
                self.r-2
            )
        self.live+=1

    def hittest(self, obj):
        if ((obj.x - self.x)**2 + (obj.y - self.y)**2 <= (obj.r+self.r)**2): return True
        else: return False

    def explode(self):
        global balls
        for i in range(randint(5,8)):
            explosion = Ball(screen, x = self.x, y = self.y, r = 8, vx = randint(-5,5)*5, vy = randint(1,5)*5)
            balls.append(explosion)

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 5
        self.f2_on = 0
        self.an = 1
        self.color = DARK_GREEN
        self.x = 30
        self.y = HEIGHT-40
        self.l = 40
        self.x_pos = 30
        self.vx = 0
        self.a = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        Пкм для особого снаряда.
        """
        global balls, bullet, shots
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.x = self.x_pos
        k = 1
        if event.button==3: 
            new_ball.type=1
            k = 1.5
        
        dy = event.pos[1]-new_ball.y
        dx = event.pos[0]-new_ball.x
        self.an = math.atan2(dy, dx)
        
        new_ball.vx = k * self.f2_power * math.cos(self.an)
        new_ball.vy = - k * self.f2_power * math.sin(self.an)
        
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 5

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        
        self.x = event.pos[0]
        self.y = event.pos[1]
        
        if event:
            if self.x-self.x_pos!=0: self.an = math.atan((self.y-HEIGHT+40) / (self.x-self.x_pos))
            else: self.an = math.atan((self.y-HEIGHT+40) / (self.x-self.x_pos+1))
            if self.x-self.x_pos<0: self.an+=math.pi
        if self.f2_on:
            self.color = RED
        else:
            self.color = DARK_GREEN

    def draw(self):
        global ticker
        if self.f2_on:
            ticker+=1
            if self.l < 100 and ticker >= 20:
                self.l+=1
                l = self.l
            elif self.l < 100 and ticker < 20:
                l = self.l
            elif self.l == 100:
                l = 100
            
        else:
            ticker = 0
            self.l = 50
            l = self.l
        
        pygame.draw.line(screen, BLACK, [self.x_pos, HEIGHT-40], [l*math.cos(self.an)+self.x_pos, l*math.sin(self.an)+HEIGHT-40], 10)
        pygame.draw.line(screen, self.color, [self.x_pos, HEIGHT-40], [l*math.cos(self.an)+self.x_pos, l*math.sin(self.an)+HEIGHT-40], 8)
        pygame.draw.rect(screen, DARK_GREEN, (self.x_pos-40, HEIGHT-40,80,30))
        pygame.draw.rect(screen, BLACK, (self.x_pos-40, HEIGHT-40,80,30), 2)
        pygame.draw.ellipse(screen, BLACK, (self.x_pos - 20, HEIGHT-50, 40,15))
        pygame.draw.ellipse(screen, BLACK, (self.x_pos - 0, HEIGHT-40, 60,30))
        pygame.draw.ellipse(screen, DARK_GREEN, (self.x_pos - 1, HEIGHT-39, 58,28))
        pygame.draw.ellipse(screen, DARK_GREEN, (self.x_pos - 20, HEIGHT-49, 38,13))
        for i in range(-2,2):
            pygame.draw.circle(screen, BLACK, (self.x_pos-10+20*(i+1), HEIGHT-10), 10)
            pygame.draw.circle(screen, DARK_GREEN, (self.x_pos-10+20*(i+1), HEIGHT-10), 8)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = DARK_GREEN

    def move(self, keys):
        
        self.a = 0.1
        if keys[pygame.K_d]: 
            if self.vx<0: self.a+=0.4
            self.vx+=self.a
          
        elif keys[pygame.K_a]: 
            if self.vx>0: self.a+=0.4
            self.vx-=self.a
            
        elif self.vx:
            if self.vx>0: 
                o = True
            else: o = False
            self.a = 0.4
            if self.vx>0: self.vx-=self.a
            else: self.vx+=self.a
            if self.vx<0 and o: self.vx = 0
            elif self.vx>0 and not(o): self.vx = 0
        if self.x_pos+self.vx+40>=WIDTH or self.x_pos+self.vx-30<=0: self.vx=-self.vx
            
        else: self.a = 0
        self.x_pos+=self.vx

    def hittest(self, obj):
        if obj.x>=self.x_pos-40 and obj.x<=self.x_pos+70 and obj.y>=HEIGHT-50: return True
        else: return False


class Target:
    def __init__(self, type):
        """ Инициализация новой цели. """
        
        self.points = 1
        self.live = 1
        x = self.x = randint(200, 600)
        y = self.y = randint(50, 300)
        r = self.r = randint(20, 50)
        color = self.color = RED
        self.vx = 5
        self.vy = 5
        self.type = type

    def hit(self, point=1):
        """Попадание шарика в цель."""
        global points
        points+=self.points
        
    def move(self):
        """Движение цели в зависимости от типа"""
        global gticker
        if self.type==1:
            self.vx = 5*math.cos(0.1*gticker)
            self.vy = 5*math.sin(0.1*gticker)
            self.y += self.vy
        self.x += self.vx
        
        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.vx = -self.vx
            

    def draw(self):

        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r-2)
        if self.type==1:
            pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r*0.2)


class bomb:
    def __init__(self, x, y, vx):
        """Создание бомбочки"""
        self.x = x
        self.y = y
        self.vy = 0
        self.vx = vx
        self.g = 0.5

    def move(self):
        self.vy+=self.g
        self.x+=self.vx
        self.y+=self.vy

    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 10)
        pygame.draw.circle(screen, GREY, (self.x, self.y), 8)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
can_shoot = True


clock = pygame.time.Clock()
gun = Gun(screen)
targets = []
for i in range(randint(1,3)):
    targets.append(Target(type = randint(0,1)))
finished = False
eventik = 0
shots = 0
we_are_leaving = False
lticker = 0

while not finished:
    gticker+=1
    screen.fill(WHITE)
    gun.draw()
    for i in range(len(targets)):
        targets[i].move()
        if targets[i].live: targets[i].draw()
    
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or we_are_leaving:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and can_shoot:
            shots+=1
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            eventik = event
    if eventik:
        gun.targetting(eventik)
    keys = pygame.key.get_pressed()
    gun.move(keys)

    for b in balls:
        b.draw()
        b.move()
        for i in range(len(targets)):
            if b.hittest(targets[i]) and targets[i].live:
                targets[i].live = 0
                targets[i].hit()

        if b.live >= FPS*1 and b.type==1:
            b.explode()
            balls.remove(b)
        elif b.live >= FPS*3 and b.type==0:
            balls.remove(b)

    
    for i in range(len(targets)):
        if gticker%(50*(i+1))==0 and targets[i].live:
            bombs.append(bomb(x = targets[i].x, y = targets[i].y, vx = targets[i].vx))

    for bomba in bombs:
        bomba.move()
        bomba.draw()
        if bomba.y>=HEIGHT: bombs.remove(bomba)
        if gun.hittest(bomba): 
            
            while lticker<=210:
                lticker+=1
                clock.tick(FPS)
                screen.fill(WHITE)
                score_text = score_font.render('Вы проиграли!!', 1, (12,12,56))
                score_text1 = score_font.render('Ваш счёт: '+str(points), 1, (0,0,0))
                score_rect = score_text.get_rect(center = (WIDTH//2, HEIGHT//2-40))
                score_rect1 = score_text.get_rect(center = (WIDTH//2, HEIGHT//2))
                screen.blit(score_text1, score_rect1)
                screen.blit(score_text, score_rect)
                pygame.display.update()
                we_are_leaving = True

    alive = False
    for i in range(len(targets)):
        if targets[i].live:
            sgticker = gticker
            alive = True
    if not(alive):
        can_shoot = False
        score_text = score_font.render('Ваш счёт: '+str(points), 1, (0,0,0))
        score_rect = score_text.get_rect(center = (WIDTH//2, HEIGHT//2))
        screen.blit(score_text, score_rect)
        targets = []
        
    if gticker-sgticker==FPS*3:
        for i in range(randint(1,3)):
            type1 = randint(0,1)
            targets.append(Target(type = type1))
        balls = []
        screen.fill(WHITE)
        
        can_shoot = True

    gun.power_up()
    pygame.display.update()

pygame.quit()
