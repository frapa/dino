from math import sqrt
from .. import vector

class Rect(object):
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def __getattr__(self, attr_name):
        if attr_name == "right":
            return self.left + self.width
        elif attr_name == "bottom":
            return self.top + self.height
        elif attr_name == "center_x":
            return self.left + self.width / 2
        elif attr_name == "center_y":
            return self.top + self.height / 2

    def collide(self, other):
        if not (self.bottom < other.top or
                self.top > other.bottom or
                self.left > other.right or
                self.right < other.left):
            return True
        else:
            return False

    def __repr__(self):
        return "Rect({}, {}, {}, {})".format(self.left, self.top, self.width, self.height)

    def collide_point(self, x, y):
        if self.left < x < self.right and self.top < y < self.bottom:
            return True
        else:
            return False

    def distance(self, other):
        return sqrt((self.center_x - other.center_x)**2 + (self.center_y - other.center_y)**2)

    def get_penetration_y(self, other):
        sep_y = abs(other.center_y - self.center_y)

        penetration = 0

        if sep_y < (other.height + self.height) / 2:
            penetration = abs((other.height + self.height) / 2 - sep_y)

        return penetration

    def get_penetration_x(self, other):
        sep_x = abs(other.center_x - self.center_x)

        penetration = 0

        if sep_x < (other.width + self.width) / 2:
            penetration = abs((other.width + self.width) / 2 - sep_x)

        return penetration

    def get_penetration(self, other):
        return [self.get_penetration_x(other), self.get_penetration_y(other)]

    def grow(self, d):
        return Rect(self.left - d, self.top - d, self.width + 2*d, self.height + 2*d)

    def get_gl_points(self):
        return (self.left, self.top, self.right, self.top,
            self.right, self.bottom, self.left, self.bottom)

    def move(self, x, y):
        self.left += x
        self.top += y

    def move_vec(self, vector):
        self.left += vector.coordinates[0]
        self.top += vector.coordinates[1]
