
# OUTlINE BEGIN


# OUTINE END


# IMPORTS BEGIN


# IMPORTS END


# CLASSES BEGIN

class Maze:
    """A class to store and interact with a maze grid."""

    # Direction Masks
    RIGHT,UP,LEFT,DOWN = 0b0001,0b0010,0b0100,0b1000

    def __init__(self, width, height):
        assert(width > 0 and height > 0)
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def edge_toward(self, node_coordinate, direction): # TODO bad idea?..
        (x,y) = node_coordinate
        return self.grid[y][x] & direction
#,_,
#|_|

#,_________,
#| , | ,__ |
#| | __| __|
#| |___|_| |
#|_________|

# CLASSES END


# FUNCTIONS BEGIN


# FUNCTIONS END


# MAIN BEGIN

def main():
    maze = Maze(10,10)

if __name__=="__main__": main()

# MAIN END
