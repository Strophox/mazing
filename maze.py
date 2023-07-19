# OUTLINE BEGIN
"""
Contains the main `Maze` class,

This file contains all important maze-relation implementations to store, create and modify grid mazes.

Notes to self / Work in Progress:
- Docstrings:
    * a l l   m u s t   b e   c h e c k e d .
- Printers:
    * With colors: generate_image
    * With solution: frame_ascii
    * With solution challenge: str_frame
- Solvers:
    * A* pathfinder
- Printers:
    * Colored image (generated_image)
- ETC Dreams:
    * Maze navigator (w/ curses)
    * Interactive picker: distance by color
    * Doom (curses) █▯▓▯▒▯░ ".,-~:;=!*#$@"
"""
# OUTLINE END


# IMPORTS BEGIN

import itertools # chain
import collections # deque
import time # strftime
import random
from PIL import Image
import my_color_utils as col

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
    A class representing a maze grid cell/node.
    """
    def __init__(self, x, y):
        """Initialize a node by its grid coordinates."""
        self.coordinates = (x, y)
        self.flag = None
        self._edges = 0b0000

    def __repr__(self):
        return self._edges.__repr__()

    def has_wall(self, direction):
        """Check whether there is a wall in a certain direction from the node."""
        return not (self._edges & direction)

    def has_edge(self, direction):
        """Check whether there is an edge in a certain direction from the node."""
        return self._edges & direction

    def set_edges(self, direction):
        """Set node to be connected exactly into the given directions."""
        self._edges = direction

    def put_edge(self, direction):
        """Connect the node into the given directions."""
        self._edges |= direction

    def toggle_edge(self, direction):
        """Connect/disconnect the node into the given directions."""
        self._edges ^= direction

class Maze:
    """
    A class to store and interact with a maze grid.

    All methods of this class fall into these broad categories:
    - Primitive Interaction
        * __init__, __iter__, __repr__
        * generate_name
        * adjacent_to, connect, connect_to, has_wall, node_at
    - Sophisticated maze presentation
        * bitmap
        * str_bitmap
        * str_block, str_block_double, str_block_half, str_block_quarter
        * str_frame, str_frame_ascii, str_frame_ascii_small
        * str_pipes
        * generate_image
    - Generation algorithms (static methods)
        * from_template
        * backtracker, bogus, divide_conquer, growing_tree, kruskal, prim, quad_divide_conquer, wilson
    - Maze modification
        * make_unicursal
    """

    def __init__(self, width, height):
        """Initialize a node by its size.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        if not (width > 0 and height > 0):
            raise ValueError("Maze must have positive width and height")
        self.width  = width
        self.height = height
        self._grid = [[Node(x,y) for x in range(width)] for y in range(height)]
        self._timestamp = time.strftime('%Y-%m-%d_%Hh%Mm%S')
        self._history = []
        self._solution = None

    def __repr__(self):
        return (self._history, self._grid).__repr__()

    def name(self):
        """Generate human-readable name for the maze."""
        size = f"{self.width}" if self.width==self.height else f"{self.width}x{self.height}"
        history = '-'.join(self._history)
        timestamp = self._timestamp
        name = f"maze{size}_{history}_{timestamp}"
        return name

    def _log_action(self, title):
        self._timestamp = time.strftime('%Y-%m-%d_%Hh%Mm%S')
        self._history.append(title)

    def nodes(self):
        """Produce iterator over the nodes of the maze."""
        return itertools.chain(*self._grid)

    def edges(self):
        """Produce iterator over the edges of the maze."""
        edge_iterators = []
        rows = self._grid
        for row in rows:
            row_right = iter(row)
            next(row_right)
            edge_iterators += [zip(row,row_right)]
        rows_below = iter(rows)
        next(rows_below)
        for row,row_below in zip(rows,rows_below):
            edge_iterators += [zip(row,row_below)]
        return itertools.chain(*edge_iterators)

    def generate_raster(self, corridorwidth=1, columnated=True, show_marked_nodes=False, show_flags=False): # TODO FIXME DANGER WARNING BUG BEGIN END ATTENTION
        """Return a simple 2D raster representation of the maze.

        Args:
            corridorwidth (int): Multiplier of how much wider corridors should be compared to the walls (default is 1)
            columnated (bool): Whether free-standing 'column' pieces should be placed in free 4x4 sections of the maze (default is True)

        Returns:
            list(list(bool)): 2D raster of the maze
        """
        wall = self.has_wall
        if show_flags:
            mkval = lambda is_wall, x,y: -1 if is_wall else self.node_at(x,y).flag
        elif show_marked_nodes and self._solution is not None:
            mkval = lambda is_wall, x,y: 1 if is_wall else 2 if self.node_at(x,y) in self._solution else 0
        else:
            mkval = lambda is_wall, x,y: True if is_wall else False
        if columnated:
            column_wall = lambda x,y: True
        else:
            column_wall = lambda x,y: x==self.width-1 or y==self.height-1 or wall(x,y,RIGHT) or wall(x,y,DOWN) or wall(x+1,y+1,LEFT) or wall(x+1,y+1,UP)
        # Top-left corner
        val = mkval(True, 0,0)
        raster = [[val]]
        # Top wall
        for x,node in enumerate(self._grid[0]):
            val = mkval(node.has_wall(UP),x,0)
            raster[0] += [val] * corridorwidth
            val = mkval(True,x,0)
            raster[0] += [val]
        # Middle and bottom rows of string
        for y,row in enumerate(self._grid):
            # Left wall
            val = mkval(row[0].has_wall(LEFT), 0,y)
            row1 = [val]
            val = mkval(True, 0,y)
            row2 = [val]
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                val = mkval(False, x,y)
                row1 += [val] * corridorwidth
                val = mkval(node.has_wall(RIGHT), x,y)
                row1 += [val]
                val = mkval(node.has_wall(DOWN), x,y)
                row2 += [val] * corridorwidth
                val = mkval(column_wall(x,y), x,y)
                row2 += [val]
            raster += [row1] * corridorwidth
            raster += [row2]
        return raster

    @staticmethod
    def raster_to_image(raster, value_to_rgb):
        """TODO"""
        pixels = [value_to_rgb(value) for value in itertools.chain(*raster)]
        image = Image.new('RGB', (len(raster[0]),len(raster)))
        image.putdata(pixels)
        return image

    def generate_image(self, show_marked_nodes=True, wallcolor=(0,0,0), aircolor=(255,255,255), markcolor=(53,215,187)):#(255,127,127)):
        """Generate a handle to a (PIL) Image object presenting the maze.

        Args:
            raster (list(list(bool))): Bit map to be rendered (default is self.generate_raster())
        """
        raster = self.generate_raster(show_marked_nodes=show_marked_nodes)
        if show_marked_nodes:
            value_to_rgb = lambda value: markcolor if value==2 else wallcolor if value==1 else aircolor
        else:
            value_to_rgb = lambda value: wallcolor if value else air
        image = Maze.raster_to_image(raster, value_to_rgb)
        return image

    def generate_image_colored(self, gradcol0=(147,118,224), gradcol1=(255,245,184)):
        if self._solution is None:
            raise ValueError("maze must be searched to generate colored image")
        if gradcol1 is None: # TODO
            gradcol1 = tuple(255-x for x in gradcol0)
        raster = self.generate_raster(show_flags=True)
        peak = max(itertools.chain(*raster))
        value_to_rgb = lambda val: (0,0,0) if val==-1 else tuple(round((1-val/peak)*c0 + (val/peak)*c1) for c0,c1 in zip(gradcol0,gradcol1))
        image = Maze.raster_to_image(raster, value_to_rgb)
        return image

    @staticmethod
    def raster_to_string(raster, value_to_chars):
        """TODO"""
        string = '\n'.join(
            ''.join(
                value_to_chars(value) for value in row
            ) for row in raster
        )
        return string

    def str_raster(self, wall='#', air=None):
        """Produce a binary string presentation of the maze.

        Args:
            wall (str): Wall texture (default is '#')
            air (str): Air texture (default is len(wall)*' ')
            raster (list(list(bool))): Bit map to be rendered (default is self.generate_raster())

        Returns:
            str: Binary string presentation of the maze
        """
        if air is None:
            air = len(wall)*' '
        raster = self.generate_raster()
        value_to_chars = lambda value: wall if value else air
        string = Maze.raster_to_string(raster, value_to_chars)
        return string

    def str_block_double(self):
        """Produce a wide (unicode) block string presentation of the maze."""
        return self.str_raster(wall='██')

    def str_block(self):
        """Produce a (unicode) block string presentation of the maze."""
        return self.str_raster(wall='█')

    def str_block_half(self):
        """Produce a (unicode) half-block string presentation of the maze."""
        raster = self.generate_raster()
        # Pad raster to even height
        if len(raster)%2!=0:
            raster.append([False for _ in raster[0]])
        # String is just a join of row strings (which are also join)
        tiles = " ▄▀█"
        string = '\n'.join(
            ''.join(
                tiles[2*hi + 1*lo] for (hi,lo) in zip(raster[y],raster[y+1])
            ) for y in range(0,len(raster),2)
        )
        return string

    def str_block_quarter(self):
        """Produce a (unicode) quarter-block string presentation of the maze."""
        raster = self.generate_raster()
        # Pad bitmap to even height and width
        if len(raster)%2!=0:
            raster.append([False for _ in raster[0]])
        if len(raster[0])%2!=0:
            for row in raster: row.append(False)
        # String is just a join of row strings (which are also join)
        tiles = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█" # ▯▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█
        string = '\n'.join(
            ''.join(
                tiles[8*raster[y+1][x+1] + 4*raster[y+1][x] + 2*raster[y][x+1] + 1*raster[y][x]] for x in range(0,len(raster[0]),2)
            ) for y in range(0,len(raster),2)
        )
        return string

    def str_pipes(self):
        """Produce a (unicode) pipe-like string presentation of the maze."""
        tiles = " ╶╺╵└┕╹┖┗╴─╼┘┴┶┚┸┺╸╾━┙┵┷┛┹┻╷┌┍│├┝╿┞┡┐┬┮┤┼┾┦╀╄┑┭┯┥┽┿┩╃╇╻┎┏╽┟┢┃┠┣┒┰┲┧╁╆┨╂╊┓┱┳┪╅╈┫╉╋"
        make_tile = lambda a,b,c,d: tiles[27*d + 9*c + 3*b + 1*a]
        string = ""
        for row in self._grid:
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
        """Produce a (unicode) frame string presentation of the maze.

        Args:
            slim (bool): Whether art should be half as wide (default is False)

        Returns:
            str: (unicode) frame string presentation of the maze
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

    def str_frame_ascii(self, corridorwidth=1, show_marked_nodes=True):
        """Produce an (ASCII) frame string presentation of the maze.

        Args:
            corridorwidth (int): Multiplier of how much wider corridors should be compared to the walls (default is 1)
            show_marked_nodes (bool): Whether solution should be displayed if calculated (default is True)

        Returns:
            str: (ASCII) frame string presentation of the maze
        """
        # Top-left corner
        linestr = [['+']]
        # Top wall
        for node in self._grid[0]:
            linestr[0] += ['---' if node.has_wall(UP) else '   '] * corridorwidth
            linestr[0] += ['+']
        # Middle and bottom rows of string
        for row in self._grid:
            # Left wall
            row1 = ['|' if row[0].has_wall(LEFT) else ' ']
            row2 = ['+']
            # Middle and bottom walls (2 blocks/node)
            for node in row:
                row1 += [f' {"." if show_marked_nodes and node in self._solution else " "} '] * corridorwidth
                row1 += ['|' if node.has_wall(RIGHT) else ' ']
                row2 += ['---' if node.has_wall(DOWN) else '   '] * corridorwidth
                row2 += ['+']
            linestr += [row1] * corridorwidth
            linestr += [row2]
        return '\n'.join(''.join(line) for line in linestr)

    def str_frame_ascii_small(self):
        """Produce a minimal (ASCII) frame string presentation of the maze."""
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

    def has_wall(self, x, y, direction):
        """Check for a wall, facing some direction at some location in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height
            direction (int) : One of (RIGHT,UP,LEFT,DOWN) = (1,2,4,8)

        Returns:
            bool: Whether there is a wall when facing direction from (x,y) in maze
        """
        return self.node_at(x,y).has_wall(direction)

    def node_at(self, x, y):
        """Get node at those coordinates in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height

        Returns:
            Node: Node object at position (x,y) in maze
        """
        return self._grid[y][x]

    def connect(self, node0, node1):
        """Toggle the connection between two nodes in the maze.

        Args:
            node0, node1 (Node): Two nodes in the maze that lie adjacent
        """
        (x0,y0), (x1,y1) = node0.coordinates, node1.coordinates
        dx, dy = x1-x0, y1-y0
        if abs(dx) + abs(dy) != 1:
            raise ValueError("nodes to connect must be neighbors")
        get_dir = lambda dx,dy: (LEFT if dx<0 else RIGHT) if dx else (UP if dy<0 else DOWN)
        node0.toggle_edge(get_dir(dx,dy))
        node1.toggle_edge(get_dir(-dx,-dy))
        return

    def connect_to(self, node, direction):
        """Toggle the connection between two nodes in the maze.

        Args:
            node (Node): Node within the maze
            direction (int) : One of (RIGHT,UP,LEFT,DOWN) = (1,2,4,8), where direction cannot face outside of maze boundaries (else ValueError)
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
        return

    def adjacent_to(self, node, connected=None):
        """Get all cells that are adjacent to node in the maze.

        Args:
            node (Node): Origin node
            connected (bool): Flag to additionally check cells for being connected or disconnected (default is None)

        Yields:
            Node: Neighboring node fulfilling conditions
        """
        (x,y) = node.coordinates
        if connected is None:
            if 0<x:             yield self.node_at(x-1,y)
            if x<self.width-1:  yield self.node_at(x+1,y)
            if 0<y:             yield self.node_at(x,y-1)
            if y<self.height-1: yield self.node_at(x,y+1)
        elif connected:
            if 0<x             and node.has_edge(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_edge(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_edge(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_edge(DOWN):  yield self.node_at(x,y+1)
        elif not connected:
            if 0<x             and node.has_wall(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_wall(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_wall(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_wall(DOWN):  yield self.node_at(x,y+1)

    def _unflag_nodes(self):
        """Set flag attributes of all nodes to `None`."""
        for node in self.nodes():
            node.flag = None

    def _join_nodes(self):
        """Join all nodes within the maze """
        for y,row in enumerate(self._grid):
            for x,node in enumerate(row):
                direction = 0b0000
                if 0<x:             direction |= LEFT
                if x<self.width-1:  direction |= RIGHT
                if 0<y:             direction |= UP
                if y<self.height-1: direction |= DOWN
                node.put_edge(direction)
        return

    def make_unicursal(self):
        """Convert self into a unicursal/ maze by removing no dead ends."""
        if "braided" not in self._history: # FIXME icky
            for node in self.nodes():
                while sum(1 for _ in self.adjacent_to(node,connected=True)) <= 1:
                    neighbor = random.choice(list(self.adjacent_to(node,connected=False)))
                    self.connect(node,neighbor)
            self._log_action("braided")
        return

    def breadth_first_search(self, entrance=None, exit=None):
        """Compute all node distances and draw in the shortest path in a maze.

        Args:
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is (0,0))
        """
        if entrance is None:
            entrance = self.node_at(0,0)
        if exit is None:
            exit = self.node_at(-1,-1)
        for node in self.nodes():
            node.flag = -1
        queue = collections.deque(maxlen=3*max(self.width,self.height))
        queue.append(entrance)
        entrance.flag = 0
        while queue:
            node = queue.popleft()
            neighbors = list(self.adjacent_to(node,connected=True))
            for neighbor in neighbors:
                if neighbor.flag == -1:
                    queue.append(neighbor)
                    neighbor.flag = node.flag + 1
        # Find solution path if not yet calculated
        if self._solution is None:
            # Backtrack solution path
            self._solution = set()
            current = exit
            while current != entrance:
                self._solution.add(current)
                current = min(self.adjacent_to(current,connected=True), default=False, key=lambda n:n.flag)
                if not current: break
            self._solution.add(entrance)
        return


#    def recursively_backtrack(self):
#        """Carve a maze using simple randomized depth-first-search.
#
#        Simple standalone implementation and tries to fill out every unvisited node but prone to function recursion limit for large mazes (see growing tree instead).
#        """
#        randomized = lambda it: random.shuffle(ls:=list(it)) or ls # randomize iterator
#        def dfs(node):
#            for neighbor in randomized(self.adjacent_to(node)):
#                if not neighbor.flag:
#                    neighbor.flag = True
#                    self.connect(node,neighbor)
#                    dfs(neighbor)
#        for node in self.nodes():
#            if not node.flag:
#                node.flag = True
#                dfs(node)
#        self._infotags.append("backtracked")
#        return

    @staticmethod
    def from_template(temp):
        """Generate a maze by loading from a template.

        Args:
            temp (list(str),list(list(int))): Maze representation

        Returns:
            Maze: Corresponding maze object
        """
        (history,grid) = temp
        maze = Maze(len(grid[0]),len(grid))
        for x in range(maze.height):
            for y in range(maze.width):
                maze.node_at(x,y).set_edges(grid[y][x])
        maze._history = history
        return maze

    @staticmethod
    def bogus(width, height):
        """Build a bogus maze by having every node randomly connected.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        maze = Maze(width,height)
        for node in maze.nodes():
            node.toggle_edge(random.randint(0b0000,0b1111))
        maze._log_action("bogo")
        return maze

    @staticmethod
    def growing_tree(width, height, start_coord=None, index_choice=None, fast_pop=False):
        """Build a random maze using the '(random) growing tree' algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
            index_choice (callable(int) -> int): Function to pick an index between 0 and a given max_index, used to determine behaviour of the algorithm (default is lambda max_index: -1 if random.random()<0.95 else random.randint(0,max_index))
            fast_pop (bool): Whether to switch chosen element with last element when removing from active set. This is to speed up generation of large, random mazes (default is False)
        """
        maze = Maze(width, height)
        if start_coord is None:
            start_coord = (random.randrange(maze.width),random.randrange(maze.height))
        start = maze.node_at(*start_coord)
        if index_choice is None:
            index_choice = lambda max_index: -1 if random.random()<0.95 else random.randint(0,max_index)
        start.flag = True
        bucket = [start]
        while bucket:
            n = index_choice(len(bucket)-1)
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
        maze._unflag_nodes()
        maze._log_action("tree")
        return maze

    @staticmethod
    def prim(width, height, start_coord=None):
        """Build a random maze using randomized Prim's algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        maze = Maze.growing_tree(width, height, start_coord, index_choice=lambda max_index: random.randint(0,max_index))
        maze._log_action("prim")
        return maze

    @staticmethod
    def backtracker(width, height, start_coord=None):
        """Build a random maze using randomized depth first search.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        maze = Maze.growing_tree(width, height, start_coord, index_choice=lambda max_index: -1)
        maze._log_action("dfs")
        return maze

    @staticmethod
    def kruskal(width, height):
        """Build a random maze using randomized Kruskal's algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        maze = Maze(width, height)
        edges = list(maze.edges())
        random.shuffle(edges)
        members = {}
        for (node0,node1) in edges:
            if not node0.flag:
                node0.flag, members[node0] = node0, [node0]
            if not node1.flag:
                node1.flag, members[node1] = node1, [node1]
            if node0.flag != node1.flag:
                maze.connect(node0,node1)
                if len(members[node0.flag]) < len(members[node1.flag]):
                    smaller,bigger = node0,node1
                else: smaller,bigger = node1,node0
                for node in members[smaller.flag]:
                    node.flag = bigger.flag
                    members[bigger.flag].append(node)
                if len(members[bigger.flag])==maze.width*maze.height: break
        maze._unflag_nodes()
        maze._log_action("kruskal")
        return maze

    @staticmethod
    def wilson(width, height, start_coord=None):
        """Build a random maze using Wilson's uniform spanning tree algorithm..

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        maze = Maze(width, height)
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
        nodes = list(maze.nodes())
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
        maze._unflag_nodes()
        maze._log_action("wilson")
        return maze

    @staticmethod
    def quad_divide_conquer(width, height):
        """Build a random maze using randomized quadruple divide-and-conquer.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        maze = Maze(width, height)
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
        maze._join_nodes()
        divide((0,0), (maze.width-1,maze.height-1))
        maze._log_action("divide4")
        return maze

    @staticmethod
    def divide_conquer(width, height, slice_bias=1.0, pivot_choice=None):
        """Build a random maze using randomized divide-and-conquer.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            slice_bias (float): Probability (0<=slice_bias<=1) to do a reroll when dividing a quadrant along the same direction as parent call
            pivot_choice (callable(int,int) -> int): Function to choose a random index between given lower and upper index along which to make a cut
        """
        maze = Maze(width, height)
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
        maze._join_nodes()
        divide((0,0), (maze.width-1,maze.height-1), maze.width)
        maze._log_action("divide")
        return maze

# CLASSES END


# MAIN BEGIN
# No main
# MAIN END
