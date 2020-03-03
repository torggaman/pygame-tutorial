from pygame import init, display, mixer, font, draw, event, QUIT, KEYUP, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
from pygame_test_game import collision, config, game_object
from random import randint

# Initialize pygame
init()

screen = display.set_mode((config.screen_width, config.screen_height))

# Background
# background = pygame.image.load('background.png')

# Title and Icon
display.set_caption("Test Game")
# icon = pygame.image.load('icon.png')
# pygame.display.set_icon(icon)


# Text
text_font = font.Font('freesansbold.ttf', 32)
end_text = font.Font('freesansbold.ttf', 64)

# Sound
# mixer.music.load('FILENEEDED.wav')
# mixer.music.play(-1)

# Game Loop
running = True
game_over = False
win = False

# Player
Player = game_object.GameObject(0, 370, 480, 370, 480, 0, 0, 0.5, 0.5, 32, 32, 32)

# Bullet
Bullet = game_object.GameObject(0, config.screen_width, config.screen_height, config.screen_width, config.screen_height, 0, .6, 0, .6, 8, 8, 8, '', 'ready')

# Enemy
enemies = [game_object.GameObject(i, 0, 0, randint(5, config.screen_width - 69), randint(40, 140), config.enemy_speed, config.enemy_y_speed, config.enemy_speed, config.enemy_y_speed, config.enemy_size, config.enemy_size, config.enemy_size) for i in range(config.num_of_enemies)]

# Score
score_value = 0


def show_score(x, y):
    score = text_font.render('Score: ' + str(score_value), True, config.white)
    screen.blit(score, (x, y))


def show_level(x, y):
    level = text_font.render('Level: ' + str(config.current_level), True, config.white)
    screen.blit(level, (x, y))


def show_weapon_state(x, y):
    state = text_font.render('Weapon: ' + Bullet.get_state().capitalize(), True, config.white)
    screen.blit(state, (x, y))


def destroy_enemy(i):
    global enemies
    # exploding_sound = mixer.Sound('exploding.wav')
    # exploding_sound.play()
    enemies[i].set_x_position(randint(5, config.screen_width - 69))
    enemies[i].set_y_position(randint(40, 140))


def fire_bullet():
    global Bullet, Player
    # bullet_sound = mixer.Sound('laser.wav')
    # bullet_sound.play()
    Bullet.set_state('fire')
    Bullet.set_x_position(Player.get_x_position() + (Player.get_size()/3))
    Bullet.set_y_position(Player.get_y_position() - 10)
    Bullet.draw_object(screen, config.green, Bullet.get_x_position(), Bullet.get_y_position())


def destroy_bullet():
    global Bullet
    Bullet.set_x_position(config.screen_width)
    Bullet.set_y_position(config.screen_height)
    Bullet.set_state("ready")


def reset_level():
    global enemies
    config.current_level += 1
    if not config.num_of_enemies >= config.max_num_of_enemies:
        config.num_of_enemies += 1
    config.enemy_size -= 1
    config.enemy_speed += 0.1
    config.enemy_y_speed += 4
    enemies = [game_object.GameObject(i, 0, 0, randint(5, config.screen_width - 69), randint(40, 140), config.enemy_speed, config.enemy_y_speed, config.enemy_speed, config.enemy_y_speed, config.enemy_size, config.enemy_size, config.enemy_size) for i in range(config.num_of_enemies)]
    Player.set_x_position(Player.get_default_x())
    Player.set_y_position(Player.get_default_y())


def win_screen():
    over_text = end_text.render("YOU WIN", True, config.white)
    screen.blit(over_text, (200, 250))


def end_screen():
    over_text = end_text.render("GAME OVER", True, config.white)
    screen.blit(over_text, (200, 250))


while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
        if events.type == KEYDOWN:
            if events.key == K_LEFT:
                Player.set_x_change(-Player.get_x_speed())
            if events.key == K_RIGHT:
                Player.set_x_change(Player.get_x_speed())
            # if events.key == K_UP:
            #     playerY_change = -player_movement_y
            # if events.key == K_DOWN:
            #     playerY_change = player_movement_y
            if events.key == K_SPACE:
                if Bullet.get_state() != "fire":
                    fire_bullet()
        if events.type == KEYUP:
            if events.key == K_UP or events.key == K_DOWN:
                Player.set_y_change(0)
            if events.key == K_LEFT or events.key == K_RIGHT:
                Player.set_x_change(0)

    # Update the screen

    # Background
    screen.fill(config.black)

    # Check Player movement for outside of screen
    Player.set_x_change(collision.check_x_boundry(Player.x_position, Player.x_change))
    Player.set_y_change(collision.check_y_boundry(Player.y_position, Player.y_change))

    # Player movement
    Player.set_x_position(Player.x_position + Player.x_change)
    # playerY += playerY_change

    # Enemy Movement
    if game_over is not True or win is not True:
        for i in range(config.num_of_enemies):
            if enemies[i].get_y_position() >= 460 and win is not True:
                for j in range(config.num_of_enemies):
                    enemies[j] .set_y_position(1000)
                game_over = True
                break
            elif config.current_level == config.win_level:
                for j in range(config.num_of_enemies):
                    enemies[i].set_y_position(1000)
                win = True
                break
            elif score_value >= config.current_level * config.win_score:
                reset_level()
            enemies[i].set_x_position(enemies[i].get_x_position() + enemies[i].get_x_change())
            if enemies[i].get_x_position() <= 0:
                enemies[i].set_x_change(enemies[i].get_x_speed())
                enemies[i].set_y_position(enemies[i].get_y_position() + enemies[i].get_y_change())

            if enemies[i].get_x_position() >= config.screen_width - 64:
                enemies[i].set_x_change(-enemies[i].get_x_speed())
                enemies[i].set_y_position(enemies[i].get_y_position() + enemies[i].get_y_change())

            # Collision
            if collision.check_collision(Bullet.get_x_position(), Bullet.get_y_position(), enemies[i].get_x_position(), enemies[i].get_y_position()):
                destroy_bullet()
                destroy_enemy(i)
                score_value += 1

            if collision.check_collision(Player.x_position, Player.y_position, enemies[i].get_x_position(), enemies[i].get_y_position()):
                Player.object_reset()
                score_value = 0

            # Enemies
            enemies[i].draw_object(screen, config.red, enemies[i].get_x_position(), enemies[i].get_y_position())

        # Bullet Movement
        if Bullet.get_state() == "fire":
            Bullet.set_y_position(Bullet.get_y_position() + -Bullet.get_y_speed())
            Bullet.draw_object(screen, config.green, Bullet.get_x_position(), Bullet.get_y_position())
            if collision.check_y_boundry(Bullet.get_y_position(), Bullet.get_y_speed()) == 0:
                destroy_bullet()

        # Player
        Player.draw_object(screen, config.blue, Player.get_x_position(), Player.get_y_position())

    if game_over:
        end_screen()
    elif win:
        win_screen()

    # Score
    show_score(config.textX, config.textY)
    show_level(config.screen_width-150, config.textY)
    show_weapon_state(config.textX, config.screen_height - 40)

    # Update
    display.update()
