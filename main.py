#this is my first time using pygame
#so i'm probably doing something weird




import pygame
from pygame.locals import *

pygame.init()
scw = 700
sch = 700
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption('Something Cool')

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
  
		#player stats
		self.speed = 5
		self.jump = 10
		

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
	
	def handle_input(self):
		"""guess"""
		keys = pygame.key.get_pressed()

		#velocity for later
		dx = 0
		dy = 0

		if keys[pygame.K_a]:
			dx = -self.speed
		if keys[pygame.K_d]:
			dx = self.speed

		self.rect.x += dx
		self.rect.y += dy

	def update(self, action = "idle"):
		"""Handles updating the animation frame."""
		self.current_frame += self.animation_speed
		
		self.handle_input()
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

#tiles and shit
TileScale = 32
TileTextures = {
	1: pygame.transform.scale(pygame.image.load('Assets/Images/Tiles/Tiles01.png').convert_alpha(), (TileScale, TileScale))
}
def draw_and_build_physics(map_data):
    solid_blocks = []  # Clear/rebuild list every frame for collisions

    for row_idx, row in enumerate(map_data):
        for col_idx, tile_type in enumerate(row):
            # Calculate pixel positions
            x = col_idx * TileScale
            y = row_idx * TileScale

            # 1. Render the texture if it exists
            if tile_type in TileTextures:
                screen.blit(TileTextures[tile_type], (x, y))

            # 2. Add bounding box for solid blocks
            if tile_type == 1:
                tile_rect = pygame.Rect(x, y, TileScale, TileScale)
                solid_blocks.append(tile_rect)
                
    return solid_blocks


PlayerGroup = pygame.sprite.Group()

player = Player("Konqi", "base", 32, 24, 5)
PlayerGroup.add(player)

clock = pygame.time.Clock()

running = True
while running:
	screen.fill((40, 40, 40))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
	PlayerGroup.update()
	PlayerGroup.draw(screen)
 
	draw_and_build_physics([[1,1,1]]) #this is gonna be annoying isn't it
	
	pygame.display.flip()
	clock.tick(60)
	#Fuck you btw
	#thanks jamie

pygame.quit()