#!/usr/bin/env python3
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1, player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80, 300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('sound/jump.mp3')
		self.jump_sound.set_volume(.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def anim_state(self):
		if self.rect.bottom < 300:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):
				self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.anim_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()

		if type == 'fly':
			fly1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
			fly2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
			self.frames = [fly1, fly2]
			y_pos = 200
		else:
			snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail1, snail2]
			y_pos = 300

		self.anim_index = 0
		self.image = self.frames[self.anim_index]
		self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
	
	def anim_state(self):
		self.anim_index += .1
		if self.anim_index >= len(self.frames):
			self.anim_index = 0
		self.image = self.frames[int(self.anim_index)]

	def update(self):
		self.anim_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100:
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score = test_font.render(f'Time: {current_time}', False, (64, 64, 64))
	score_rect = score.get_rect(center = (400, 50))
	screen.blit(score, score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite, obstacle_grp, False):
		obstacle_grp.empty()
		return False
	else:
		return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('RUNNER')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('sound/music.wav')
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_grp = pygame.sprite.Group()

sky = pygame.image.load('graphics/sky.png').convert()
grass = pygame.image.load('graphics/ground.png').convert()

# intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Snail Trailers', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_msg = test_font.render('Press SPACE to run', False, (111, 196, 169))
game_msg_rect = game_msg.get_rect(center = (400, 320))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_grp.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)

	if game_active:
		screen.blit(sky, (0, 0))
		screen.blit(grass, (0, 300))
		score = display_score()
		
		# Player
		player.draw(screen)
		player.update()

		# obs movement
		obstacle_grp.draw(screen)
		obstacle_grp.update()

		# collision
		game_active = collision_sprite()

	else:
		screen.fill((94, 129, 162))
		screen.blit(player_stand, player_stand_rect)

		score_msg = test_font.render(f'SCORE: {score}', False, (111, 196, 169))
		score_msg_rect = score_msg.get_rect(center = (400, 330))
		screen.blit(game_name, game_name_rect)

		if score == 0:
			screen.blit(game_msg, game_msg_rect)
		else:
			screen.blit(score_msg, score_msg_rect)

	pygame.display.update()
	clock.tick(60)
		