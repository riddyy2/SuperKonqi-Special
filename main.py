import pygame
from pygame.locals import *

pygame.init()

#screen width and height
scw = 700
sch = 700
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption('Something Cool')

TheSun = pygame.image.load('Assets/Images/BG/Sun.png')

run = True
while run:

	screen.blit(TheSun, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()