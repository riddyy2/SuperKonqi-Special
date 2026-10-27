#this is my first time using pygame
#so i'm probably doing something weird




import pygame
from pygame.locals import *

pygame.init()

#stuff
import pygame

class SpriteSheet:
	def __init__(self, filename, scale=1):
		"""itn'nit?"""
		try:
			okThisIsTheImage = pygame.image.load(filename).convert_alpha()
			self.sheet = pygame.transform.scale(okThisIsTheImage, (okThisIsTheImage.get_width()*scale,okThisIsTheImage.get_height()*scale))
			
		except pygame.error as e:
			print(f"Unable to load spritesheet image: {filename}")
			raise SystemExit(e)

	def get_image(self, x, y, width, height):
		"""grabs specific rectangle area out of the spritesheet"""
		rect = pygame.Rect(x, y, width, height)
		image = self.sheet.subsurface(rect)
		return image

	def load_strip(self, rect, image_count):
		"""loads horizontal strip of images and returns as a list"""
		tup = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
			   for x in range(image_count)]
		return [self.get_image(*frame) for frame in tup]

class Player(pygame.sprite.Sprite):
	def __init__(self, PlayCharName = "Konqi", State = "base", spriteWidth = 32, spriteHeight = 24, scale = 2):
		super().__init__()
		self.spritesheet = SpriteSheet(f"Assets/Images/Sprites/Players/{PlayCharName}/{State}.png", scale) 
		#something goes here
		

		self.frames = []
		self.spriteWidth = spriteWidth * scale
		self.spriteHeight = spriteHeight * scale
		
		for i in range(4): #frame count i'll make this editable later idk what i want to do with it tho
			frame = self.spritesheet.get_image(i * self.spriteWidth, 0, self.spriteWidth, self.spriteHeight)
			self.frames.append(frame)

		self.current_frame = 0
		self.animation_speed = 0.15 
		
		self.image = self.frames[int(self.current_frame)]
		self.rect = self.image.get_rect()
		self.rect.center = (0, 0)

	def update(self, action = "idle", position = (0,0)):
		"""Handles updating the animation frame."""
		self.current_frame += self.animation_speed

		self.rect.center = position
		
		match action:
			case "idle":
				self.current_frame = 0
			case "walk":
				self.current_frame += self.animation_speed
				if self.current_frame >= 3:
					self.current_frame = 1
			case "air":
				self.current_frame = 2
			case "crouch":
				self.current_frame = 3
			
		self.image = self.frames[int(self.current_frame)]


#screen width and height
scw = 700
sch = 700
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption('Something Cool')


all_sprites = pygame.sprite.Group()
player = Player("Konqi", "base", 32, 24, 5)
all_sprites.add(player)

clock = pygame.time.Clock()

running = True
while running:
	screen.fill((40, 40, 40))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	all_sprites.update()
	all_sprites.draw(screen)
	
	pygame.display.flip()
	clock.tick(60)
	#Fuck you btw
	#thanks jamie

pygame.quit()