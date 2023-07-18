
# OUTLINE BEGIN

# A small script to generate some mazes
"""
Work in Progress:
- Refactor:
  * maze naming internals
- Carvers: All done!
- Solvers:
  * BFS
  * A* pathfinder
- ETC Dreams:
  * Maze navigator (w/ curses)
  * Interactive picker: distance by color
  * Doom (curses) █▯▓▯▒▯░ ".,-~:;=!*#$@"
"""

# OUTLINE END


# IMPORTS BEGIN

import random
import itertools # chain
import time # perf_counter
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
        if wall is None:     make_wall = lambda: random.choice(['##','#@','%#'])
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


# FUNCTIONS BEGIN

def bogus_maze(dimensions):
    """Build a complete bogus maze by randomizing every node.
    """
    maze = Maze(*dimensions)
    for node in maze:
        node.toggle_edge(random.randint(0b0000,0b1111))
    maze.add_info("bogus")
    return maze

def growing_tree_maze(dimensions, start_coord=None, index_choice=None, fast_pop=False):
    """Build a maze using the 'growing binary tree' algorithm.
    - start : origin `Node`
    - index_choice : callable that returns a valid index given an indexable `bucket`
    * Note that this carver can be made equivalent to other algorithms by tweaking `index_choice`:
      - always `-1` (newest element) is recursive backtracker / depth first search
      - always `0` (oldest element) is breadth first search
      - always random is randomized prim's algorithm.
    """
    maze = Maze(*dimensions)
    if start_coord is None:
        start_coord = (random.randrange(maze.width),random.randrange(maze.height))
    start = maze.node_at(*start_coord)
    if index_choice is None:
        index_choice = lambda bucket: -1 if random.random()<0.95 else random.randrange(len(bucket))
    start.flag = True
    bucket = [start]
    while bucket:
        n = index_choice(bucket)
        node = bucket[n]
        neighbors = [nb for nb in maze.adjacent_to(node) if not nb.flag]
        if neighbors:
            neighbor = random.choice(neighbors)
            maze.connect(node,neighbor)
            neighbor.flag = True
            bucket.append(neighbor)
        else:
            if fast_pop:
                if len(bucket) > 1 and n != -1:
                    bucket[n],bucket[-1] = bucket[-1],bucket[n]
                bucket.pop()
            else:
                bucket.pop(n)
    maze.add_info("growing-tree")
    return maze

def prim_maze(dimensions, start_coord=None):
    """Build a maze using randomized Prim's algorithm.
    """
    maze = growing_tree_maze(dimensions, start_coord, index_choice=lambda bucket: random.randrange(len(bucket)))
    maze.add_info("prim")
    return maze

def backtracker_maze(dimensions, start_coord=None):
    """Build a maze using simple randomized depth-first-search.
    * More robust than `recursive backtracker` for larger mazes.
    """
    maze = growing_tree_maze(dimensions, start_coord, index_choice=lambda bucket: -1)
    maze.add_info("backtracker")
    return maze

def kruskal_maze(dimensions):
    """Build a maze using randomized Kruskal's algorithm.
    """
    maze = Maze(*dimensions)
    edges = []
    rows = maze.grid
    for row in rows:
        row_right = iter(row) ; next(row_right)
        edges.extend(zip(row,row_right))
    rows_below = iter(rows) ; next(rows_below)
    for row,row_below in zip(rows,rows_below):
        edges.extend(zip(row,row_below))
    random.shuffle(edges)
    for (node0,node1) in edges:
        if not getattr(node0,'color',None):
            node0.color, node0.members = node0, [node0]
        if not getattr(node1,'color',None):
            node1.color, node1.members = node1, [node1]
        if node0.color != node1.color:
            maze.connect(node0,node1)
            if len(node0.color.members) < len(node1.color.members):
                smaller,bigger = node0,node1
            else: smaller,bigger = node1,node0
            for node in smaller.color.members:
                node.color = bigger.color
                bigger.color.members.append(node)
            if len(bigger.color.members)==maze.width*maze.height: break
    maze.add_info("kruskal")
    return maze

def wilson_maze(dimensions, start_coord=None):
    """Build a maze using Wilson's random uniform spanning tree algorithm.
    """
    maze = Maze(*dimensions)
    def backtrack_walk(tail_node, origin):
        while tail_node != origin:
            prev_node = next(maze.adjacent_to(tail_node,connected=True))
            maze.connect(tail_node,prev_node) # DANGER actually disconnecting
            tail_node.flag = 0
            tail_node = prev_node
    if start_coord is None:
        start = maze.node_at(maze.width//2,maze.height//2)
    else:
        start = maze.node_at(*start_coord)
    nodes = list(maze)
    nodes.remove(start)
    generation = 1
    start.flag = generation
    random.shuffle(nodes)
    for node in nodes:
        if not node.flag:
            generation += 1
            node.flag = generation
            curr_node = node
            while True:
                next_node = random.choice(list(maze.adjacent_to(curr_node)))
                if not next_node.flag:
                    next_node.flag = generation
                    maze.connect(curr_node,next_node)
                    curr_node = next_node
                elif next_node.flag == generation:
                    backtrack_walk(curr_node,next_node)
                    curr_node = next_node
                elif next_node.flag < generation:
                    maze.connect(curr_node,next_node)
                    break
    maze.add_info("wilson")
    return maze

def quarter_division_maze(dimensions):
    """Build a maze using a divide-and-conquer approach.
    """
    maze = Maze(*dimensions)
    def divide(topleft, bottomright):
        (x0,y0), (x1,y1) = topleft, bottomright
        if x0==x1 or y0==y1: return
        (xP,yP) = (random.randrange(x0,x1),random.randrange(y0,y1))
        for x in range(x0,x1+1):
            maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1)) # DANGER actually disconnect
        for y in range(y0,y1+1):
            maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y)) # DANGER actually disconnect
        dice = random.randint(1,4)
        if dice != 1:
            x = random.randint(x0,xP)
            maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1))
        if dice != 2:
            x = random.randint(xP+1,x1)
            maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1))
        if dice != 3:
            y = random.randint(y0,yP)
            maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y))
        if dice != 4:
            y = random.randint(yP+1,y1)
            maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y))
        divide((x0,y0), (xP,yP))
        divide((xP+1,y0), (x1,yP))
        divide((x0,yP+1), (xP,y1))
        divide((xP+1,yP+1), (x1,y1))
    for y,row in enumerate(maze.grid):
        for x,node in enumerate(row):
            dir = 0b0000
            if 0<x:             dir |= LEFT
            if x<maze.width-1:  dir |= RIGHT
            if 0<y:             dir |= UP
            if y<maze.height-1: dir |= DOWN
            node.put_edge(dir)
    divide((0,0), (maze.width-1,maze.height-1))
    maze.add_info("divide-q")
    return maze

def division_maze(dimensions, slice_bias=1.0, pivot_choice=None):
    """Build a maze using a divide-and-conquer approach.
    """
    maze = Maze(*dimensions)
    if pivot_choice is None:
        pivot_choice = lambda l,r: (l+r)//2
        #pivot_choice = lambda l,r: min(max(l,int(random.gauss((l+r)/2,(l+r)/2**6))),r)
        #pivot_choice = lambda l,r: random.triangular(l,r)
        #pivot_choice = lambda l,r: random.randint(l,r)
    def divide(topleft, bottomright, prev_horz):
        (x0,y0), (x1,y1) = topleft, bottomright
        if x0==x1 or y0==y1: return
        horizontal_cut = random.getrandbits(1)
        while prev_horz==horizontal_cut and random.random() < slice_bias:
            horizontal_cut = random.getrandbits(1)
        if horizontal_cut:
            yP = pivot_choice(y0,y1-1)
            for x in range(x0,x1+1):
                maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1)) # DANGER actually disconnect
            x = random.randint(x0,x1)
            maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1))
            divide((x0,y0), (x1,yP), True)
            divide((x0,yP+1), (x1,y1), True)
        else:
            xP = pivot_choice(x0,x1-1)
            for y in range(y0,y1+1):
                maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y)) # DANGER actually disconnect
            y = random.randint(y0,y1)
            maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y))
            divide((x0,y0), (xP,y1), False)
            divide((xP+1,y0), (x1,y1), False)
        #print(maze.str_frame())
    for y,row in enumerate(maze.grid):
        for x,node in enumerate(row):
            dir = 0b0000
            if 0<x:             dir |= LEFT
            if x<maze.width-1:  dir |= RIGHT
            if 0<y:             dir |= UP
            if y<maze.height-1: dir |= DOWN
            node.put_edge(dir)
    divide((0,0), (maze.width-1,maze.height-1), maze.width)
    maze.add_info("divide-n-conquer")
    return maze

def recursive_backtracker(maze):
    """Carve a maze using simple randomized depth-first-search.
    * Prone to function recursion limit for large mazes.
    * Simple standalone implementation and tries to fill out every unvisited node.
    """
    randomized = lambda it: random.shuffle(ls:=list(it)) or ls # randomize iterator
    def dfs(node):
        for neighbor in randomized(maze.adjacent_to(node)):
            if not neighbor.flag:
                neighbor.flag = True
                maze.connect(node,neighbor)
                dfs(neighbor)
    for node in maze:
        if not node.flag:
            node.flag = True
            dfs(node)
    maze.add_info("backtracked")
    return None

def make_unicursal(maze):
    """Convert a maze into a unicursal/'braided' maze by joining/removing no dead ends.
    """
    for node in maze:
        dirs = [dir for dir in (RIGHT,UP,LEFT,DOWN) if node.has_wall(dir)]
        if len(dirs) == 3:
            (x,y) = node.coordinates
            if x==0: dirs.remove(LEFT)
            if x==maze.width-1: dirs.remove(RIGHT)
            if y==0: dirs.remove(UP)
            if y==maze.height-1: dirs.remove(DOWN)
            maze.connect_to(node, random.choice(dirs))
    maze.add_info("joined")
    return None

def maze_maze():
    """Creates a custom maze that spells 'MAZE'.
    """
    def maze_from_mask(template):
        assert((height:=len(template)) > 0 and (width:=len(template[0])) > 0)
        maze = Maze(width, height)
        mask = itertools.chain(*template)
        for (node,bit) in zip(maze,mask):
            node.flag = not bit
            node.toggle_edge(0b1111 * (not bit))
        return maze
    template = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,0,1],
        [1,0,0,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,0,0,1,1,0,1,1,0,0,1,1],
        [1,0,1,0,1,0,1,0,1,0,0,0,1,1,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    maze = maze_from_mask(template)
    recursive_backtracker(maze)
    return maze

def autocomplete(input_word, full_words):
    candidates = [w for w in full_words if w.startswith(input_word)]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return input_word

def run_and_time(f):
    start_time = time.perf_counter()
    result = f()
    time_taken = time.perf_counter() - start_time
    return (result, time_taken)

def display(maze, limit=100*100):
    cellcount = maze.width*maze.height
    if cellcount <= limit:
        print(maze.str_frame())
    else:
        print(f"[no print (cellcount {cellcount})]")
    return None

# FUNCTIONS END


# MAIN BEGIN

def main():
    main_dimensions = (16,16)
    main_maze = maze_maze()#Maze(*dimensions)
    main_image = None
    import textwrap # remove source code multiline string indents
    help_menu_text = textwrap.dedent("""
       A Mazing Sandbox
        | help  : show this menu
       Editing
        | build : new maze
        | join  : /remove dead ends
        | size  : for next maze
        | load  : maze from string
       Viewing
        | print : latest maze, ascii art
        | show  : latest maze, external png
        | save  : external png
       >""")
    commands = ["help","build","join","size","load","print","show","save"]
    command = "help"
    while command:
        match command:
            case "help":
                user_input = input(help_menu_text)
                command = autocomplete(user_input.strip(), commands)
                continue
            case "build":
                builders = {x.__name__:x for x in [
                    backtracker_maze,
                    growing_tree_maze,
                    prim_maze,
                    kruskal_maze,
                    wilson_maze,
                    division_maze,
                    quarter_division_maze,
                ]}
                user_input = input(f"Choose method:\n| " + ' | '.join(builders) + "\n>")
                name = autocomplete(user_input.strip(),builders)
                if name in builders:
                    (main_maze, secs) = run_and_time(lambda: builders[name](main_dimensions))
                    print(f"[{name} completed in {secs:.03f}s]")
                    main_cached_image = None
                    display(main_maze)
                else:
                    print(f"[unrecognized algorithm '{name}']")
            case "join":
                (_, secs) = run_and_time(lambda: make_unicursal(main_maze))
                print(f"[joining completed in {secs:.03f}s]")
                main_cached_image = None
                display(main_maze)
            case "size":
                user_input = input("Enter dimensions 'X Y' >")
                try:
                    main_dimensions = (_, _) = tuple(map(int, user_input.split()))
                except Exception as e:
                    print(f"[invalid dimensions: {e}]")
            case "load":
                user_input = input("Enter string `repr`esentation (e.g. '[[9,5..]]') >")
                try:
                    main_maze = Maze.from_grid(eval(user_input.strip()))
                    display(main_maze)
                except Exception as e:
                    print(f"[could not load maze: {e}]")
            case "print":
                printers = {x.__name__:x for x in [
                    Maze.str_bitmap,
                    Maze.str_block_double,
                    Maze.str_block,
                    Maze.str_block_half,
                    Maze.str_block_quarter,
                    Maze.str_pipes,
                    Maze.str_frame,
                    Maze.str_frame_ascii,
                    Maze.str_frame_ascii_small,
                    repr,
                ]}
                for name,printer in printers.items():
                    print(f"{name}:\n{printer(main_maze)}")
            case "show":
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                print(f"[showing maze in external program]")
                main_cached_image.show()
            case "save":
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                filename = f"{main_maze.make_name()}.png"
                main_cached_image.save(filename)
                print(f"[saved '{filename}']")
            case cmd if cmd in {"debug","exec","sudo","dev","py"}:
                user_input = input(">>> ")
                try:
                    exec(user_input)
                except Exception as e:
                    print(f"<error: {e}>")
            case _:
                print("[unrecognized command]")
        user_input = input(f"""| {' | '.join(commands)} >""")
        command = autocomplete(user_input.strip(), commands)
    print("goodbye")

def my_benchmark():
    """Run `python3 -m scalene maze.py`
    """
    sq = lambda n: (n,n)
    # Execute actions
    benchmark_maze = Maze(1,1)
    for (title,action) in [
          ("BEGIN", lambda maze:
            maze
        ),("div-cqr", lambda maze:
             division_maze(sq(2**9))
        ),("grow w/fastpop", lambda maze:
            growing_tree_maze(sq(2**9),fast_pop=True)
        ),("wilson", lambda maze:
            wilson_maze(sq(2**7))
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.make_name()}.png") and()or maze
        ),("join", lambda maze:
            make_unicursal(maze) and()or maze # cursed sequential composition
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.make_name()}.png") and()or maze
        ),("END  ", lambda maze:
            maze
        ),
    ]:
        (benchmark_maze, secs) = run_and_time(lambda:action(benchmark_maze))
        print(f"['{title}' completed in {secs:.03f}s]")

if __name__=="__main__":
    main()
    #my_benchmark()

#[[8,9,13,5,5,5,12,1,5,13,13,5,5,4,9,12],[11,6,2,9,12,1,7,5,5,14,2,9,13,5,6,10],[3,12,9,6,3,5,5,5,12,10,9,6,3,12,9,6],[9,14,3,12,1,13,4,9,6,2,10,1,5,6,10,8],[10,3,5,6,9,7,12,3,5,5,6,8,9,5,6,10],[10,9,5,4,10,8,3,5,12,9,5,6,3,12,9,6],[10,11,5,5,6,3,13,4,10,11,5,5,12,10,3,12],[10,3,12,8,9,13,6,1,6,10,1,12,3,14,9,14],[3,12,10,10,10,3,5,12,1,7,12,3,12,3,6,10],[9,14,11,14,11,5,12,3,5,4,10,9,7,4,9,6],[10,10,2,10,10,1,14,8,8,9,6,10,1,12,10,8],[10,3,12,10,10,8,11,6,10,3,5,7,4,3,6,10],[10,8,11,7,14,10,3,12,11,5,5,13,12,8,9,14],[10,10,10,9,6,10,9,6,10,1,13,6,3,6,2,10],[10,10,10,2,9,6,10,1,7,12,3,5,12,1,13,14],[3,6,3,5,6,1,7,5,5,6,1,5,7,5,6,2]]

# MAIN END
