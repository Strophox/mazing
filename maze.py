# OUTLINE BEGIN
"""
Contains the main `Maze` class,

This file contains all important maze-relation implementations to store, create and modify grid mazes.

### Work in Progress:
- General:
    * a l l   d o c s t r i n g s   m u s t   b e   c h e c k e d   ( d e a t h )
- Printers:
    * distance heatmap (official standards?)
    * FIXME generate_raster
    * str_frame_ascii_small solution
    * CHALLENGE str_frame solution
- Builders:
    * division; alternate on aspect ratio
    * division; rooms
    * CHALLENGE compose algorithms
- Solvers:
    * A* pathfinder
- ETC Dreams:
    * curses maze navigator
    * CHALLENGE doom; "░▒▓█.,-~:;=!*#$@"
"""
# OUTLINE END


# IMPORTS BEGIN

import itertools # chain
import collections # deque
import time # strftime
import random
from PIL import Image
import my_colortools as col

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
        self.distance = None
        self._edges = 0b0000

    def __repr__(self):
        return self.coordinates.__repr__()

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
        * backtracker, bogus, division, growing_tree, kruskal, prim, quad_division, wilson
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
        self._entrance = self.node_at(0,0)
        self._exit = self.node_at(-1,-1)
        self._history = [time.strftime('%Y-%m-%d_%Hh%Mm%S')]
        self._solution = None

    def __repr__(self):
        string = (
            self._history,
            self._entrance.coordinates,
            self._exit.coordinates,
            [[node._edges for node in row] for row in self._grid],
        ).__repr__()
        return string

    @staticmethod
    def from_repr(data):
        """Generate a maze by loading from a template.

        Args:
            data (list(str),list(list(int))): Maze representation

        Returns:
            Maze: Corresponding maze object
        """
        (
            history,
            entrance_coordinates,
            exit_coordinates,
            grid
        ) = data
        assert (type(grid) == list)
        assert (len(grid) > 0)
        assert (type(grid[0]) == list)
        assert (len(grid[0]) > 0)
        maze = Maze(len(grid[0]),len(grid))
        for x in range(maze.height):
            for y in range(maze.width):
                assert (type(grid[y][x]) == int)
                maze.node_at(x,y).set_edges(grid[y][x])
        assert (type(entrance_coordinates) == tuple)
        assert (type(entrance_coordinates[0]) == int)
        assert (type(entrance_coordinates[1]) == int)
        maze.set_entrance(*entrance_coordinates)
        assert (type(exit_coordinates) == tuple)
        assert (type(exit_coordinates[0]) == int)
        assert (type(exit_coordinates[1]) == int)
        maze.set_exit(*exit_coordinates)
        assert (type(history) == list)
        for entry in history:
            assert (type(entry) == str)
            maze._log_action(entry)
        return maze

    def _log_action(self, title):
        self._history.append(title)
        return

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

    def name(self):
        """Generate human-readable name for the maze."""
        size = f"{self.width}" if self.width==self.height else f"{self.width}x{self.height}"
        history = '-'.join(self._history)
        string = f"maze{size}_{history}"
        return string

    def nodes(self):
        """Produce iterator over the nodes of the maze."""
        return itertools.chain(*self._grid)

    def edges(self):
        """Produce iterator over the edges of the maze."""
        edge_iterators = []
        rows = self._grid
        rows_below = iter(rows) ; next(rows_below)
        for row,row_below in zip(rows,rows_below):
            row_shifted_right = iter(row) ; next(row_shifted_right)
            edge_iterators.append(zip(row,row_shifted_right))
            edge_iterators.append(zip(row,row_below))
        return itertools.chain(*edge_iterators)

    def set_entrance(self, x, y):
        self._solution = None
        self._entrance = self.node_at(x,y)
        return

    def set_exit(self, x, y):
        self._solution = None
        self._exit = self.node_at(x,y)
        return

    def node_at(self, x, y):
        """Get node at those coordinates in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height

        Returns:
            Node: Node object at position (x,y) in maze
        """
        #if not (0 <= x < self.width and 0 <= y < self.height):
            #raise ValueError("coordinates not within boundaries")
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

    def has_wall(self, x, y, direction):
        """Check for a wall, facing some direction at some location in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height
            direction (int) : One of (RIGHT,UP,LEFT,DOWN) = (1,2,4,8)

        Returns:
            bool: Whether there is a wall when facing direction from (x,y) in maze
        """
        return self.node_at(x,y).has_wall(direction)

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
        elif connected is True:
            if 0<x             and node.has_edge(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_edge(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_edge(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_edge(DOWN):  yield self.node_at(x,y+1)
        elif connected is False:
            if 0<x             and node.has_wall(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_wall(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_wall(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_wall(DOWN):  yield self.node_at(x,y+1)

    def make_unicursal(self):
        """Convert self into a unicursal/ maze by removing no dead ends."""
        for node in self.nodes():
            while sum(1 for _ in self.adjacent_to(node,connected=True)) <= 1:
                neighbor = random.choice(list(self.adjacent_to(node,connected=False)))
                self.connect(node,neighbor)
                progressed = True # NOTE icky
        if progressed:self._log_action("unicursal")
        return

    def has_solution(self):
        if self._solution is None:
            return None
        if len(self._solution) == 0:
            return False
        else:
            return True

    def breadth_first_search(self):
        """Compute all node distances and draw in the shortest path in a maze.

        Args:
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is (0,0))
        """
        for node in self.nodes():
            node.distance = float('inf')
        queue = collections.deque(maxlen=3*max(self.width,self.height))
        queue.append(self._entrance)
        self._entrance.distance = 0
        while queue:
            node = queue.popleft()
            neighbors = list(self.adjacent_to(node,connected=True))
            for neighbor in neighbors:
                if neighbor.distance == float('inf'):
                    queue.append(neighbor)
                    neighbor.distance = node.distance + 1
        self._solution = set()
        if self._exit.distance == float('inf'):
            return
        current = self._exit
        while current != self._entrance:
            self._solution.add(current)
            current = min(self.adjacent_to(current,connected=True), default=False, key=lambda n:n.distance)
        self._solution.add(self._entrance)
        return

    def depth_first_search(self):
        start = self.node_at(0,0)
        visited = {start}
        startIter = self.adjacent_to(start,connected=True)
        startBestTs = []
        startRmtBest = (None,None,0)
        frame = [start,startIter,startBestTs,startRmtBest]
        stack = [frame]
        return_ = None
        while stack:
            #print(return_)#TESTING
            #for frame in stack:print(frame)#TESTING
            #print("---")
            # Load stackframe
            [curr,currIter,currBestTs,currRmtBest] = stack[-1]
            # Handle return value of child call by updating locals
            if return_ is not None:
                ((child,childDist), childRmtBest) = return_
                currBestTs.append((child,childDist+1))
                currBestTs.sort(key=lambda t:t[1],reverse=True)
                if len(currBestTs) == 3: currBestTs.pop()
                if currRmtBest[2] <= childRmtBest[2]:
                    stack[-1][3] = childRmtBest
            # Look at next neighbor
            for nbr in currIter:
                if nbr not in visited:
                    visited.add(curr)
                    # Prepare resursive call
                    nbrIter = self.adjacent_to(nbr,connected=True)
                    nbrBestTs = []
                    nbrRmtBest = (None,None,0)
                    frame = [nbr,nbrIter,nbrBestTs,nbrRmtBest]
                    stack.append(frame)
                    return_ = None
                    break
            # Gone through all neighbors, return value
            else:
                if currBestTs:
                    currT = currBestTs[0]
                else:
                    currT = (curr,0)
                if len(currBestTs) == 2:
                    currRmtBest2 = (currBestTs[0][0],currBestTs[1][0],currBestTs[0][1]+currBestTs[1][1])
                elif len(currBestTs) == 1:
                    currRmtBest2 = (curr,currBestTs[0][0],currBestTs[0][1])
                else:
                    currRmtBest2 = (curr,curr,0)
                if currRmtBest[2] <= currRmtBest2[2]:
                    currRmtBest = currRmtBest2
                stack.pop()
                return_ = (currT, currRmtBest)
            #for frame in stack:print(frame)#TESTING
            #print(return_)#TESTING
            #print(self.str_frame())#TESTING
        return return_[1]

    def generate_raster(self, corridorwidth=1, columnated=True, show_solution=False, show_distances=False): # TODO
        """
        normal:
            wall = +1  air = 0
        show_solution:
            wall = -1  air = 0  marker = [1,2..]
        show_distances:
            wall = -1  air = [0,1..]  unreachable = -1
        """
        """Return a simple 2D raster representation of the maze.

        Args:
            corridorwidth (int): Multiplier of how much wider corridors should be compared to the walls (default is 1)
            columnated (bool): Whether free-standing 'column' pieces should be placed in free 4x4 sections of the maze (default is True)

        Returns:
            list(list(bool)): 2D raster of the maze
        """
        wall = self.has_wall
        if show_solution and self.has_solution() is None:
            raise RuntimeError("cannot show solution path before searching for it")
        if show_distances:
            mkval = lambda is_wall, x,y: (-1) if is_wall or self.node_at(x,y).distance==float('inf') else self.node_at(x,y).distance
        elif show_solution and self._solution:
            mkval = lambda is_wall, x,y: (-1) if is_wall else self.node_at(x,y).distance + 1 if self.node_at(x,y) in self._solution else 0
        else:
            mkval = lambda is_wall, x,y: (+1) if is_wall else 0
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
    def raster_to_image(raster, value_to_color):
        colors = [value_to_color(value) for value in itertools.chain(*raster)]
        image = Image.new('RGB', (len(raster[0]),len(raster)))
        image.putdata(colors)
        return image

    def generate_image(self, wall_air_colors=(col.hex_to_tuple(0x000000),col.hex_to_tuple(0xFFFFFF))):
        """Generate a handle to a (PIL) Image object presenting the maze.

        Args:
            raster (list(list(bool))): Bit map to be rendered (default is self.generate_raster())
        """
        raster = self.generate_raster()
        # color conversion
        (wall_color, air_color) = wall_air_colors
        value_to_color = lambda value: wall_color if value else air_color
        # Convert to image
        image = Maze.raster_to_image(raster, value_to_color)
        return image

    def generate_solutionimage(self, wall_air_marker_colors=None):
        raster = self.generate_raster(show_solution=True)
        # color conversion
        if wall_air_marker_colors is None:
            peak = self._exit.distance or 1
            wall_color = col.hex_to_tuple(0x000000)
            air_color = col.hex_to_tuple(0xFFFFFF)
            marker_color = lambda value: col.convert((360*value/peak, 1, 1),'HSV','RGB')
            #marker_color = col.hex_to_tuple(0x007FFF)
        else:
            wall_color = wall_air_marker_colors[0]
            air_color = wall_air_marker_colors[1]
            marker_color = lambda value: wall_air_marker_colors[2]
        value_to_color = lambda value: wall_color if value==(-1) else air_color if value==0 else marker_color(value)
        # Convert to image
        image = Maze.raster_to_image(raster, value_to_color)
        return image

    def generate_colorimage(self, gradient_colors=None):
        raster = self.generate_raster(show_distances=True)
        # color conversion
        wall_color = col.hex_to_tuple(0x000000)
        if gradient_colors is None:
            hex_colors = [0xFFFFFF, 0x00007F, 0x7FFF00, 0x7F3F00, 0x7FCBFF, 0x7F00FF, 0xFFFF7F, 0x000000]
            #hex_colors = [0xFFFFFF, 0x003F7F, 0xFFFF7F, 0x7F003F]
            gradient_colors = list(col.hex_to_tuple(color) for color in hex_colors)
        air_color = lambda value: col.interpolate(gradient_colors, param=value/peak)
        peak = max(itertools.chain(*raster)) or 1
        value_to_color = lambda value: wall_color if value==(-1) else air_color(value)
        # Convert to image
        image = Maze.raster_to_image(raster, value_to_color)
        return image

    @staticmethod
    def raster_to_string(raster, value_to_chars):
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

    def str_frame_ascii(self, corridorwidth=1, show_solution=False):
        """Produce an (ASCII) frame string presentation of the maze.

        Args:
            corridorwidth (int): Multiplier of how much wider corridors should be compared to the walls (default is 1)
            show_marked_nodes (bool): Whether solution should be displayed if calculated (default is True)

        Returns:
            str: (ASCII) frame string presentation of the maze
        """
        if show_solution and self.has_solution() is None:
            raise RuntimeError("cannot show solution path before searching for it")
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
                row1 += [f' {"." if show_solution and node in self._solution else " "} '] * corridorwidth
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
    def random_edges(width, height, edge_probability=0.5):
        """Build a bogus maze by flipping a coin on every edge.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        maze = Maze(width,height)
        for edge in maze.edges():
            if random.random() < edge_probability:
                maze.connect(*edge)
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
        maze._log_action("wilson")
        return maze

    @staticmethod
    def division(width, height, slice_bias=1.0, pivot_choice=None):
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
        maze._log_action("division")
        return maze

# CLASSES END


# MAIN BEGIN
# No main
# MAIN END

# {{{ BEGIN END }}} ALERT ATTENTION DANGER HACK SECURITY BUG FIXME DEPRECATED TASK TODO TBD WARNING CAUTION NOLINT ### NOTE NOTICE TEST TESTING
