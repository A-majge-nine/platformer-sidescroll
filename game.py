import pygame
from pygame.locals import *
import levels

pygame.init()
window = pygame.display.set_mode((500, 500))
fps = pygame.time.Clock()

scale = 2

def convertGridToPixels (r, offset):
    return  Rect(r[0]*scale - offset[0], r[1]*scale - offset[1], r[2]*scale, r[3]*scale)

font = pygame.font.SysFont("Arial", 24)
fontLarge = pygame.font.SysFont("Arial", 64)
BACKGROUND = (0, 0, 0)
PLAYER = (255, 255, 255)
PLATFORM = (255, 178, 102)
WALL = (128, 128, 128)
COIN = (255, 255, 51)
LAVA = (255, 51, 51)
GOAL = (0, 255, 0)

player = Rect([20, 200, 10, 20])
offset = [0, 25 * scale]
centering = [255, 300]
movingLeft = False
movingRight = False
horizontalSpeed = 5
verticalspeed = 5
jumpHeight = 50
jumpFor = -1
onGround = False
points = 0
health = 10
quit = False
victorious = False

while not quit:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit = True
            if event.key == K_UP:
                if onGround:
                    jumpFor = jumpHeight
            if event.key == K_LEFT:
                movingLeft = True
                movingRight = False
            if event.key == K_RIGHT:
                movingRight = True
                movingLeft = False
        elif event.type == K_SPACE:
            if event.key == K_LEFT:
                movingLeft = False
            if event.key == K_RIGHT:
                movingRight = False

    window.fill(BACKGROUND)

    if movingLeft:
        player.x -= horizontalSpeed
    elif movingRight:
        player.x += horizontalSpeed
    if jumpFor >= 0:
        player.y -= verticalspeed
        jumpFor -= verticalspeed
    elif not onGround and jumpFor < 0:
        player.y += verticalspeed
        pass

    offset[0] = -centering[0] + player.x * scale
    offset[1] = -centering[1] + player.y * scale

    for platform in levels.platforms:
        pygame.draw.rect(window, PLATFORM, convertGridToPixels(platform, offset))

    for lava in levels.firepits:
        pygame.draw.rect(window, LAVA, convertGridToPixels(lava, offset))

    for coin in levels.coins:
        pygame.draw.ellipse(window, COIN, convertGridToPixels(coin, offset))

    for endpoint in levels.goal:
        pygame.draw.rect(window, GOAL, convertGridToPixels(endpoint, offset))

    draw = convertGridToPixels(player, offset)
    pygame.draw.rect(window, PLAYER, draw)

    if player.collidelist(levels.platforms) > -1:
        if not onGround and jumpFor < 0:
            onGround = True
            jumpFor = -1
    else:
        onGround = False

    if player.collidelist(levels.firepits) >-1:
        onGround = True
        health = health - 1

    if player.collidelist(levels.walls) > -1:
        if movingLeft:
            movingLeft = False
            movingRight = True
        elif movingRight:
            movingRight = False
            movingLeft = True

    coinNumber = player.collidelist(levels.coins)
    if coinNumber >= 0:
        points = points + 1
        del levels.coins[coinNumber]

    if player.collidelist(levels.goal) > -1:
        victorious = True

    if health <= 0:
        quit = True

    pointsText = font.render(str(points), 1, (0, 255, 0))
    healthText = font.render(str(health), 1, (255, 128, 0))
    window.blit(pointsText, (20, 20))
    window.blit(healthText, (20, 50))

    pygame.display.update()
    fps.tick(20)

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                waiting = False
    message = fontLarge.render("Goodbye :-(", 1, (128, 128, 255))
    if health <= 0:
        message = fontLarge.render("Sorry, you died.", 1, (255, 0, 0))
    elif victorious:
        message = fontLarge.render("Congratulations!", 1, (0, 255, 0))
    window.blit(message, (20, 220))
    message = font.render("You collected "+str(points)+" coins", 1, (255, 255, 255))
    window.blit(message, (20, 320))
    pygame.display.update()
    fps.tick(20)

pygame.quit()
