from math import sqrt

class Vector(object):
    def __init__(self, *args, **kwargs):
        # check if a list or a tuple was passed
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            self.coordinates = args[0]
        else:
            self.coordinates = args

        # Tribute to Pytagoras.
        self.magnitude = sqrt(sum([c**2 for c in self.coordinates]))

    def get_versor(self):
        """Returns versor which points in the same direction
        as this vector."""

        return self / self.magnitude
            
    def __repr__(self):
        template = "Vector({args})"

        # comma separated coordinates
        cs = ", ".join(map(str, self.coordinates)) 

        return template.format(args=cs)

    def __str__(self):
        template = "<Vector ({coord}) magnitude: {mag:.3f}>"

        # Build template for a comma separated list of coordinates.
        # In this way it is possible to automatically
        # round the values to be displayed for pretty printing.
        coord_temp = ", ".join(["{:.3f}"] * len(self.coordinates))
        # format with coordinates' values
        cs = coord_temp.format(*self.coordinates) 

        return template.format(coord=cs, mag=self.magnitude)

    def __add__(self, vector):
        """Define the sum between 2 vectors."""

        # check if vector is really a Vector
        if not isinstance(vector, Vector):
            return NotImplemented

        pairs = zip(self.coordinates, vector.coordinates)
        new_coord = [sum(pair) for pair in pairs]

        return Vector(*new_coord)

    def __sub__(self, vector):
        return self.__add__(-vector)

    def __mul__(self, scalar):
        """Define a multiplication between a vector and a scalar.
        For cross and dot product use the utility functions."""

        # check if scalar is really a number
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        new_coord = [c * scalar for c in self.coordinates]

        return Vector(*new_coord)

    def __neg__(self):
        return self.__mul__(-1)
    
    def __truediv__(self, scalar):
        """Defines a division between a vector and a scalar.
        A vector cannot be divided by another vector."""

        # check if scalar is really a number
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        if scalar == 0:
            raise ZeroDivisionError()
        else:
            new_coord = [c / scalar for c in self.coordinates]
            
            return Vector(*new_coord)

    def __abs__(self):
        "Return the magnitude of the vector."

        return self.magnitude

    def __eq__(self, vector):
        "Compare two vectors for equality."
        
        # check if vector is really a Vector
        if not isinstance(vector, Vector):
            return NotImplemented

        if vector.coordinates == self.coordinates:
            return True

    def __ne__(self, vector):
        "Compare two vectors for disequality."

        # check if vector is really a Vector
        if not isinstance(vector, Vector):
            return NotImplemented

        if vector.coordinates != self.coordinates:
            return True

    # define some other methods ...
    __div__ = __truediv__
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__
    __rtruediv__ = __truediv__


# Utility fuctions which provide dot ancd cross product operations
# as well as other interesting operations.

def dot(vec1, vec2):
    """Dot product between two vectors."""

    pairs = zip(vec1.coordinates, vec2.coordinates)

    return sum([a * b for a, b in pairs])

def cross(vec1, vec2):
    """Cross product between two vectors"""

    pass

def component(vector, along):
    """Calculates the component of vector along another vector."""

    return dot(vector, along.get_versor())

def distance(vec1, vec2):
    """Compute the distance between 2 points given as vectors."""

    return abs(vec1 - vec2)
