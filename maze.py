
# OUTLINE BEGIN

# A small script to generate some mazes
"""
Work in Progress:
- Carvers:
  * DFS
  * Growing Binary Tree (customizable)
  * Wilson's
  * Kruskal
  * Recursive division
- Printers:
  * utf_thin
  * utf_half: ▀▯▄▯█
  * utf_quarter: ▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█
- ETC Dreams:
  * Maze navigator (w/ curses)
  * Interactive picker: distance by color
  * Doom (curses) █▯▓▯▒▯░
"""

# OUTLINE END


# IMPORTS BEGIN

import random
import pprint

# IMPORTS END


# CLASSES BEGIN

class Maze:
    """
    A class to store and interact with a maze grid.
    """

    # Direction constants/flags
    RIGHT = 0b0001
    UP    = 0b0010
    LEFT  = 0b0100
    DOWN  = 0b1000
    DIRECTIONS = [RIGHT,UP,LEFT,DOWN]

    def __init__(self, width_, height_):
        assert(width_ > 0 and height_ > 0)
        self.width  = width_
        self.height = height_
        self.grid = [[random.randint(0b0000,0b1111) for _ in range(width_)] for _ in range(height_)]

    def __repr__(self):
        return "[" + ',\n'.join(map(repr,self.grid)) + "]"

    def __format__(self, *args):
        if args[0] == '':
            return self.ascii_thin()
        else:
            return self.ascii_block(wall=args[0])

    def bitmap(self, columnated=True):
        has_wall, [RIGHT,UP,LEFT,DOWN] = self.has_wall, self.DIRECTIONS
        wall, air = True, False
        if columnated: column = lambda x,y: True
        else:
            column = lambda x,y: x==self.width-1 or y==self.height-1 or has_wall(x,y,RIGHT) or has_wall(x,y,DOWN) or has_wall(x,y+1,RIGHT) or has_wall(x+1,y,DOWN)
        # Top-left corner
        bmap = [[wall]]
        # Top wall
        for x,node in enumerate(self.grid[0]):
            bmap[0].append(has_wall(x,0,UP))
            bmap[0].append(wall)
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            brow1 = [has_wall(0,y,LEFT)]
            brow2 = [wall]
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                brow1.append(air)
                brow1.append(has_wall(x,y,RIGHT))
                brow2.append(has_wall(x,y,DOWN))
                brow2.append(column(x,y))
            bmap.append(brow1)
            bmap.append(brow2)
        return bmap

    def ascii_block(self, wall=None, air=None):
        """
        Produce a canonical, 'blocky' ASCII representation of the maze.
        """
        if wall is None:
            wall = '%#'
        if air is None:
            air = len(wall)*' '
        bmap = self.bitmap(columnated=True)
        string = '\n'.join(''.join(wall if b else air for b in row) for row in bmap)
        return string

    def ascii_thin(self):
        """
        Produce a 'compact' ASCII representation.
        """
        wall, [RIGHT,UP,LEFT,DOWN] = self.has_wall, self.DIRECTIONS
        # Corner cases are nasty, man
        """ ,___, ,___, ,___, ,___,
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
            |_|_| |_|_| |_|_| |_|_|"""
        def cornersegment_top_left():
            if wall(0,0,LEFT): return ','
            elif wall(0,0,UP): return '_'
            else: return '.'
        def cornersegment_top(x):
            if wall(x,0,RIGHT) and not (wall(x,0,UP) and x<self.width-1 and wall(x+1,0,UP)): return ','
            elif wall(x,0,UP) or (x<self.width-1 and wall(x+1,0,UP)): return '_'
            else: return '.'
        def cornersegment_left(y):
            if wall(0,y,LEFT): return '|'
            elif y!=self.height-1 and wall(0,y+1,LEFT): return ','
            elif wall(0,y,DOWN): return '_'
            else: return '.'
        def cornersegment(x, y):
            if wall(x,y,RIGHT): return '|'
            elif y<self.height-1 and wall(x,y+1,RIGHT) and not (wall(x,y,DOWN) and x<self.width-1 and wall(x+1,y,DOWN)): return ','
            elif wall(x,y,DOWN) or (x<self.width-1 and wall(x+1,y,DOWN)): return '_'
            else: return '.'
        # Top-left corner
        string = cornersegment_top_left()
        # Top wall
        for x,node in enumerate(self.grid[0]):
            string += '_' if wall(x,0,UP) else ' '
            string += cornersegment_top(x)
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            string += f"\n{cornersegment_left(y)}"
            # Middle and right walls (2 chars/node)
            for x,node in enumerate(row):
                string += '_' if wall(x,y,DOWN) else ' '
                string += cornersegment(x,y)
        return string

    def utf_pipe(self):
        """
        Produce pipe-like unicode art to represent the maze.
        """
        tiles = " ╶╺╵└┕╹┖┗╴─╼┘┴┶┚┸┺╸╾━┙┵┷┛┹┻╷┌┍│├┝╿┞┡┐┬┮┤┼┾┦╀╄┑┭┯┥┽┿┩╃╇╻┎┏╽┟┢┃┠┣┒┰┲┧╁╆┨╂╊┓┱┳┪╅╈┫╉╋"
        string = ""
        for y,row in enumerate(self.grid):
            string  += "\n"
            strbelow = "\n"
            for x,node in enumerate(row):
                [r,u,l,d] = [self.has_wall(x,y,dir) for dir in self.DIRECTIONS]
                [nr,nu,nl,nd] = [not val for val in (r,u,l,d)]
                string   += tiles[27*l + 9*nl + 3*nu + 1*u]
                string   += 2*tiles[27*0 + 9*u + 3*0 + 1*u]
                string   += tiles[27*r + 9*u + 3*nu + 1*nr]
                strbelow += tiles[27*nd + 9*nl + 3*l + 1*d]
                strbelow += 2*tiles[27*0 + 9*d + 3*0 + 1*d]
                strbelow += tiles[27*nd + 9*d + 3*r + 1*nr]
            string += strbelow
        return string

    def edge_toward(self, node_coordinate, direction): # TODO bad idea?..
        """Check whether there is an edge from a specified node into some direction.
        - node_coordinate : (x,y) where 0<=x<width && 0<=y<height
        - direction : one of self.DIRECTIONS"""
        (x,y) = node_coordinate
        return bool(self.grid[y][x] & direction)

    def has_wall(self, x, y, direction):
        return not self.edge_toward((x,y), direction)

# CLASSES END


# FUNCTIONS BEGIN

#def carve_binary_tree(maze):
    # TODO

# FUNCTIONS END


# MAIN BEGIN

def main():
    maze = Maze(10,10)
    print("repr : \n" + str(maze))
    print(f"ascii_thin : \n{maze}")
    print(f"ascii_block : \n{maze:██}")
    print(f"utf_pipe : \n{maze.utf_pipe()}")

    #help(Maze)

if __name__=="__main__": main()

# MAIN END
