from pygame import draw


class GameObject:
    def __init__(self, object_id, default_x, default_y, x_position, y_position, x_change, y_change, x_speed, y_speed, width, height, size, image='', state=''):
        self.object_id = object_id
        self.default_x = default_x
        self.default_y = default_y
        self.x_position = x_position
        self.y_position = y_position
        self.x_change = x_change
        self.y_change = y_change
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height
        self.size = size
        self.image = image
        self.state = state
        # self.health = 0
        # self.weapon = ''
        # self.power_up = ''
        # self.facing = 270

    def get_default_x(self):
        return self.default_x

    def set_default_x(self, new_x):
        self.default_x = new_x

    def get_default_y(self):
        return self.default_y

    def set_default_y(self, new_y):
        self.default_y = new_y

    def get_x_position(self):
        return self.x_position

    def set_x_position(self, new_x):
        self.x_position = new_x

    def get_y_position(self):
        return self.y_position

    def set_y_position(self, new_y):
        self.y_position = new_y

    def get_x_change(self):
        return self.x_change

    def set_x_change(self, new_x):
        self.x_change = new_x

    def get_y_change(self):
        return self.y_change

    def set_y_change(self, new_y):
        self.y_change = new_y

    def get_x_speed(self):
        return self.x_speed

    def set_x_speed(self, new_x_speed):
        self.x_speed = new_x_speed

    def get_y_speed(self):
        return self.y_speed

    def set_y_speed(self, new_y_speed):
        self.y_speed = new_y_speed

    def get_width(self):
        return self.width

    def set_width(self, new_width):
        self.width = new_width

    def get_height(self):
        return self.height

    def set_height(self, new_height):
        self.width = new_height

    def get_size(self):
        return self.size

    def set_size(self, new_size):
        self.width = new_size

    def draw_object(self, screen, color, x_position, y_position):
        draw.rect(screen, color, (x_position, y_position, self.size, self.size), 0)

    def object_reset(self):
        self.x_position = self.default_x
        self.y_position = self.default_y

    def get_image(self):
        return self.image

    def set_image(self, new_image):
        self.image = new_image

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    # health = 0
    # weapon = ''
    # power_up = ''
    # facing = 270
