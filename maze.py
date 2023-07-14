
# OUTLINE BEGIN

# A small script to generate some mazes

# TODO
# - █▯▓▯▒▯░▯ ▯▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█
# - ╶╺╵└┕╹┖┗╴─╼┘┴┶┚┸┺╸╾━┙┵┷┛┹┻╷┌┍│├┝╿┞┡┐┬┮┤┼┾┦╀╄┑┭┯┥┽┿┩╃╇╻┎┏╽┟┢┃┠┣┒┰┲┧╁╆┨╂╊┓┱┳┪╅╈┫╉╋

# OUTLINE END


# IMPORTS BEGIN

import random
import pprint

# IMPORTS END


# CLASSES BEGIN

class Maze:
    """A class to store and interact with a maze grid."""

    # Direction constants/flags
    RIGHT = 0b0001
    UP    = 0b0010
    LEFT  = 0b0100
    DOWN  = 0b1000

    def __init__(self, width_, height_):
        assert(width_ > 0 and height_ > 0)
        self.width  = width_
        self.height = height_
        self.grid = [[random.randint(0b0000,0b1111) for _ in range(width_)] for _ in range(height_)]

    def __repr__(self):
        return pprint.pformat(self.grid)

    def __format__(self, *args):
        if args[0] == '':
            return self.ascii_thin()
        else:
            return self.ascii_str(wall=args[0])

    def ascii_thin(self):
        """
        Produce a compact ASCII representation.
        """
        """
            ,___, ,___, ,___, ,___,
            |   | | __| | | | | |_|
            |___| |___| |___| |___|
            ,___, ,___, ,___, ,___,
            |__ | |___| |_| | |_|_|
            |___| |___| |___| |___|
            ,___, ,___, ,___, ,___,
            | , | | ,_| | | | | |_|
            |_|_| |_|_| |_|_| |_|_|
            ,___, ,___, ,___, ,___,
            |_, | |___| |_| | |_|_|
            |_|_| |_|_| |_|_| |_|_|
        """
        def wall(x, y, direction):
            return not self.edge_toward((x,y),direction)
        def cornersegment_top_left():
            if wall(0,0,self.LEFT): return ','
            elif wall(0,0,self.UP): return '_'
            else: return '.'
        def cornersegment_top(x):
            if wall(x,0,self.RIGHT) and not (wall(x,0,self.UP) and x<self.width-1 and wall(x+1,0,self.UP)): return ','
            elif wall(x,0,self.UP) or (x<self.width-1 and wall(x+1,0,self.UP)): return '_'
            else: return '.'
        def cornersegment_left(y):
            if wall(0,y,self.LEFT): return '|'
            elif y!=self.height-1 and wall(0,y+1,self.LEFT): return ','
            elif wall(0,y,self.DOWN): return '_'
            else: return '.'
        def cornersegment(x, y):
            if wall(x,y,self.RIGHT): return '|'
            elif y<self.height-1 and wall(x,y+1,self.RIGHT) and not (wall(x,y,self.DOWN) and x<self.width-1 and wall(x+1,y,self.DOWN)): return ','
            elif wall(x,y,self.DOWN) or (x<self.width-1 and wall(x+1,y,self.DOWN)): return '_'
            else: return '.'
        # Top-left corner
        string = cornersegment_top_left()
        # Top wall
        for x,node in enumerate(self.grid[0]):
            string += '_' if wall(x,0,self.UP) else ' '
            string += cornersegment_top(x)
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            string += f"\n{cornersegment_left(y)}"
            # Middle and right walls (2 chars/node)
            for x,node in enumerate(row):
                string += '_' if wall(x,y,self.DOWN) else ' '
                string += cornersegment(x, y)
        return string

    def ascii_str(self, wall=None, air=None):
        """Produce a 'block' ASCII representation of the maze."""
        if wall is None: wall = '%#'
        if air is None: air = len(wall)*' '
        # Top-left corner
        string = wall
        # Top wall
        for x,node in enumerate(self.grid[0]):
            wall_above = not self.edge_toward((x,0),self.UP)
            string += f"{wall if wall_above else air}{wall}"
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            wall_left = not self.edge_toward((0,y),self.LEFT)
            string += f"\n{wall if wall_left else air}"
            strbelow = f"\n{wall}"
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                wall_right = not self.edge_toward((x,y),self.RIGHT)
                wall_below = not self.edge_toward((x,y),self.DOWN)
                string += f"{air}{wall if wall_right else air}"
                strbelow += f"{wall if wall_below else air}{wall}"
            string += strbelow
        return string

    def edge_toward(self, node_coordinate, direction): # TODO bad idea?..
        """Check whether there is an edge from a specified node into some direction.
        - node_coordinate : (x,y) where 0<=x<width && 0<=y<height
        - direction : one of self.{RIGHT,UP,LEFT,DOWN}"""
        (x,y) = node_coordinate
        return bool(self.grid[y][x] & direction)


# CLASSES END


# FUNCTIONS BEGIN


# FUNCTIONS END


# MAIN BEGIN

def main():
    maze = Maze(10,10)
    print(maze)
    print(f"{maze}")
    #print(f"{maze:@#}")
    print(f"{maze:██}")

if __name__=="__main__": main()

# MAIN END
