import pygame
import time
import random

#Pygame window
pygame.init()
dis_width=1300
dis_height=700
dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.update()
pygame.display.set_caption("WWII The Invasion of London")

#Clock
clock = pygame.time.Clock()
dt = clock.tick(60)

#Colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
yellow = (255,255,102)
green = (0,255,0)

#Fonts
font1 = pygame.font.Font('ChursaechsischeFraktur.ttf', 30)
font2 = pygame.font.Font('Qiko.ttf', 30)
font3 = pygame.font.Font('Marsh Stencil Regular.otf', 60)

#Title text function
def title():
	text = font3.render("WWII THE INVASION OF LONDON", True, black)
	dis.blit(text, [200, 300])

#Images
def swastika():
	sv = pygame.image.load('svastika.png')
	sv = pygame.transform.scale(sv, (100, 100))
	sv = pygame.transform.rotate(sv, 45)
	dis.blit(sv, [1000, 250])

#Floor
def floor():
	pygame.draw.rect(dis, black, [0, 650, 1300, 50])

#Score
def display_score(score):
	text = font2.render(str(score), True, black)
	dis.blit(text, [1250, 20])

def display_final_score(score):
	text = font3.render("Score: " + str(score), True, black)
	dis.blit(text, [500, 420])

#Tank
class Tank:
	image = pygame.image.load('panzer_ii_black.png')
	velocity = 1
	def __init__(self, x):
		self.x = x
		self.y = 572
	def draw(self):
		self.image = pygame.transform.scale(self.image, [200, 80])
		dis.blit(self.image, [self.x, self.y])
	def move(self):
		self.x -= self.velocity
	def get_mask(self):
		return pygame.mask.from_surface(self.image)
	def collide(self, bomb):
		bomb_mask = bomb.get_mask()
		tank_mask = self.get_mask()
		collision_point = bomb_mask.overlap(tank_mask, (self.x - bomb.x, self.y - round(bomb.y)))
		if collision_point:
			return True
		return False

#Plane
class Plane:
	image = pygame.image.load('plane_2d_2.png')
	velocity = -2
	bomb_launched = False
	def __init__(self, x, bomb):
		self.x = x
		self.y = 100
		self.bomb = bomb
	def draw(self):
		self.image = pygame.transform.scale(self.image, [200, 80])
		dis.blit(self.image, [self.x, self.y])
	def move(self):
		self.x -= self.velocity
		if self.x > 1300:
			self.x = -200
			self.velocity = -2
			self.bomb.velocity_x = -2
			self.bomb_launched = False
			self.bomb.x = -120
			self.bomb.y = 150
			self.bomb.velocity_y = 0.5
		if self.bomb_launched == False:
			self.bomb.move()
		else:
			self.bomb.drop()
	def accelerate(self):
		self.velocity = -4
		if not self.bomb_launched:
			self.bomb.velocity_x = -4

#Bomb
class Bomb:
	image = pygame.image.load('bomb2.png')
	velocity_x = -2
	velocity_y = 0.5
	def __init__(self, x):
		self.x = x
		self.y = 150
	def draw(self):
		self.image = pygame.transform.scale(self.image, [60, 15])
		dis.blit(self.image, [self.x, self.y])
	def draw_drop(self,angle):
		rotate = pygame.transform.scale(self.image, [60, 15])
		rotate = pygame.transform.rotate(rotate, angle)
		dis.blit(rotate, [self.x, self.y])
	def move(self):
		if self.x > 1500:
			self.x = -200
		self.x -= self.velocity_x
		self.draw()
	def drop(self):
		self.x -= self.velocity_x
		self.y += self.velocity_y
		self.velocity_y += 0.02
		self.draw_drop(-self.velocity_y * 15)
	def get_mask(self):
		return pygame.mask.from_surface(self.image)

def gameIntro():
	intro = True
	while intro:
		dis.fill(red)
		title()
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
		pygame.display.update()

def gameOver(score):
	pause = True
	while pause:
		dis.fill(red)
		title()
		display_final_score(score)
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pause = False
					gameLoop()
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
		pygame.display.update()



def gameLoop():
	game_over = False
	score = 0
	bomb = Bomb(-120)
	plane = Plane(-200, bomb)
	tanks = [Tank(1300), Tank(1960), Tank(2600)]
	while not game_over:
		dis.fill(red)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					game_over = True
				if event.key == pygame.K_SPACE:
					plane.bomb_launched = True
				if event.key == pygame.K_w:
					plane.accelerate()

		floor()
		display_score(score)
		plane.draw()
		plane.move()
		for tank in tanks:
			if tank.x < -200:
				tank.x = 1300
				game_over = True
			tank.move()
			tank.draw()
			if tank.collide(bomb):
				score += 1
				tanks.remove(tank)
				new_tank = Tank(random.randint(1500, 2500))
				tanks.append(new_tank)
				if score%25 == 0:
					new_tank = Tank(random.randint(1500, 2500))
					tanks.append(new_tank)
		pygame.display.update()
	gameOver(score)

gameIntro()
gameLoop()