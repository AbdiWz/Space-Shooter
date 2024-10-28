import pygame
import os
pygame.font.init()
pygame.mixer.init()

#Window Width & Height
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

#Caption
pygame.display.set_caption("Space Shooter!")

#Global Variables
WHITE = (255,255,255)							
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
FPS = 60	   									
VEL = 5		
BULLET_VEL = 7		
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40		
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)	
MAX_BULLETS = 3		

#Sound
BULLET_HIT_SOUND = pygame.mixer.Sound('assets/Bombsound.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/Gunsound.wav')

#Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT= pygame.font.SysFont('comicsans', 100)

#Create Hit Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2																		

#Window Icon
WINDOW_ICON = pygame.image.load('assets/Icon.png')
pygame.display.set_icon(WINDOW_ICON)

#Yellow Spaceship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
#Red Spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
#Space Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

#Drawing on Window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):																									
	WIN.blit(SPACE, (0,0))	
	pygame.draw.rect(WIN, BLACK, BORDER)		#Border
	red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
	yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)	
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
	WIN.blit(yellow_health_text, (10, 10))
	#Blit Draws Text and Images
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))	
	#Spaceship Coordinates are Updated to the Coordinates of the Red and Yellow Rectangle Each Time Window is Updated.																		
	WIN.blit(RED_SPACESHIP, (red.x, red.y))
	#Draw Bullets
	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)
	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)
	#Update the Window
	pygame.display.update()																										 

#Yellow Movement
def yellow_handle_movement(key_pressed, yellow):
	#When Keys Pressed, Coordinates of Yellow and Red Change 
	if key_pressed[pygame.K_a] and yellow.x - VEL > 0:							#LEFT
		yellow.x -= VEL
	elif key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:	#RIGHT
		yellow.x += VEL
	elif key_pressed[pygame.K_w] and yellow.y - VEL > 0:						#UP
		yellow.y -= VEL
	elif key_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT:	#DOWN
		yellow.y += VEL

#Red Movement
def red_handle_movement(key_pressed, red):
	if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:	#LEFT
		red.x -= VEL
	elif key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:		#RIGHT
		red.x += VEL
	elif key_pressed[pygame.K_UP] and red.y - VEL > 0:							#UP
		red.y -= VEL
	elif key_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT:		#DOWN
		red.y += VEL

#Handling Bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		#Remove Bullets That Go Offscreen
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)	
		#Remove Bullets That Go Offscreen
		elif bullet.x < 0:
			red_bullets.remove(bullet)

#Winner Text
def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()))
	pygame.display.update()
	pygame.time.delay(3000)

#Main Fuction
def main():
	#Red and Yellow Represented as Rectangles. Given Default Coordinates and Sizes of Spaceships.
	yellow = pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	#Player Bullets
	yellow_bullets = []
	red_bullets = []

	#Player Health
	yellow_health = 10
	red_health = 10

	#Controls Pygame FPS
	clock = pygame.time.Clock()																						
	run = True
	while run:
		clock.tick(FPS)
		#If Event is Quit, Loop Stops
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			#Yellow Bullets
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()
			#Red Bullets
				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
					red_bullets.append(bullet)	
					BULLET_FIRE_SOUND.play()

			#Heal System
			if event.type == RED_HIT:
				red_health -= 1
				BULLET_HIT_SOUND.play()

			if event.type == YELLOW_HIT:
				yellow_health -= 1
				BULLET_HIT_SOUND.play()	

		#Declaring Winner
		winner_text = ''
		if red_health <= 0:
			winner_text = 'Yellow Wins'

		if yellow_health <= 0:
			winner_text = 'Red Wins'

		if winner_text != '':
			draw_winner(winner_text) 
			break 

		#Handling Movement Call
		key_pressed = pygame.key.get_pressed() 
		yellow_handle_movement(key_pressed, yellow)
		red_handle_movement(key_pressed, red)
		#Handling Bullets Call
		handle_bullets(yellow_bullets, red_bullets, yellow, red)
		#Draw Function 
		draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

	#If Loop Stops Call Main Again
	main()

#Import Control
if __name__ == '__main__':
	main()