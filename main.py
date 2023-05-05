import pygame
import random
import math
from pygame import mixer



# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

#background image
background = pygame.image.load('background.jpg')

# Background Song
mixer.music.load('background.wav')
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('player.png')
playerX = 380
playerY = 450
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(20)

# Bullet

# Ready : You can't see the bullet on the screen
# Fire : The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : "+ str(score_value),True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER " ,True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))    


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27 :
        return True
    else:
        return False


# Game loop
running = True
while running:
    # screen.fill((0, 0, 0))  
    screen.blit(background,(0,0))
    # playerY -= 0.1  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check keyboards
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                playerX_change = - 0.4

            if event.key == pygame.K_2:
                playerX_change = 0.4  

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1 or event.key == pygame.K_2:
                playerX_change = 0

            if event.key == pygame.K_9:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current state of x-codinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)



    # Checking for boundries                   
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 750:
        playerX = 750    

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break    
        enemyX[i] += enemyX_change [i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 750:
            enemyX_change[i] = -0.5  
            enemyY[i] += enemyY_change[i]


        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value +=1
            
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)    

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

   

        

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()