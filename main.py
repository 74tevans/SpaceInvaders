import pygame
import random
import time
from pygame import mixer

pygame.init()

# Set up game window
sWidth = 1920
sHeight = 1080
screen = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(pygame.image.load('spaceship-black.png'))
background = pygame.image.load('space-bg.png')

# Music
mixer.music.set_volume(0.2)
mixer.music.load('Main.mp3')
mixer.music.play(-1)  # -1 infinitely loops

# Framerate and setting up framerate independent movement
clock = pygame.time.Clock()
prev = time.time()
dt = 0
fps = 60
target = 60

# Player hitbox (Rect) and settings
playerImg = pygame.image.load('spaceship-colour.png')
playerRect = playerImg.get_rect()
playerRect.centerx = sWidth / 2
playerRect.centery = sHeight - 100
playerChangeX = 0
playerChangeY = 0
playerSpeed = 4
playerState = 'alive'
playerDown = mixer.Sound('Player Down.mp3')

# Bullet hitboxes and settings
playerBulletImg = pygame.image.load('bullet.png')
playerBulletRect = playerBulletImg.get_rect()
playerBulletChangeY = 8
playerBulletState = 'ready'
fire = mixer.Sound('Fire.mp3')
fire.set_volume(0.4)

# Enemies
enemyType = []
enemyImg = []
enemyRect = []
enemyState = []
enemyStartX = 100
enemyStartY = 100
enemyCols = 10
enemyRows = 1
enemyChangeX = 1.5
enemyChangeY = 128
enemyDirection = 'right'
enemyBulletImg = []
enemyBulletRect = []
enemyBulletState = []
enemyBulletFreq = 1000
enemyBulletNormChangeY = 6
enemyBulletRareChangeY = 8
enemyDown = mixer.Sound('Invader Down.mp3')

# General
mode = 'title'
scoreValue = 0
level = 0
titleFont = pygame.font.Font('ATROX.TTF', 128)
optionFont = pygame.font.Font('ATROX.TTF', 48)
scoreFont = pygame.font.Font('ATROX.TTF', 48)
goFont = pygame.font.Font('ATROX.TTF', 128)
levelFont = pygame.font.Font('ATROX.TTF', 48)

def display_title():
    titletext = titleFont.render('SPACE INVADERS', True, (255, 255, 255))
    titlerect = titletext.get_rect()
    titlerect.center = (sWidth / 2, sHeight / 2)
    playtext = optionFont.render('Play: Press ENTER', True, (255, 255, 255))
    playrect = playtext.get_rect()
    playrect.center = (sWidth / 2, sHeight / 2 + 100)
    quittext = optionFont.render('Quit: Press ESCAPE', True, (255, 255, 255))
    quitrect = quittext.get_rect()
    quitrect.center = (sWidth / 2, sHeight / 2 + 150)
    screen.blit(titletext, titlerect)
    screen.blit(playtext, playrect)
    screen.blit(quittext, quitrect)

def display_score():
    scoretext = scoreFont.render('Score: ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(scoretext, (10, 10))

def display_level():
    leveltext = levelFont.render('Level: ' + str(level), True, (255, 255, 255))
    levelrect = leveltext.get_rect()
    levelrect.topright = (sWidth - 10, 10)
    screen.blit(leveltext, levelrect)

def game_over():
    global sHeight, sWidth, playerSpeed, playerState
    gotext = goFont.render('GAME OVER', True, (255, 255, 255))
    gorect = gotext.get_rect()
    gorect.center = (sWidth / 2, sHeight / 2)
    playtext = optionFont.render('Play: Press ENTER', True, (255, 255, 255))
    playrect = playtext.get_rect()
    playrect.center = (sWidth / 2, sHeight / 2 + 100)
    quittext = optionFont.render('Quit: Press ESCAPE', True, (255, 255, 255))
    quitrect = quittext.get_rect()
    quitrect.center = (sWidth / 2, sHeight / 2 + 150)
    screen.blit(gotext, gorect)
    screen.blit(playtext, playrect)
    screen.blit(quittext, quitrect)
    playerSpeed = 0
    playerState = 'dead'

# Draw player icon at x, y coords
def player(x, y):
    if playerState == 'alive':
        screen.blit(playerImg, (x, y))

# Change state of player bullet and draw to screen
def player_fire(x, y):
    global playerBulletState
    playerBulletState = 'fire'
    screen.blit(playerBulletImg, (x, y))

def player_reset():
    global playerState, playerSpeed, playerBulletState
    playerRect.centerx = sWidth / 2
    playerRect.centery = sHeight - 100
    playerState = 'alive'
    playerSpeed = 4
    playerBulletState = 'ready'

# Draw enemy icons at x, y coords
def enemy(c, x, y):
    global enemyState
    if enemyState[c] == 'alive':
        screen.blit(enemyImg[c], (x, y))

# Change state of enemy bullet and draw to screen
def enemy_fire(c, x, y):
    global enemyBulletState
    enemyBulletState[c] = 'fire'
    screen.blit(enemyBulletImg[c], (x, y))

def enemy_reset():
    global enemyDirection, enemyChangeX
    enemyType.clear()
    enemyImg.clear()
    enemyRect.clear()
    enemyState.clear()
    enemyBulletImg.clear()
    enemyBulletRect.clear()
    enemyBulletState.clear()
    if enemyDirection == 'left':
        enemyChangeX = -enemyChangeX
        enemyDirection = 'right'

def load_enemies(rows, cols):
    for _i in range(rows):
        for _j in range(cols):
            _r = random.randint(1, 5)
            if _r == 1:
                enemyType.append('rare')
                enemyImg.append(pygame.image.load('ufo-rare.png'))
                enemyBulletImg.append(pygame.image.load('bullet-rare.png'))
            else:
                enemyType.append('norm')
                enemyImg.append(pygame.image.load('ufo-norm.png'))
                enemyBulletImg.append(pygame.image.load('bullet-norm.png'))
            enemyRect.append(pygame.Rect(enemyStartX + (100 * _j), enemyStartY + (100 * _i), 64, 64))
            enemyState.append('alive')
            enemyBulletRect.append(pygame.Rect(enemyStartX + (100 * _j), enemyStartY + (100 * _i), 10, 31))
            enemyBulletState.append('ready')

def next_level():
    global level, enemyRows, enemyChangeX, enemyBulletFreq
    level += 1
    enemy_reset()
    if level % 5 == 0:
        enemyRows += 1
        enemyBulletFreq = 1000
        enemyChangeX = 2
    elif level % 2 == 0:
        enemyBulletFreq -= 250
    else:
        enemyChangeX += 0.5

    load_enemies(enemyRows, enemyCols)

def new_game():
    global scoreValue, level, enemyBulletFreq, enemyChangeX
    player_reset()
    enemy_reset()
    enemyBulletFreq = 1000
    enemyChangeX = 2
    scoreValue = 0
    level = 1
    load_enemies(1, 10)
    mixer.music.load('Main.mp3')
    mixer.music.play(-1)

# Game loop
running = True
while running:

    # Calculate time delta
    clock.tick(fps)
    now = time.time()
    dt = now - prev
    prev = now

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Pygame events
    for event in pygame.event.get():

        # Functionality for red close button
        if event.type == pygame.QUIT:
            running = False

        # Player controls
        keyState = pygame.key.get_pressed()
        if keyState[ord('a')] and keyState[ord('d')]:
            playerChangeX = 0
        elif keyState[ord('a')] and playerRect.x > 0:
            playerChangeX = -playerSpeed
        elif keyState[ord('d')] and playerRect.x < sWidth - 64:
            playerChangeX = playerSpeed
        if keyState[ord('w')] and keyState[ord('s')]:
            playerChangeY = 0
        elif keyState[ord('w')] and playerRect.y > 0:
            playerChangeY = -playerSpeed
        elif keyState[ord('s')] and playerRect.y < sHeight - 77:
            playerChangeY = playerSpeed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if playerBulletState == 'ready' and playerState == 'alive':
                    playerBulletRect.x = playerRect.x + 27
                    playerBulletRect.y = playerRect.y - 20
                    player_fire(playerBulletRect.x, playerBulletRect.y)
                    fire.play()
            elif event.key == pygame.K_RETURN:
                if mode == 'title':
                    player_reset()
                    mode = 'play'
                elif mode == 'over':
                    new_game()
                    mode = 'play'
            elif event.key == pygame.K_ESCAPE:
                if mode == 'title' or mode == 'over':
                    running = False

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_a and not keyState[ord('d')]) or (event.key == pygame.K_d and not keyState[ord('a')]):
                playerChangeX = 0
            elif (event.key == pygame.K_w and not keyState[ord('s')]) or (event.key == pygame.K_s and not keyState[ord('w')]):
                playerChangeY = 0

    # Player speed, multiplied by delta time for frame independence
    playerRect.x += playerChangeX * dt * target
    playerRect.y += playerChangeY * dt * target

    # Screen boundaries
    if playerRect.x < 0 or playerRect.x > sWidth - 64:
        playerChangeX = 0
    if playerRect.y < 0 or playerRect.y > sHeight - 77:
        playerChangeY = 0

    player(playerRect.x, playerRect.y)

    # Player bullet movement
    if playerBulletRect.y <= 0:
        playerBulletRect.x = playerRect.x
        playerBulletRect.y = playerRect.y
        playerBulletState = 'ready'
    if playerBulletState == 'fire':
        player_fire(playerBulletRect.x, playerBulletRect.y)
        playerBulletRect.y -= playerBulletChangeY * dt * target
    elif playerBulletState == 'ready':
        playerBulletRect.x = playerRect.x
        playerBulletRect.y = playerRect.y

    if mode == 'title':
        display_title()
    elif mode == 'play':
        # Enemy movement
        enemyCount = len(enemyImg)
        for i in range(enemyCount):
            if enemyRect[i].y >= sHeight - 50:
                mode = 'over'
                break
            while enemyRect[i].x <= 0 and enemyDirection == 'left':
                for j in range(enemyCount):
                    enemyRect[j].y += enemyChangeY
                enemyChangeX = -enemyChangeX
                enemyDirection = 'right'
            while enemyRect[i].x >= sWidth - 64 and enemyDirection == 'right':
                for j in range(enemyCount):
                    enemyRect[j].y += enemyChangeY
                enemyChangeX = -enemyChangeX
                enemyDirection = 'left'
            enemyRect[i].x += enemyChangeX * dt * target
            enemy(i, enemyRect[i].x, enemyRect[i].y)

            # Enemy bullets
            r = random.randint(1, enemyBulletFreq)
            if enemyType[i] == 'norm' and enemyState[i] == 'alive' and r in range(1, 5):
                if enemyBulletState[i] == 'ready':
                    enemyBulletRect[i].x = enemyRect[i].x + 27
                    enemyBulletRect[i].y = enemyRect[i].y + 50
                    enemy_fire(i, enemyBulletRect[i].x, enemyBulletRect[i].y)
            elif enemyType[i] == 'rare' and enemyState[i] == 'alive' and r in range(1, 10):
                if enemyBulletState[i] == 'ready':
                    enemyBulletRect[i].x = enemyRect[i].x + 27
                    enemyBulletRect[i].y = enemyRect[i].y + 50
                    enemy_fire(i, enemyBulletRect[i].x, enemyBulletRect[i].y)
            elif enemyState[i] == 'alive' and enemyBulletState[i] == 'ready':
                enemyBulletRect[i].x = enemyRect[i].x
                enemyBulletRect[i].y = enemyRect[i].y

            if enemyBulletRect[i].y >= sHeight:
                enemyBulletRect[i].x = enemyRect[i].x
                enemyBulletRect[i].y = enemyRect[i].y
                enemyBulletState[i] = 'ready'
            if enemyBulletState[i] == 'fire':
                enemy_fire(i, enemyBulletRect[i].x, enemyBulletRect[i].y)
                if enemyType[i] == 'norm':
                    enemyBulletRect[i].y += enemyBulletNormChangeY * dt * target
                elif enemyType[i] == 'rare':
                    enemyBulletRect[i].y += enemyBulletRareChangeY * dt * target

        # Collisions
        for i in range(enemyCount):
            # Player collides with enemy
            if playerRect.colliderect(enemyRect[i]) and playerState == 'alive' and enemyState[i] == 'alive':
                mode = 'over'
                playerDown.play()
                mixer.music.stop()
                mixer.music.load('Game Over.mp3')
                mixer.music.play()
                playerBulletRect.x = playerRect.x
                playerBulletRect.y = playerRect.y
                playerBulletState = 'ready'
                break
            # Player bullet collides with enemy
            if playerBulletRect.colliderect(enemyRect[i]) and playerState == 'alive' and enemyState[i] == 'alive':
                enemyDown.play()
                playerBulletRect.x = playerRect.x
                playerBulletRect.y = playerRect.y
                playerBulletState = 'ready'
                if enemyType[i] == 'norm':
                    scoreValue += 100
                elif enemyType[i] == 'rare':
                    scoreValue += 300
                enemyState[i] = 'dead'
            # Player collides with enemy bullet
            if playerRect.colliderect(enemyBulletRect[i]) and playerState == 'alive':
                mode = 'over'
                playerDown.play()
                mixer.music.stop()
                mixer.music.load('Game Over.mp3')
                mixer.music.play()
                playerBulletRect.x = playerRect.x
                playerBulletRect.y = playerRect.y
                playerBulletState = 'ready'
                enemyBulletRect[i].x = enemyRect[i].x
                enemyBulletRect[i].y = enemyRect[i].y
                break

        if 'alive' not in enemyState:
            next_level()

        display_score()
        display_level()
    elif mode == 'over':
        game_over()
        display_score()
        display_level()

    pygame.display.update()
