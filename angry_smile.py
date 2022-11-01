import pygame
from pygame.draw import *

pygame.init()

LENGTH = 720
HEIGHT = 480
sc = pygame.display.set_mode((LENGTH,HEIGHT))

FPS = 60
clock = pygame.time.Clock()

YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)
GRAY = (50,50,50)

sc.fill(GRAY)
circle(sc, BLACK, (LENGTH//2, HEIGHT//2), 102)
circle(sc, YELLOW, (LENGTH//2, HEIGHT//2), 100)
circle(sc, RED, (LENGTH//2-50, HEIGHT//2), 20)
circle(sc, RED, (LENGTH//2+50, HEIGHT//2), 20)
circle(sc, BLACK, (LENGTH//2-50, HEIGHT//2), 10)
circle(sc, BLACK, (LENGTH//2+50, HEIGHT//2), 10)
polygon(sc, BLACK, ((270, 180),(330, 220),(320, 230),(260, 190)))
polygon(sc, BLACK, ((450, 180),(390, 230),(380, 220),(440, 170)))
rect(sc, BLACK, (320, 280, 80, 20))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	pygame.display.update()
	clock.tick(FPS)
