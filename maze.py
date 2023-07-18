
# OUTLINE BEGIN
"""
This file contains the main `Maze` class, which stores and allows for interaction with a maze.
"""
# OUTLINE END


# IMPORTS BEGIN

import itertools # chain
from PIL import Image

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
    def __init__(self, x, y):
        self.coordinates = (self.x, self.y) = (x, y)
        self.flag = None
        self._connectivity = 0

    def __repr__(self):
        return self._connectivity.__repr__()

    def __str__(self):
        return " ╶╵└╴─┘┴╷┌│├┐┬┤┼"[self._connectivity%0b10000]

    def has_wall(self, direction):
        return not (self._connectivity & direction)

    def has_edge(self, direction):
        """Check whether there is an edge into some direction.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        return self._connectivity & direction

    def set_edges(self, direction):
        """Change connectivity of a node.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        self._connectivity = direction

    def put_edge(self, direction):
        """Add an edge into some direction.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        self._connectivity |= direction

    def toggle_edge(self, direction):
        """Add or remove an edge into some direction.
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        self._connectivity ^= direction

class Maze:
    """
    A class to store and interact with a maze grid.
    """
    def __init__(self, width, height):
        assert(width > 0 and height > 0)
        self.width  = width
        self.height = height
        self.grid = [[Node(x,y) for x in range(width)] for y in range(height)]
        #self.grid = [Node(z%width,z//width) for z in range(width*height)] TODO
        self._infotags = []

    def __repr__(self):
        return self.grid.__repr__() # "["+ ','.join("["+ ','.join(str(n._connectivity) for n in row) +"]" for row in self.grid) + "]"

    def __iter__(self):
        return itertools.chain(*self.grid)

    def from_grid(grid):
        dimensions = (len(grid[0]),len(grid))
        maze = Maze(*dimensions)
        for x in range(maze.height):
            for y in range(maze.width):
                maze.node_at(x,y).set_edges(grid[y][x])
        maze.name = f"maze_{maze.width}x{maze.height}_loaded"
        return maze

    def add_info(self, string):
        self._infotags.append(string)
        return None

    def make_name(self):
        """Set an internal name for the maze object.
        """
        info = '-'.join(self._infotags)
        size = f"{self.width}" if self.width==self.height else f"{self.width}x{self.height}"
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        name = f"maze_{info}_{size}_{timestamp}"
        return name

    def bitmap(self, corridorwidth=1, columnated=True):
        """Return a simple bitmap drawing of the maze.
        - columnated : bool to determine whether to draw free-standing columns in the maze
        - corridorwidth : how wide the corridors should be in relation to the walls
        """
        has_wall, w, (wall,air) = self.has_wall, corridorwidth, (True,False)
        if columnated: column = lambda x,y: True
        else:
            column = lambda x,y: x==self.width-1 or y==self.height-1 or has_wall(x,y,RIGHT) or has_wall(x,y,DOWN) or has_wall(x,y+1,RIGHT) or has_wall(x+1,y,DOWN)
        # Top-left corner
        bmap = [[wall]]
        # Top wall
        for x,node in enumerate(self.grid[0]):
            bmap[0] += [node.has_wall(UP)] * w
            bmap[0] += [wall]
        # Middle and bottom rows of string
        for y,row in enumerate(self.grid):
            # Left wall
            brow1 = [row[0].has_wall(LEFT)]
            brow2 = [wall]
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                brow1 += [air] * w
                brow1 += [node.has_wall(RIGHT)]
                brow2 += [node.has_wall(DOWN)] * w
                brow2 += [column(x,y)]
            bmap += [brow1] * w
            bmap += [brow2]
        return bmap

    def str_bitmap(self, wall=None, air=None, bitmap=None):
        """Produce 'canonical' bitmap string art of the maze.
        Keyword arguments `wall`/`air` may also be functions that produce random texture instead of a fixed string.
        - wall, air : a string (or callable object that produces a string) to be used as wall/air texture
        """
        # Sort out default arguments
        if bitmap is None:
            bitmap = self.bitmap()
        if wall is None:     make_wall = lambda: '#'
        elif callable(wall): make_wall = wall
        else:                make_wall = lambda: wall
        if air is None:     make_air = lambda: ' '*len(make_wall())
        elif callable(air): make_air = air
        else:               make_air = lambda: air
        # Produce actual string
        string = '\n'.join(
            ''.join(
                make_wall() if b else make_air() for b in row
            ) for row in bitmap
        )
        return string

    def str_block_double(self):
        """Produce double-block (unicode) bitmap art of the maze.
        """
        return self.str_bitmap(wall='██',air='  ')

    def str_block(self):
        """Produce full-block (unicode) bitmap art of the maze.
        """
        return self.str_bitmap(wall='█',air=' ')

    def str_block_half(self):
        """Produce half-block (unicode) bitmap art of the maze.
        """
        bmap = self.bitmap()
        # Pad bitmap to even height
        if len(bmap)%2!=0:
            bmap.append([False for _ in bmap[0]])
        # String is just a join of row strings (which are also join)
        tiles = " ▄▀█"
        string = '\n'.join(
            ''.join(
                tiles[2*hi + 1*lo] for (hi,lo) in zip(bmap[y],bmap[y+1])
            ) for y in range(0,len(bmap),2)
        )
        return string

    def str_block_quarter(self):
        """Produce quarter-block (unicode) bitmap art of the maze.
        """
        bmap = self.bitmap()
        # Pad bitmap to even height and width
        if len(bmap)%2!=0:
            bmap.append([False for _ in bmap[0]])
        if len(bmap[0])%2!=0:
            for row in bmap: row.append(False)
        # String is just a join of row strings (which are also join)
        tiles = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█" # ▯▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█
        string = '\n'.join(
            ''.join(
                tiles[8*bmap[y+1][x+1] + 4*bmap[y+1][x] + 2*bmap[y][x+1] + 1*bmap[y][x]] for x in range(0,len(bmap[0]),2)
            ) for y in range(0,len(bmap),2)
        )
        return string

    def str_pipes(self):
        """Produce pipe-like unicode art of the maze.
        """
        tiles = " ╶╺╵└┕╹┖┗╴─╼┘┴┶┚┸┺╸╾━┙┵┷┛┹┻╷┌┍│├┝╿┞┡┐┬┮┤┼┾┦╀╄┑┭┯┥┽┿┩╃╇╻┎┏╽┟┢┃┠┣┒┰┲┧╁╆┨╂╊┓┱┳┪╅╈┫╉╋"
        make_tile = lambda a,b,c,d: tiles[27*d + 9*c + 3*b + 1*a]
        string = ""
        for row in self.grid:
            string  += '\n'
            strbelow = "\n"
            for node in row:
                [r,u,l,d] = [node.has_wall(dir) for dir in (RIGHT,UP,LEFT,DOWN)]
                [nr,nu,nl,nd] = [not val for val in (r,u,l,d)]
                string += (make_tile(u,nu,nl,l) + 2*make_tile(u,0,u,0) + make_tile(nr,nu,u,r))
                strbelow += make_tile(d,l,nl,nd) + 2*make_tile(d,0,d,0) + make_tile(nr,r,d,nd)
            string += strbelow
        return string

    def str_frame(self, slim=False):
        """Produce outline/frame (unicode) art of the maze.
        """
        wall = self.has_wall
        tiles = " ╶╵└╴─┘┴╷┌│├┐┬┤┼"
        #tiles = " -+++-++++|+++++"
        make_tile = lambda a,b,c,d: tiles[8*d + 4*c + 2*b + 1*a] + tiles[5*a]
        if slim: make_tile = lambda a,b,c,d: tiles[8*d + 4*c + 2*b + 1*a]
        # Top-left corner
        string = make_tile(wall(0,0,UP),False,False,wall(0,0,LEFT))
        # Top wall
        for x in range(self.width):
            string += make_tile(x<self.width-1 and wall(x+1,0,UP),False,wall(x,0,UP),wall(x,0,RIGHT))
        # Middle and bottom rows of string
        for y in range(self.height):
            # Left wall
            string += '\n'
            string += make_tile(wall(0,y,DOWN),wall(0,y,LEFT),False,y<self.height-1 and wall(0,y+1,LEFT))
            # Middle and right walls (2 chars/node)
            for x in range(self.width):
                string += make_tile(x<self.width-1 and wall(x+1,y,DOWN),wall(x,y,RIGHT),wall(x,y,DOWN),y<self.height-1 and wall(x,y+1,RIGHT))
        return string

    def str_frame_ascii(self, corridorwidth=1):
        # Top-left corner
        linestr = [['+']]
        # Top wall
        for node in self.grid[0]:
            linestr[0] += ['--' if node.has_wall(UP) else '  '] * corridorwidth
            linestr[0] += ['+']
        # Middle and bottom rows of string
        for row in self.grid:
            # Left wall
            row1 = ['|' if row[0].has_wall(LEFT) else ' ']
            row2 = ['+']
            # Middle and bottom walls (2 blocks/node)
            for node in row:
                row1 += ['  '] * corridorwidth
                row1 += ['|' if node.has_wall(RIGHT) else ' ']
                row2 += ['--' if node.has_wall(DOWN) else '  '] * corridorwidth
                row2 += ['+']
            linestr += [row1] * corridorwidth
            linestr += [row2]
        return '\n'.join(''.join(line) for line in linestr)

    def str_frame_ascii_small(self):
        """Produce a 'minimal/compact' ASCII art of the maze.
        """
        wall = self.has_wall
        # Corner cases are nasty, dude;
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
        string = [] # Here we instead add chars to a list and join at the end, for fun
        # Top-left corner
        string.append(cornersegment_top_left())
        # Top wall
        for x in range(self.width):
            string.append('_' if wall(x,0,UP) else ' ')
            string.append(cornersegment_top(x))
        # Middle and bottom rows of string
        for y in range(self.height):
            # Left wall
            string.append('\n')
            string.append(cornersegment_left(y))
            # Middle and right walls (2 chars/node)
            for x in range(self.width):
                string.append('_' if wall(x,y,DOWN) else ' ')
                string.append(cornersegment(x,y))
        return ''.join(string)

    def generate_image(self, bitmap=None):
        """Generate an Image of the maze and store it in the instance.
        - bitmap : custom bitmap (2D list)
        """
        if bitmap is None:
            bitmap = self.bitmap()
        width,height = len(bitmap[0]),len(bitmap)
        bit_to_rgb = lambda bit: (0,0,0) if bit else (255,255,255)
        imgdata = tuple(bit_to_rgb(bit) for bit in itertools.chain(*bitmap))
        # Convert to Image
        image = Image.new('RGB', (width,height))
        image.putdata(imgdata)
        return image

    def has_wall(self, x, y, direction):
        """Check whether there is a wall in that direction.
        - x, y : integers where 0<=x<width && 0<=y<height
        - direction : one of {RIGHT,UP,LEFT,DOWN}
        """
        return self.node_at(x,y).has_wall(direction)

    def node_at(self, x, y):
        """Provide direct access to a grid node.
        - x, y : integers where 0<=x<width && 0<=y<height
        """
        return self.grid[y][x]

    def connect(self, node0, node1):
        """Toggle the connection between two nodes in the maze.
        - node0, node1 : `Node`s
        """
        (x0,y0), (x1,y1) = node0.coordinates, node1.coordinates
        dx, dy = x1-x0, y1-y0
        if abs(dx) + abs(dy) != 1:
            raise ValueError("nodes to connect must be neighbors")
        get_dir = lambda dx,dy: (LEFT if dx<0 else RIGHT) if dx else (UP if dy<0 else DOWN)
        node0.toggle_edge(get_dir(dx,dy))
        node1.toggle_edge(get_dir(-dx,-dy))
        return None

    def connect_to(self, node, direction):
        """Toggle the connection between a node and its neighbor in the maze.
        """
        (x,y) = node.coordinates
        [r,u,l,d] = [direction==dir for dir in (RIGHT,UP,LEFT,DOWN)]
        invalid_direction = (
            r and x==self.width-1
            or l and x==0
            or u and y==0
            or d and y==self.height-1
        )
        if invalid_direction:
            raise ValueError("cannot connect node outside grid")
        dx, dy = (1 if r else -1 if l else 0), (1 if d else -1 if u else 0)
        neighbor = self.node_at(x+dx,y+dy)
        opposite_direction = {RIGHT:LEFT,UP:DOWN,LEFT:RIGHT,DOWN:UP}[direction]
        node.toggle_edge(direction)
        neighbor.toggle_edge(opposite_direction)
        return None

    def adjacent_to(self, node, connected=False):
        """Get the adjacent cells to a node.
        - node : `Node`
        """
        (x,y) = node.coordinates
        if connected:
            if 0<x             and node.has_edge(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_edge(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_edge(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_edge(DOWN):  yield self.node_at(x,y+1)
        else:
            if 0<x:             yield self.node_at(x-1,y)
            if x<self.width-1:  yield self.node_at(x+1,y)
            if 0<y:             yield self.node_at(x,y-1)
            if y<self.height-1: yield self.node_at(x,y+1)

# CLASSES END


# MAIN BEGIN
# No main
# MAIN END
