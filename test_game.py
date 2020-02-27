from pygame import init, display, mixer, font, draw, event, QUIT, KEYUP, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
from random import randint
from math import sqrt, pow

# Initialize pygame
init()

# Create the screen
screen_width = 800
screen_height = 600
screen = display.set_mode((screen_width, screen_height))

# Background
# background = pygame.image.load('background.png')

black = 0, 0, 0
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
white = 255, 255, 255

# Sound
# mixer.music.load('FILENEEDED.wav')
# mixer.music.play(-1)

# Title and Icon
display.set_caption("Test Game")
# icon = pygame.image.load('icon.png')
# pygame.display.set_icon(icon)

# Score
score_value = 0
text_font = font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
win_score = 10

end_text = font.Font('freesansbold.ttf', 64)

# Player
# playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 480
# playerImage =
player_movement_x = 0.5
player_movement_y = 0.5
playerX_change = 0
playerY_change = 0
player_size = 32

# Enemy
enemyX = []
enemyY = []
enemyX_change = []
enemy_movement_x = []
enemyY_change = []
enemy_movement_y = []
enemy_size = 32
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyX.append(randint(5, screen_width - 69))
    enemyY.append(randint(0, 100))
    enemyX_change.append(0.4)
    enemy_movement_x.append(0.4)
    enemyY_change.append(40)
    enemy_movement_y.append(40)

# Bullet
bulletX = screen_width
bulletY = screen_height
bulletY_change = 0
bullet_movement_y = 0.2
bullet_size = player_size/4
bullet_state = "ready"


def show_score(x, y):
    score = text_font.render('Score: ' + str(score_value), True, white)
    screen.blit(score, (x, y))

def check_x_boundry(positionX, positionX_change):
    if positionX + positionX_change < 0 or positionX + positionX_change > screen_width - 64:
        return 0
    return positionX_change


def check_y_boundry(positionY, positionY_change):
    if positionY + positionY_change < 0 or positionY + positionY_change > screen_height - 64:
        return 0
    return positionY_change


def player(x, y):
    draw.rect(screen, blue, (x, y, player_size, player_size), 0)


def enemy(x, y):
    draw.rect(screen, red, (x, y, enemy_size, enemy_size), 0)


def destroy_enemy(i):
    global enemyX, enemyY
    # exploding_sound = mixer.Sound('exploding.wav')
    # exploding_sound.play()
    enemyX[i] = randint(5, screen_width - 69)
    enemyY[i] = randint(0, 100)


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # bullet_sound = mixer.Sound('laser.wav')
    # bullet_sound.play()
    draw.rect(screen, green, (x, y, bullet_size, bullet_size), 0)


def bullet(x, y):
    draw.rect(screen, green, (x, y, bullet_size, bullet_size), 0)


def destroy_bullet():
    global bulletX, bulletY, bullet_state
    bulletX = screen_width
    bulletY = screen_height
    bullet_state = "ready"


def check_collision(x1, y1, x2, y2):
    distance = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    return distance < enemy_size


# Game Loop
running = True
game_over = False
win = False


def win_screen():
    over_text = end_text.render("YOU WIN", True, white)
    screen.blit(over_text, (200, 250))


def end_screen():
    over_text = end_text.render("GAME OVER", True, white)
    screen.blit(over_text, (200, 250))


while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
        if events.type == KEYDOWN:
            if events.key == K_LEFT:
                playerX_change = -player_movement_x
            if events.key == K_RIGHT:
                playerX_change = player_movement_x
            # if events.key == K_UP:
            #     playerY_change = -player_movement_y
            # if events.key == K_DOWN:
            #     playerY_change = player_movement_y
            if events.key == K_SPACE:
                if bullet_state != "fire":
                    bulletX = playerX + (player_size/3)
                    bulletY = playerY - 10
                    fire_bullet(bulletX, bulletY)
        if events.type == KEYUP:
            if events.key == K_UP or events.key == K_DOWN:
                playerY_change = 0
            if events.key == K_LEFT or events.key == K_RIGHT:
                playerX_change = 0

    # Update the screen

    # Background
    screen.fill(black)

    # Check Player movement for outside of screen
    playerX_change = check_x_boundry(playerX, playerX_change)
    playerY_change = check_y_boundry(playerY, playerY_change)

    # Player movement
    playerX += playerX_change
    playerY += playerY_change

    # Enemy Movement
    if game_over is not True or win is not True:
        for i in range(num_of_enemies):
            if enemyY[i] >= 470 and win is not True:
                for j in range(num_of_enemies):
                    enemyY[j] = 1000
                game_over = True
                break
            elif score_value >= win_score:
                for j in range(num_of_enemies):
                    enemyY[j] = 1000
                win = True
                break
            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = enemy_movement_x[i]
                enemyY[i] += enemyY_change[i]

            if enemyX[i] >= screen_width - 64:
                enemyX_change[i] = -enemy_movement_x[i]
                enemyY[i] += enemyY_change[i]

            # Collision
            if check_collision(bulletX, bulletY, enemyX[i], enemyY[i]):
                destroy_bullet()
                destroy_enemy(i)
                score_value += 1

            if check_collision(playerX, playerY, enemyX[i], enemyY[i]):
                playerX = 370
                playerY = 480
                score_value = 0

            if bullet_state == "fire":
                bullet(bulletX, bulletY)
                bulletY -= bullet_movement_y
                if check_y_boundry(bulletY, bullet_movement_y) == 0:
                    destroy_bullet()

            # Player
            player(playerX, playerY)

            # Enemy
            for i in range(num_of_enemies):
                enemy(enemyX[i], enemyY[i])

    if game_over is True:
        end_screen()
    elif win is True:
        win_screen()

    # Score
    show_score(textX, textY)

    # Update
    display.update()
