
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

    #def __format__(self, *args):
        #if args[0] == '':
            #return self.ascii_thin()
        #else:
            #return self.ascii_block(wall=args[0])

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
        Keyword arguments `wall`/`air` may also be functions that produce random texture instead of a fixed string.
        """
        # Sort out non-/default wall/air texture,
        if wall is None: make_wall = lambda: '##'
        elif callable(wall): make_wall = wall
        else: make_wall = lambda: wall
        if air is None: make_air = lambda: ' '*len(make_wall())
        elif callable(air): make_air = air
        else: make_air = lambda: air
        # Actually produce string using default maze bitmap
        bmap = self.bitmap(columnated=True)
        string = '\n'.join(''.join(make_wall() if b else make_air() for b in row) for row in bmap)
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

    def utf_block(self):
        """
        Produce blocky unicode art to represent the maze.
        """
        return self.ascii_block(wall='██',air='  ')

    def utf_half(self):
        """
        Produce blocky unicode art to represent the maze, at half the size.
        """
        tiles = " ▄▀█"
        bmap = self.bitmap(columnated=True)
        if len(bmap)%2!=0:
            bmap.append([False for _ in bmap[0]])
        string = ""
        for y in range(0,len(bmap),2):
            string += '\n'
            string += ''.join(tiles[2*hi + 1*lo] for (hi,lo) in zip(bmap[y],bmap[y+1]))
        return string

    def utf_quarter(self):
        """
        Produce blocky unicode art to represent the maze, at quarter the size.
        """
        #tiles = " ▯▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█"
        tiles = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
        bmap = self.bitmap(columnated=True)
        if len(bmap)%2!=0:
            bmap.append([False for _ in bmap[0]])
        if len(bmap[0])%2!=0:
            for row in bmap: row.append(False)
        string = ""
        for y in range(0,len(bmap),2):
            string += '\n'
            for x in range(0,len(bmap[0]),2):
                string += tiles[8*bmap[y+1][x+1] + 4*bmap[y+1][x] + 2*bmap[y][x+1] + 1*bmap[y][x]]
        return string

    def utf_pipe(self):
        """
        Produce pipe-like unicode art to represent the maze.
        """
        tiles = " ╶╺╵└┕╹┖┗╴─╼┘┴┶┚┸┺╸╾━┙┵┷┛┹┻╷┌┍│├┝╿┞┡┐┬┮┤┼┾┦╀╄┑┭┯┥┽┿┩╃╇╻┎┏╽┟┢┃┠┣┒┰┲┧╁╆┨╂╊┓┱┳┪╅╈┫╉╋"
        get_tile = lambda a,b,c,d: tiles[27*d + 9*c + 3*b + 1*a]
        string = ""
        for y,row in enumerate(self.grid):
            string  += "\n"
            strbelow = "\n"
            for x,node in enumerate(row):
                [r,u,l,d] = [self.has_wall(x,y,dir) for dir in self.DIRECTIONS]
                [nr,nu,nl,nd] = [not val for val in (r,u,l,d)]
                string += (get_tile(u,nu,nl,l) + 2*get_tile(u,0,u,0) + get_tile(nr,nu,u,r))
                strbelow += get_tile(d,l,nl,nd) + 2*get_tile(d,0,d,0) + get_tile(nr,r,d,nd)
            string += strbelow
        return string

    #def utf_thin(self):
        #"""
        #Produce a 'compact' unicode representation.
        #"""
        #tiles = " ╶╵└╴─┘┴╷┌│├┐┬┤┼"
        #string = tiles[]

    def utf_network(self):
        """
        Display the node connections in the maze.
        """
        tiles = " ╶╵└╴─┘┴╷┌│├┐┬┤┼"
        #get_tile = lambda n: tiles[n]+tiles[5*(n%2)]
        get_tile = lambda n: tiles[n]
        return '\n'.join(''.join(get_tile(node) for node in row) for row in self.grid)

    def edge_toward(self, node_coordinate, direction): # TODO bad idea?..
        """
        Check whether there is an edge from a specified node into some direction.
        - node_coordinate : (x,y) where 0<=x<width && 0<=y<height
        - direction : one of self.DIRECTIONS
        """
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
    print(f"repr:\n{repr(maze)}")
    print(f"ascii_block:\n{maze.ascii_block(wall=lambda:random.choice(['##','#@','%#']))}")
    print(f"ascii_thin:\n{maze.ascii_thin()}")
    print(f"utf_block:\n{maze.utf_block()}")
    print(f"utf_half:\n{maze.utf_half()}")
    print(f"utf_quarter:\n{maze.utf_quarter()}")
    print(f"utf_pipe:\n{maze.utf_pipe()}")
    print(f"utf_network:\n{maze.utf_network()}")

    #help(Maze)

if __name__=="__main__": main()

# MAIN END
