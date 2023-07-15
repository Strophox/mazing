
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
  * png
- ETC Dreams:
  * Maze navigator (w/ curses)
  * Interactive picker: distance by color
  * Doom (curses) █▯▓▯▒▯░
"""

# OUTLINE END


# IMPORTS BEGIN

import random
import pprint
import itertools

# IMPORTS END


# CONSTANTS BEGIN

# Directions
RIGHT = 0b0001
UP    = 0b0010
LEFT  = 0b0100
DOWN  = 0b1000

# CONSTANTS END


# CLASSES BEGIN

class Node:
    """
    A class to abstract over a grid cell/node.
    """
    def __init__(self):
        self._connectivity = 0

    def __repr__(self):
        return self._connectivity.__repr__()

    def __str__(self):
        return " ╶╵└╴─┘┴╷┌│├┐┬┤┼"[self._connectivity%0b10000]

    def toggle_edge(self, direction):
        """
        Add or remove an edge into some direction.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        self._connectivity ^= direction

    def has_edge(self, direction):
        """
        Check whether there is an edge into some direction.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        return bool(self._connectivity & direction)

class Maze:
    """
    A class to store and interact with a maze grid.
    """
    def __init__(self, width_, height_):
        assert(width_ > 0 and height_ > 0)
        self.width  = width_
        self.height = height_
        self.grid = [[Node() for _ in range(width_)] for _ in range(height_)]

    def __repr__(self):
        return self.grid.__repr__()

    def __str__(self):
        return self.ascii_block(wall='##', air='  ')

    def __iter__(self):
        return itertools.chain(*self.grid)

    def bitmap(self, columnated=True):
        has_wall = self.has_wall
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
        if wall is None: make_wall = lambda: random.choice(['##','#@','%#'])
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
        wall = self.has_wall
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
            string += '\n'
            string += cornersegment_left(y)
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
        make_tile = lambda a,b,c,d: tiles[27*d + 9*c + 3*b + 1*a]
        string = ""
        for y,row in enumerate(self.grid):
            string  += '\n'
            strbelow = "\n"
            for x,node in enumerate(row):
                [r,u,l,d] = [self.has_wall(x,y,dir) for dir in (RIGHT,UP,LEFT,DOWN)]
                [nr,nu,nl,nd] = [not val for val in (r,u,l,d)]
                string += (make_tile(u,nu,nl,l) + 2*make_tile(u,0,u,0) + make_tile(nr,nu,u,r))
                strbelow += make_tile(d,l,nl,nd) + 2*make_tile(d,0,d,0) + make_tile(nr,r,d,nd)
            string += strbelow
        return string

    def utf_thin(self):
        """
        Produce a 'compact' unicode representation.
        """
        wall = self.has_wall
        tiles = " ╶╵└╴─┘┴╷┌│├┐┬┤┼"
        make_tile = lambda a,b,c,d: tiles[8*d + 4*c + 2*b + 1*a]
        # Top-left corner
        string = make_tile(wall(0,0,UP),False,False,wall(0,0,LEFT))
        # Top wall
        for x,node in enumerate(self.grid[0]):
            string += make_tile(x<self.width-1 and wall(x+1,0,UP),False,wall(x,0,UP),wall(x,0,RIGHT))
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            string += '\n'
            string += make_tile(wall(x,y,DOWN),wall(x,y,LEFT),False,y<self.height-1 and wall(x,y+1,LEFT))
            # Middle and right walls (2 chars/node)
            for x,node in enumerate(row):
                string += make_tile(x<self.width-1 and wall(x+1,y,DOWN),wall(x,y,RIGHT),wall(x,y,DOWN),y<self.height-1 and wall(x,y+1,RIGHT))
        return string

    def utf_network(self):
        """
        Display the node connections in the maze.
        """
        return '\n'.join(''.join(str(node) for node in row) for row in self.grid)

    def has_wall(self, x, y, direction):
        """
        Check whether there is a wall in that direction.
        - node_coordinate : (x,y) where 0<=x<width && 0<=y<height
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        return not self.grid[y][x].has_edge(direction)

# CLASSES END


# FUNCTIONS BEGIN

def bogus(maze):
    """
    Carve complete bogus into a maze by essentially randomizing it.
    """
    for node in maze:
        random_directions = random.randint(0b0000,0b1111)
        node.toggle_edge(random_directions)

def depth_first_search(maze):
    stack = [start]
    start.visited = True
    def dfs(node):
        for neighbor in node.neighbors:
            if not neighbor.visited:
                neighbor.visited = True
                node.connectto(neighbor)
                dfs(neighbor)

# FUNCTIONS END


# MAIN BEGIN

def main():
    from textwrap import dedent # removes source code multiline string indents
    main_menu_text = '\n' + dedent(f"""
        Sandbox - fiddle around with mazes
        * [print] current maze (ascii/utf)
        * [resize] maze
        * [carve] new maze
        >
    """).strip()
    printers = [
        repr,
        Maze.ascii_block,
        Maze.ascii_thin,
        Maze.utf_block,
        Maze.utf_half,
        Maze.utf_quarter,
        Maze.utf_pipe,
        Maze.utf_thin,
        Maze.utf_network,
    ]
    carvers = [
        bogus,
        depth_first_search,
    ]
    maze = Maze(10,10)
    while user_input := input(main_menu_text).strip():
        match user_input:
            case "print":
                for p in printers:
                    print(f"{p.__name__}:\n{p(maze)}")
            case "resize":
                try:
                    prompt = "Dimensions X,Y >"
                    maze = Maze(*tuple(map(int, input(prompt).split(','))))
                except:
                    print("<something went wrong>")
            case "carve":
                prompt = f"Choose a carving method:\n| {' | '.join(c.__name__ for c in carvers)}\n>"
                {c.__name__:c for c in carvers}.get(input(prompt), lambda _: print("<carving unsuccessful"))(maze)
            case "sudo":
                try: exec(input())
                except: pass
            case _:
                print("<invalid option>")
    print("Goodbye.")

    #help(Maze)

if __name__=="__main__": main()

# MAIN END
