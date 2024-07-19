import pygame 
import random 
import math
import sys

from pygame import mixer

# Initialize the pygame 
pygame.init()

# It is a tuple and screen is a variable 
# It need width and the height of the screen that you want to create 
# Create a screen
x_axis = 800
y_axis = 600 
screen = pygame.display.set_mode((x_axis , y_axis))  #px

# Background 
backgroundimg = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = x_axis // 2 - 32
playerY = y_axis - 100
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 10

for i in range(num_enemy):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, x_axis - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(15)
    enemyY_change.append(80)

# Bullet
# Here two states --> ready state and the fire state
# ready state -->     You don't able to see the bullet movement 
# fire state -->      Fire means , bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = y_axis - 100
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Score 
score = 0  
font = pygame.font.Font('freesansbold.ttf', 40)

textX = 10
textY = 10

# Colors 
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0 , 0 , 255)

# Required Fonts
over_font = pygame.font.Font('freesansbold.ttf', 64)
button_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 50) 

def game_over_text():
    # Draw the box
    pygame.draw.rect(screen, white, (150, 200, 500, 200))
    pygame.draw.rect(screen, black, (150, 200, 500, 200),5)
    
    # Render the game over 
    over_text = over_font.render("GAME OVER", True, red)
    screen.blit(over_text, (200, 250))

    pygame.draw.rect(screen, white, (300, 350, 200, 50))
    pygame.draw.rect(screen, black, (300, 350, 200, 50), 5)
    play_again_text = button_font.render("Play Again", True, black)
    screen.blit(play_again_text, (310, 360))

def score_value(x, y):
    score_val = font.render("Score : " + str(score), True, yellow)
    screen.blit(score_val, (x, y))
    
def player(x, y):
    screen.blit(playerImg, (x, y)) # blit means just put an image on the game surface  

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  

def fire_bullet(x, y):
    global bullet_state 
    bullet_state = "fire"
    
    # The bullet should appear in the middle of the player spaceship
    screen.blit(bulletImg, (x + 16, y + 10))   

def is_collision_happens(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 30:
        return True 
    else:
        return False

def reset_game():
    global playerX, playerX_change, bulletX, bulletY, bullet_state, score, enemyX, enemyY, enemyX_change, enemyY_change, game_over
    playerX = x_axis // 2 - 32
    playerX_change = 0
    bulletX = 0
    bulletY = y_axis - 100
    bullet_state = "ready"
    score = 0
    for i in range(num_enemy):
        enemyX[i] = random.randint(0, x_axis - 64)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 0.5
        enemyY_change[i] = 50   

# Game Loop
running = True
game_over = False

while running:
    # RGB = Red, Green, Blue
    screen.fill(blue)
    
    screen.blit(backgroundimg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX 
                    fire_bullet(bulletX, bulletY)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and 300 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 400:
                reset_game()
    
    # Check for the boundary cases for player  
    playerX += playerX_change
    
    if playerX <= 0: 
        playerX = 0
    elif playerX >= x_axis - 64:
        playerX = x_axis - 64 # just stay there because it is the border of the screen 
        
    for i in range(num_enemy): 
            
            if enemyY[i] > y_axis - 110:
                game_over = True
                for j in range(num_enemy):
                    enemyY[j] = 2000
                playerX = x_axis + 1000
                game_over_text()
                break
            
            enemyX[i] += enemyX_change[i]
            
            if enemyX[i] <= 0: 
                enemyX_change[i] = 0.5
                enemyY[i] += enemyY_change[i]
                
            elif enemyX[i] >= x_axis - 64:
                enemyX_change[i] = -0.5
                enemyY[i] += enemyY_change[i]
            
            # Collision 
            collision = is_collision_happens(bulletX, bulletY, enemyX[i], enemyY[i])
            if collision: 
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = y_axis - 100
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, x_axis - 64)
                enemyY[i] = random.randint(0, 100)
            
            enemy(enemyX[i], enemyY[i], i)
          
    # Bullet Movement 
    if bulletY <= 0:
        bulletY = y_axis - 100
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
         
    player(playerX, playerY)
    score_value(textX, textY)
    pygame.display.update()

pygame.quit()
sys.exit()
