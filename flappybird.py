import os
import pygame
from pygame.locals import *
import random

path_to_blappy_fird = '/Users/misalsahoo/Desktop/Coding Projects/blappy fird'
os.chdir(path_to_blappy_fird)

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Blappy Fird")

#font variables
font = pygame.font.SysFont('Bauhaus 93', 100)

#color variables
red = (255, 0, 0)

# game variables
ground_scroll = 0
scroll_speed = 4 # every iteration is 4 pixels
flying = False
game_over = False
pipe_gap = 150
pipe_freq = 1500 # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
pass_pipe = False

# images
background = pygame.image.load('images/bg.png')
ground = pygame.image.load('images/ground.png')
button = pygame.image.load('images/restart.png')

def draw_score(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	score = 0
	return score

class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for i in range(1, 4):
			img = pygame.image.load(f'images/bird{i}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.velocity = 0
		self.clicked = False

	def update(self): # handling the animation
		#gravity component of bird
		
		if flying == True:

			self.velocity += 0.5
			if self.velocity > 8:
				self.velocity = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.velocity)

		if game_over == False:
			# bird jumping function
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.velocity = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False


			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			# bird rotation
			self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2.1)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], self.velocity -90)
class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/pipe.png')
		self.rect = self.image.get_rect()
		#position 1 is top, -1 is bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
		if position == -1:
			self.rect.topleft = [x,y + int(pipe_gap / 2)]
	
	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
	
	def draw(self): 

		action = False
		#mouse position
		pos = pygame.mouse.get_pos()

		# check if mouse is hovering over restart button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
		
		#drawing button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action



bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)
		
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button)

run = True
while run:

	clock.tick(fps)

	screen.blit(background, (0,0))

	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)


	screen.blit(ground, (ground_scroll, 768))

	# checking score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	
	draw_score(str(score), font, red, int(screen_width / 2), 20)
		


	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True


	#bird ground collision check
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False

	if game_over == False and flying == True:
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_freq:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height /2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height /2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now

		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0

		pipe_group.update()

# restarting game after gave over
	if game_over == True:
		if button.draw() == True:
			game_over = False
			score = reset_game

	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()