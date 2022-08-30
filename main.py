import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the window
window = pygame.display.set_mode((800, 600))

# change title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.png")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
player_image = pygame.image.load("player.png")
playerX = 380
playerY = 470
playerX_change = 0


def player(x, y):
    window.blit(player_image, (x, y))


# enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_num = 6
for i in range(enemy_num):
    enemy_image.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 734))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    window.blit(enemy_image[i], (x, y))


# Bullet
bullet_image = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "rest"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bullet_image, (x + 16, y - 10))


# checking for the collision of the bullet with the enemy


def is_colliding_bullet(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 25:
        return True
    else:
        return False


# score
score_name = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render(f"score: {str(score_name)}", True, (255, 255, 255))
    window.blit(score, (x, y))


# function for game over
font_game_over = pygame.font.Font("freesansbold.ttf", 70)


def game_over(x, y):
    game_over = font_game_over.render("Game over", True, (255, 255, 255))
    window.blit(game_over, (x, y))


# game loop
running = True
while running:
    # background fill
    window.fill((0, 0, 0))

    # background image
    window.blit(background, (0, 0))

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == "rest":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
                bulletX_change = 0

    # will add the player in the surface
    player(playerX, playerY)

    # player bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy loop
    for i in range(enemy_num):
        # game over text
        if enemyY[i] > 400:
            for j in range(enemy_num):
                enemyY[j] = 2000
                playerY = 2000
                bulletY = -320
                bulletX_change = 0
            game_over(225, 200)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # will add the enemy to the surface
        enemy(enemyX[i], enemyY[i], i)

        # collision
        collision = is_colliding_bullet(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "rest"
            score_name += 1
            enemyX[i] = random.randint(0, 734)
            enemyY[i] = random.randint(50, 150)
            enemy_sound = mixer.Sound("explosion.wav")
            enemy_sound.play()

    # bullet movements
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY == 0:
        bulletY = 480
        bullet_state = "rest"

    # the score board:
    show_score(0, 0)

    pygame.display.update()
