# OUTLINE BEGIN
"""
Contains the main `Maze` class,

This file contains all important maze-relation implementations to store, create and modify grid mazes.

### Ideas/Work in Progress:
- General
    * a l l   d o c s t r i n g s   m u s t   b e   c h e c k e d   ( p a i n )
    * (Is generate_raster rly bug-free??)
- Printers
    * PIL GIF
    * (? str_frame solution)
- Builders
    * (? compose algorithms)
- Solvers
    * A* pathfinder
- ETC Dreams
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
import colortools

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
        self.distance = float('inf')
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

    def remove_edge(self, direction):
        """Connect the node into the given directions."""
        self._edges &= ~direction

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
        * adjacent_to, connect, has_wall, node_at
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
    #_ALGORITHMS = {
            #0: ("unknown", Maze),
            #1: ("tree", Maze
                    #Maze.growing_tree,
                    #Maze.backtracker,
                    #Maze.prim,
                    #Maze.kruskal,
                    #Maze.wilson,
                    #Maze.division,
                    #Maze.random_edges
        #}

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
        self.entrance = self.node_at(0,0)
        self.exit = self.node_at(-1,-1)
        self.solution_nodes = None
        self._history = [time.strftime('%Y.%m.%d-%Hh%Mm%S')]

    def __repr__(self):
        string = (
            self._history,
            self.entrance.coordinates,
            self.exit.coordinates,
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
        for y in range(maze.height):    # `x` and `y` were swappe for these
            for x in range(maze.width): # two loops for a long time - epic bug
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
        history = '-'.join(self._history)
        size = f"{self.width}x{self.height}"
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
        self.entrance = self.node_at(x,y)
        return

    def set_exit(self, x, y):
        self.exit = self.node_at(x,y)
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

    def has_wall(self, x, y, direction):
        """Check for a wall, facing some direction at some location in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height
            direction (int) : One of (RIGHT,UP,LEFT,DOWN) = (1,2,4,8)

        Returns:
            bool: Whether there is a wall when facing direction from (x,y) in maze
        """
        return self.node_at(x,y).has_wall(direction)

    def connect(self, node0, node1, invert=False):
        """Toggle the connection between two nodes in the maze.

        Args:
            node0, node1 (Node): Two nodes in the maze that lie adjacent
        """
        (x0,y0), (x1,y1) = node0.coordinates, node1.coordinates
        dx, dy = x1-x0, y1-y0
        if abs(dx) + abs(dy) != 1:
            raise ValueError("nodes to connect must be neighbors")
        get_dir = lambda dx,dy: (LEFT if dx<0 else RIGHT) if dx else (UP if dy<0 else DOWN)
        if invert:
            node0.remove_edge(get_dir(dx,dy))
            node1.remove_edge(get_dir(-dx,-dy))
        else:
            node0.put_edge(get_dir(dx,dy))
            node1.put_edge(get_dir(-dx,-dy))
        return

    def adjacent_to(self, node):
        """Get all cells that are adjacent to node in the maze.

        Args:
            node (Node): Origin node
            connected (bool): Flag to additionally check cells for being connected or disconnected (default is None)

        Yields:
            Node: Neighboring node fulfilling conditions
        """
        (x,y) = node.coordinates
        if 0<x:             yield self.node_at(x-1,y)
        if x<self.width-1:  yield self.node_at(x+1,y)
        if 0<y:             yield self.node_at(x,y-1)
        if y<self.height-1: yield self.node_at(x,y+1)

    def connected_to(self, node, invert=False):
        (x,y) = node.coordinates
        if invert:
            if 0<x             and node.has_wall(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_wall(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_wall(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_wall(DOWN):  yield self.node_at(x,y+1)
        else:
            if 0<x             and node.has_edge(LEFT):  yield self.node_at(x-1,y)
            if x<self.width-1  and node.has_edge(RIGHT): yield self.node_at(x+1,y)
            if 0<y             and node.has_edge(UP):    yield self.node_at(x,y-1)
            if y<self.height-1 and node.has_edge(DOWN):  yield self.node_at(x,y+1)

    def _breadth_first_search(self, start, scanr=lambda _:None):
        queue = collections.deque(maxlen=3*max(self.width,self.height))
        queue.append(start)
        start.distance = 0 ; scanr(start)
        while queue:
            current = queue.popleft()
            neighbors = list(self.connected_to(current))
            for neighbor in neighbors:
                if neighbor.distance == float('inf'):
                    queue.append(neighbor)
                    neighbor.distance = current.distance + 1 ; scanr(neighbor)
        return

    def compute_distances(self, start_coord=None):
        """Compute all node distances using breadth first search.

        Args:
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is (0,0))
        """
        if start_coord is None:
            start = self.entrance
        else:
            start = self.node_at(*start_coord)
        for node in self.nodes():
            node.distance = float('inf')
        self._breadth_first_search(start)
        return

    def compute_branchdistances(self):
        for node in self.nodes():
            node.distance = float('inf')
        for node in self.nodes(): # TODO optimize
            if node.distance == float('inf'):
                node.distance = 0
                previous = None
                current = node
                while True:
                    neighbors = [nbr for nbr in self.connected_to(current) if nbr!=previous]
                    if len(neighbors) != 1:
                        break
                    previous = current
                    current = neighbors[0]
                    current.distance = previous.distance + 1
        return

    def compute_solution(self, recompute_distances=True):
        if recompute_distances:
            self.compute_distances()
        self.solution_nodes = set()
        if self.exit.distance == float('inf'):
            return
        current = self.exit
        self.solution_nodes.add(self.exit)
        while current != self.entrance:
            current = min(self.connected_to(current), default=False, key=lambda n:n.distance)
            self.solution_nodes.add(current)
        return

    def compute_stats(self):
        def nearest_branch_distance(node):
            dist = 0
            previous = None
            current = node
            while True:
                neighbors = [nbr for nbr in self.connected_to(current) if nbr!=previous]
                if len(neighbors) != 1:
                    break
                dist += 1
                previous = current
                current = neighbors[0]
            return dist
        is_dead_end = lambda node: (node._edges in [1,2,4,8])
        # Prepare accumulators for tiles and distance stats
        self.compute_solution()
        tiles_counts = [0 for _ in range(0b10000)]
        branch_distances = []
        for node in self.nodes():
            tiles_counts[node._edges] += 1
            if is_dead_end(node):
                branch_distances.append(nearest_branch_distance(node))
            # Preparation for next part
            if node not in self.solution_nodes:
                node.distance = float('inf')
        offshoots_maxlengths = []
        offshoots_avglengths = []
        for node in self.solution_nodes:
            for offshoot in self.connected_to(node):
                if offshoot not in self.solution_nodes:
                    lengths = []
                    length_adder = lambda n: lengths.append(n.distance) if is_dead_end(n) else None
                    self._breadth_first_search(offshoot, scanr=length_adder)
                    maxlength = max(lengths)
                    avglength = round(sum(lengths)/len(lengths))
                    offshoots_maxlengths.append(maxlength)
                    offshoots_avglengths.append(avglength)
        return (tiles_counts, branch_distances, offshoots_maxlengths, offshoots_avglengths)

    def set_longest_path(self):
        #remote_nodes = []
        #def add_to_remote_nodes(node):
            #if not remote_nodes:
                #remote_nodes.append(node)
            #else:
                #if remote_nodes[0].distance < node.distance:
                    #remote_nodes.clear()
                    #remote_nodes.append(node)
                #elif remote_nodes[0].distance == node.distance:
                    #remote_nodes.append(node)
                #elif remote_nodes[0].distance > node.distance:
                    #pass
        self.compute_distances()
        farthest = max(self.nodes(), key=lambda n:n.distance)
        self.entrance = farthest
        self.compute_distances()
        farthest = max(self.nodes(), key=lambda n:n.distance)
        self.exit = farthest
        return self.exit.distance

    def make_unicursal(self):
        """Convert self into a unicursal/ maze by removing no dead ends."""
        for node in self.nodes():
            while sum(1 for _ in self.connected_to(node)) <= 1:
                neighbor = random.choice(list(self.connected_to(node,invert=True)))
                self.connect(node,neighbor)
                progressed = True # NOTE icky
        if progressed:self._log_action("unicursal")
        return

    def generate_raster(self, wall_air_ratio=(1,1), columnated=True, show_solution=False, show_distances=False): # TODO wall_air_ratio
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
        (wallM, airM) = wall_air_ratio
        if columnated:
            column_wall = lambda x,y: True
        else:
            column_wall = lambda x,y: x==self.width-1 or y==self.height-1 or wall(x,y,RIGHT) or wall(x,y,DOWN) or wall(x+1,y+1,LEFT) or wall(x+1,y+1,UP)
        if show_solution:
            if self.solution_nodes is None:
                raise RuntimeError("cannot show solution path before computing it")
            mkval = lambda is_wall, x,y, nx,ny: (-1) if is_wall else self.node_at(x,y).distance + 1 if self.node_at(x,y) in self.solution_nodes and nx<self.width and ny<self.height and self.node_at(nx,ny) in self.solution_nodes else 0
        elif show_distances:
            if self.entrance.distance == float('inf'):
                raise RuntimeError("cannot show distances before computing them")
            mkval = lambda is_wall, x,y, nx,ny: (-1) if is_wall or self.node_at(x,y).distance==float('inf') else self.node_at(x,y).distance
        else:
            mkval = lambda is_wall, x,y, nx,ny: (+1) if is_wall else 0
        raster = []
        # Top-left corner
        row1 = [mkval(True, 0,0, 0,0)] * wallM
        # Top wall
        for x,node in enumerate(self._grid[0]):
            row1 += [mkval(node.has_wall(UP),x,0, x,0)] * airM
            row1 += [mkval(True,x,0, x,0)] * wallM
        raster += [row1] * wallM
        # Middle and bottom rows of string
        for y,row in enumerate(self._grid):
            # Left wall
            row1 = [mkval(row[0].has_wall(LEFT), 0,y, 0,y)] * wallM
            row2 = [mkval(True, 0,y, 0,y)] * wallM
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                row1 += [mkval(False, x,y, x,y)] * airM
                row1 += [mkval(node.has_wall(RIGHT), x,y, x+1,y)] * wallM
                row2 += [mkval(node.has_wall(DOWN), x,y, x,y+1)] * airM
                row2 += [mkval(column_wall(x,y), x,y, x,y)] * wallM
            raster += [row1] * airM
            raster += [row2] * wallM
        return raster

    @staticmethod
    def _raster_to_image(raster, value_to_color):
        colors = [value_to_color(value) for value in itertools.chain(*raster)]
        image = Image.new('RGB', (len(raster[0]),len(raster)))
        image.putdata(colors)
        return image

    def generate_image(self, wall_air_colors=(colortools.parse_hex('#000000'),colortools.parse_hex('#FFFFFF')), raster=None):
        """Generate a handle to a (PIL) Image object presenting the maze.

        Args:
            raster (list(list(bool))): Bit map to be rendered (default is self.generate_raster())
        """
        if raster is None:
            raster = self.generate_raster()
        # color conversion
        (wall_color, air_color) = wall_air_colors
        value_to_color = lambda value: wall_color if value else air_color
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}.png"
        return image

    def generate_solutionimage(self, wall_air_marker_colors=None, raster=None):
        if raster is None:
            if self.solution_nodes is None:
                self.compute_solution()
            raster = self.generate_raster(show_solution=True)
        # color conversion
        if wall_air_marker_colors is None:
            peak = self.exit.distance or 1
            wall_color = colortools.parse_hex('#000000')
            air_color = colortools.parse_hex('#FFFFFF')
            marker_color = lambda value: colortools.convert((360*value/peak, 1, 1),'HSV','RGB')
            #marker_color = colortools.parse_hex('#007FFF')
        else:
            wall_color = wall_air_marker_colors[0]
            air_color = wall_air_marker_colors[1]
            marker_color = lambda value: wall_air_marker_colors[2]
        value_to_color = lambda value: wall_color if value==(-1) else air_color if value==0 else marker_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_solution.png"
        return image

    def generate_colorimage(self, gradient_colors=None, raster=None):
        if raster is None:
            raster = self.generate_raster(show_distances=True)
        # color conversion
        wall_color = colortools.parse_hex('#000000')
        if gradient_colors is None:
            gradient_colors = colortools.COLORMAPS['viridis'][::-1]
        air_color = lambda value: colortools.interpolate(gradient_colors, param=value/peak)
        peak = max(itertools.chain(*raster)) or 1
        value_to_color = lambda value: wall_color if value==(-1) else air_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_distances.png"
        return image

    @staticmethod
    def _raster_to_string(raster, value_to_chars):
        string = '\n'.join(
            ''.join(
                value_to_chars(value) for value in row
            ) for row in raster
        )
        return string

    def str_raster(self, wall='#', air=None, raster=None):
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
        if raster is None:
            raster = self.generate_raster()
        value_to_chars = lambda value: wall if value else air
        string = Maze._raster_to_string(raster, value_to_chars)
        return string

    def str_block_double(self, raster=None):
        """Produce a wide (unicode) block string presentation of the maze."""
        return self.str_raster(wall='██', raster=raster)

    def str_block(self, raster=None):
        """Produce a (unicode) block string presentation of the maze."""
        return self.str_raster(wall='█',raster=raster)

    def str_block_half(self, raster=None):
        """Produce a (unicode) half-block string presentation of the maze."""
        if raster is None:
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

    def str_block_quarter(self, raster=None):
        """Produce a (unicode) quarter-block string presentation of the maze."""
        if raster is None:
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

    def str_frame_ascii(self, air_ratio=1, show_solution=False):
        """Produce an (ASCII) frame string presentation of the maze.

        Args:
            air_ratio (int): Multiplier of how much wider corridors should be compared to the walls (default is 1)
            show_marked_nodes (bool): Whether solution should be displayed if calculated (default is True)

        Returns:
            str: (ASCII) frame string presentation of the maze
        """
        if show_solution and self.solution_nodes is None:
            raise RuntimeError("cannot show solution path before searching for it")
        # Top-left corner
        linestr = [['+']]
        # Top wall
        for node in self._grid[0]:
            linestr[0] += ['---' if node.has_wall(UP) else '   '] * air_ratio
            linestr[0] += ['+']
        # Middle and bottom rows of string
        for row in self._grid:
            # Left wall
            row1 = ['|' if row[0].has_wall(LEFT) else ' ']
            row2 = ['+']
            # Middle and bottom walls (2 blocks/node)
            for node in row:
                row1 += [f' {"." if show_solution and node in self.solution_nodes else " "} '] * air_ratio
                row1 += ['|' if node.has_wall(RIGHT) else ' ']
                row2 += ['---' if node.has_wall(DOWN) else '   '] * air_ratio
                row2 += ['+']
            linestr += [row1] * air_ratio
            linestr += [row2]
        return '\n'.join(''.join(line) for line in linestr)

    def str_frame_ascii_small(self, show_solution=False, columnated=True):
        """Produce a minimal (ASCII) frame string presentation of the maze."""
        wall = self.has_wall
        if show_solution and self.solution_nodes is None:
            raise RuntimeError("cannot show solution path before searching for it")
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
            else: return '.' if columnated else ' '
        def cornersegment_top(x):
            if wall(x,0,RIGHT) and not (wall(x,0,UP) and x<self.width-1 and wall(x+1,0,UP)): return ','
            elif wall(x,0,UP) or (x<self.width-1 and wall(x+1,0,UP)): return '_'
            else: return '.' if columnated else ' '
        def cornersegment_left(y):
            if wall(0,y,LEFT): return '|'
            elif y!=self.height-1 and wall(0,y+1,LEFT): return ','
            elif wall(0,y,DOWN): return '_'
            else: return '.' if columnated else ' '
        def cornersegment(x, y):
            if wall(x,y,RIGHT): return '|'
            elif y<self.height-1 and wall(x,y+1,RIGHT) and not (wall(x,y,DOWN) and x<self.width-1 and wall(x+1,y,DOWN)): return ','
            elif wall(x,y,DOWN) or (x<self.width-1 and wall(x+1,y,DOWN)): return '_'
            else: return '.' if columnated else ' '
        def trsfm1(char):
            if show_solution and self.node_at(x,y) in self.solution_nodes:
                return {'_':'i', ' ':'!'}[char]
            else:
                return char
        def trsfm2(char):
            if show_solution and self.node_at(x,y) in self.solution_nodes and x<self.width-1 and self.node_at(x+1,y) in self.solution_nodes:
                return {'|':'|', ',':'i', '_':'i', '.':'!'}[char]
            else:
                return char

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
                string.append(trsfm1('_' if wall(x,y,DOWN) else ' '))
                string.append(trsfm2(cornersegment(x,y)))
        return ''.join(string)
#### print(maze.str_frame_ascii_small(show_solution=True))
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
            index_choice = lambda max_index: -1 if random.random()<0.75 else random.randint(0,max_index)
        start.flag = True
        bucket = [start]
        #### IMAGES = []
        while bucket:
            n = index_choice(len(bucket)-1)
            node = bucket[n]
            neighbors = [nb for nb in maze.adjacent_to(node) if not nb.flag]
            if neighbors:
                neighbor = random.choice(neighbors)
                maze.connect(node,neighbor)
                neighbor.flag = True
                bucket.append(neighbor)
                #### IMAGES.append(maze.generate_image(raster=maze.generate_raster(corridorwidth=3)))
            else:
                if fast_pop:
                    if len(bucket) > 1 and n != -1:
                        bucket[n],bucket[-1] = bucket[-1],bucket[n]
                    bucket.pop()
                else:
                    bucket.pop(n)
        maze._log_action("tree")
        #### IMAGES[0].save('test.gif', save_all=True, append_images=IMAGES[1:], optimize=True, duration=30, loop=0)
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
                prev_node = next(maze.connected_to(tail_node))
                maze.connect(tail_node,prev_node,invert=True)
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
    def division(width, height, slice_direction_choice=None, pivot_choice=None, roomlength=0):
        """Build a random maze using randomized divide-and-conquer.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            slice_bias (float): Probability (0<=slice_bias<=1) to do a reroll when dividing a quadrant along the same direction as parent call
            pivot_choice (callable(int,int) -> int): Function to choose a random index between given lower and upper index along which to make a cut
        """
        maze = Maze(width, height)
        if pivot_choice is None:
            pivot_choice = lambda l,r: (l+r)//2
            #pivot_choice = lambda l,r: min(max(l,int(random.gauss((l+r)/2,(l+r)/2**5))),r)
            #pivot_choice = lambda l,r: random.triangular(l,r)
            #pivot_choice = lambda l,r: random.randint(l,r)
        if slice_direction_choice is None:
            slice_direction_choice = lambda w,h, prev: h > w if h != w else random.getrandbits(1)
            #slice_direction_choice = lambda w,h, prev: prev ^ (random.random() < 1.9)
            #slice_direction_choice = lambda w,h, prev: random.getrandbits(1)
        def divide(topleft, bottomright, prev_dir):
            (x0,y0), (x1,y1) = topleft, bottomright
            width,height = (x1-x0), (y1-y0)
            if width < 1 or height < 1 or roomlength and width < roomlength and height < roomlength and random.random() < 1/(width*height): return
            horizontal_cut = slice_direction_choice(width, height, prev_dir)
            if horizontal_cut:
                yP = pivot_choice(y0,y1-1)
                for x in range(x0,x1+1):
                    maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1),invert=True)
                x = random.randint(x0,x1)
                maze.connect(maze.node_at(x,yP),maze.node_at(x,yP+1))
                divide((x0,y0), (x1,yP), True)
                divide((x0,yP+1), (x1,y1), True)
            else:
                xP = pivot_choice(x0,x1-1)
                for y in range(y0,y1+1):
                    maze.connect(maze.node_at(xP,y),maze.node_at(xP+1,y),invert=True)
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
