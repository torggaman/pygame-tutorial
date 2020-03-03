from math import sqrt, pow
from pygame_test_game.config import screen_width, screen_height, object_size


def check_x_boundry(positionX, positionX_change):
    if positionX + positionX_change < 0 or positionX + positionX_change > screen_width - object_size:
        return 0
    return positionX_change


def check_y_boundry(positionY, positionY_change):
    if positionY + positionY_change < 0 or positionY + positionY_change > screen_height - object_size:
        return 0
    return positionY_change


def check_collision(x1, y1, x2, y2):
    distance = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    return distance < object_size
