#this is my first time using pygame
#so i'm probably doing something weird

#10/27 discovered jamie used ai. oof :C
#de-ai-ified some stuff and made some variables sexier

debug = True


import pygame
from pygame.locals import *

pygame.init()
scw = 700
sch = 700
screen = pygame.display.set_mode((scw, sch))
pygame.display.set_caption('Something Cool')

#stuff
import pygame

TileGroup = pygame.sprite.Group()

class SpriteSheet:
	def __init__(self, filename, scale=1):
		"""itn'nit?"""
		try:
			okThisIsTheImage = pygame.image.load(filename).convert_alpha()
			self.sheet = pygame.transform.scale(okThisIsTheImage, (okThisIsTheImage.get_width()*scale,okThisIsTheImage.get_height()*scale))
			
		except pygame.error as e:
			print(f"Unable to load spritesheet image: {filename}")
			raise SystemExit(e)

	def get_image(self, x, y, width, height, flip):
		"""grabs specific rectangle area out of the spritesheet"""
		rect = pygame.Rect(x, y, width, height)
		image = pygame.transform.flip(self.sheet.subsurface(rect),flip,False)

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
		self.posX = 80
		self.posY = 80
		self.velX = 0
		self.velY = -1
		self.health = 3
		self.hitCooldown = 0
		self.onGround = False

		#player physics
		self.frictionGround = 1.4
		self.frictionAir = 1.03
		self.frictionCrouch = 1.2
		self.speed = 1
		self.speedAir = 0.4
		self.jumpForce = 13
		self.gravity = 0.8
		self.jumpGravity = 0.5
		self.maxFallVelocity = 12

		#visual
		self.debugBoxColor = (255,0,0)
		self.animationState = "idle"
		self.imgOffX = -10.8 * scale
		self.imgOffY = -9.6 * scale
		self.isFacingLeft = True


		self.frames = []
		self.spriteWidth = spriteWidth * scale
		self.spriteHeight = spriteHeight * scale
		
		for i in range(5): #frame count i'll make this editable later idk what i want to do with it tho
			frame = self.spritesheet.get_image(i * self.spriteWidth, 0, self.spriteWidth, self.spriteHeight, False)
			self.frames.append(frame)

		self.current_frame = 0
		self.animationSpeed = 0.15 
		
		self.image = self.frames[int(self.current_frame)]
		self.rect = self.image.get_rect().scale_by((0.3, 0.6))
		self.rect.topleft = (self.posX, self.posY)
	
	def jump(self):
		if self.onGround:
			self.velY = -self.jumpForce
			self.onGround = False

	def move(self, collision_tiles, danger_tiles):
		keys = pygame.key.get_pressed()
		self.animationState = "idle"

		if keys[pygame.K_SPACE]:
			self.jump()

		frictionFinal = self.frictionGround
		if self.hitCooldown > 1.4:
			self.animationState = "hurt"
		elif keys[pygame.K_s]:
			self.animationState = "crouch"
			frictionFinal = self.frictionCrouch
		else:
			if keys[pygame.K_a] and self.velX > -4:
				self.isFacingLeft = True
				self.debugBoxColor = (25,0,0)
				self.animationState = "walk"
				if self.onGround:
					self.velX -= self.speed
				else:
					self.velX -= self.speedAir
			if keys[pygame.K_d] and self.velX < 4:
				self.isFacingLeft = False
				self.debugBoxColor = (0,0,25)
				self.animationState = "walk"
				if self.onGround:
					self.velX += self.speed
				else:
					self.velX += self.speedAir
			if self.onGround:
				self.debugBoxColor = (0,0,0)
			else:
				self.debugBoxColor = (0,255,0)
				self.animationState = "air"
				frictionFinal = self.frictionAir
		try:
			self.velX = self.velX/frictionFinal
		except ZeroDivisionError:
			self.velX = 0
		print(self.velX, frictionFinal)
		self.posX += self.velX
		self.rect.x = round(self.posX)
		hits = [tile for tile in collision_tiles if self.rect.colliderect(tile)]
		if hits:
			if self.velX > 0:
				self.rect.right = min(tile.left for tile in hits)
			elif self.velX < 0:
				self.rect.left = max(tile.right for tile in hits)
			self.velX = 0
			self.posX = self.rect.x

		appliedGravity = self.gravity
		if keys[pygame.K_SPACE]:
			appliedGravity = self.jumpGravity
		self.velY = min(self.velY + appliedGravity, self.maxFallVelocity)+0.1
		self.posY += round(self.velY)
		self.rect.y = round(self.posY) #round? idk
		self.onGround = False
		hits = [tile for tile in collision_tiles if self.rect.colliderect(tile)]
		if hits:
			if self.velY > 0:
				self.rect.bottom = min(tile.top for tile in hits)
				self.onGround = True
			elif self.velY < 0:
				self.rect.top = max(tile.bottom for tile in hits)
			self.velY = 0
			self.posY = self.rect.y

		dangerTouch = [tile for tile in danger_tiles if self.rect.colliderect(tile)]
		if dangerTouch and self.hitCooldown <= 0:
			self.hitCooldown = 2
			self.health -= 1
			self.velX *= -1.2
			self.velY *= -1.2

	def update(self, collision_tiles, danger_tiles):
		"""it's moving"""
		print(self.isFacingLeft)

		if self.hitCooldown > 0:
			self.hitCooldown -= 0.1

		if self.health <= 0:
			print("oof")
		else:
			self.move(collision_tiles, danger_tiles)

		match self.animationState:
			case "idle":
				self.current_frame = 0
			case "walk":
				self.current_frame += self.animationSpeed
				if self.current_frame >= 3:
					self.current_frame = 1
			case "air":
				self.current_frame = 2
			case "crouch":
				self.current_frame = 3
			case "hurt":
				self.current_frame = 4
			
		self.image = pygame.transform.flip(self.frames[int(self.current_frame)], self.isFacingLeft, False)

	def draw(self, surface, offsetX, offsetY):
		draw_pos = (self.rect.x + self.imgOffX - offsetX, self.rect.y + self.imgOffY - offsetY)
		surface.blit(self.image, draw_pos)

#tiles and shit

TileScale = 32
TileSpritesheets = {
	1: SpriteSheet('Assets/Images/Tiles/Tiles01.png', 2)
}
TileTextures = {
	"GrassUL": TileSpritesheets[1].get_image(0,0,32,32,False),
	"GrassUC": TileSpritesheets[1].get_image(32,0,32,32,False),
	"GrassUR": TileSpritesheets[1].get_image(64,0,32,32,False),
	"GrassCL": TileSpritesheets[1].get_image(0,32,32,32,False),
	"Dirt": TileSpritesheets[1].get_image(32,32,32,32,False),
	"GrassCR": TileSpritesheets[1].get_image(64,32,32,32,False),
	"GrassLL": TileSpritesheets[1].get_image(0,64,32,32,False),
	"GrassLC": TileSpritesheets[1].get_image(32,64,32,32,False),
	"GrassLR": TileSpritesheets[1].get_image(64,64,32,32,False),

	"SpikeUC": TileSpritesheets[1].get_image(32,96,32,32,False),
	"SpikeCL": TileSpritesheets[1].get_image(0,128,32,32,False),
	"SpikeCR": TileSpritesheets[1].get_image(64,128,32,32,False),
	"SpikeLC": TileSpritesheets[1].get_image(32,160,32,32,False)
}
TileProperties = {
	"GrassUL": "solid",
	"GrassUC": "solid",
	"GrassUR": "solid",
	"GrassCL": "solid",
	"Dirt": "solid",
	"GrassCR": "solid",
	"GrassLL": "solid",
	"GrassLC": "solid",
	"GrassLR": "solid",

	"SpikeUC": "danger",
	"SpikeCL": "danger",
	"SpikeCR": "danger",
	"SpikeLC": "danger"
}
blocks = []
danger = []

def BuildMap(map_data, cameraX, cameraY):
	global blocks, danger
	for row_idx, row in enumerate(map_data):
		for col_idx, tile_type in enumerate(row):
			x = col_idx * TileScale
			y = row_idx * TileScale

			if tile_type in TileTextures:
				screen.blit(TileTextures[tile_type], (x - cameraX, y - cameraY))

				if TileProperties[tile_type] == "solid":
					tile_rect = pygame.Rect(x, y, TileScale, TileScale)
					blocks.append(tile_rect)
				if TileProperties[tile_type] == "danger":
					tile_rect = pygame.Rect(x, y, TileScale, TileScale)
					danger.append(tile_rect)


PlayerGroup = pygame.sprite.Group()

player = Player("Konqi", "base", 32, 24, 2)
PlayerGroup.add(player)

#camera?
camX = 0
camY = 0
camSmoothX = 4
camSmoothY = 70

clock = pygame.time.Clock()

running = True
while running:
	camX -= (scw/2)/camSmoothX
	camY -= (sch/2)/camSmoothY
	screen.fill((40, 40, 40))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	tiles = BuildMap([
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[],
		[0, "SpikeUC", 0],
		["GrassUL","GrassUC","GrassUR"],
		["GrassCL","Dirt","GrassCR"],
		["GrassLL","GrassLC","GrassLR"]
		], camX, camY) #this is gonna be annoying isn't it
			
	PlayerGroup.update(blocks, danger)
	PlayerCount = len(PlayerGroup)
	for indvPlayer in PlayerGroup:
		indvPlayer.draw(screen, camX, camY)
		camX -= (camX - indvPlayer.posX)/camSmoothX
		camY -= (camY - indvPlayer.posY)/camSmoothY

		
	
	pygame.display.flip()
	clock.tick(60)
	#Fuck you btw
	#fuck you too

pygame.quit()
