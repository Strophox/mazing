# BEGIN OUTLINE
"""
Contains the main `Maze` class,

This file contains all important maze-relation implementations to store, create and modify grid mazes.

### Ideas/Work in Progress:
- General
    * a l l   d o c s t r i n g s   m u s t   b e   c h e c k e d   ( p a i n )
    * (Is generate_raster rly bug-free??)
    * Learn numpy to optimize stuf
- Printers
    * Allow choosing of start node for animation
    * (? str_frame solution)
- Solvers
    * A* pathfinder
- ETC Dreams
    * curses maze navigator
    * CHALLENGE doom; "░▒▓█.,-~:;=!*#$@"
"""
# END   OUTLINE


# BEGIN IMPORTS

import random
import time # strftime
import collections # deque
from PIL import Image
import colortools

# END   IMPORTS


# BEGIN CONSTANTS

# Directions
RIGHT = 0b0001
UP    = 0b0010
LEFT  = 0b0100
DOWN  = 0b1000

# END   CONSTANTS


# BEGIN DECORATORS
# No decorators
# END   DECORATORS


# BEGIN CLASSES

class Node:
    """
    A class representing a maze grid cell/node.
    """
    def __init__(self, x, y):
        """Initialize a node by its grid coordinates."""
        self.flag = None
        self._coordinates = (x, y)
        self._distance = float('inf')
        self._mark = 'unidentified'
        self._edges = 0b0000

    def __repr__(self):
        return self._coordinates.__repr__()

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def distance(self):
        return self._distance

    @property
    def mark(self):
        return self._mark

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

    def __init__(self, width, height):
        """Initialize a node by its size.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        if not (width > 0 and height > 0):
            raise ValueError("Maze must have positive width and height")
        self._width  = width
        self._height = height
        self._grid = [[Node(x,y) for x in range(width)] for y in range(height)]
        self._solution_nodes = None
        self.entrance = self.node_at(0,0)
        self.exit = self.node_at(-1,-1)

    def __repr__(self):
        string = (
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
        return maze

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def solution(self):
        return self._solution_nodes#.copy()

    def name(self):
        """Generate human-readable name for the maze."""
        candidates = self.generate_algorithm_shares()
        main_algorithm = max(candidates,key=candidates.get)
        size = f"{self.width}x{self.height}"
        string = f"maze{size}_{main_algorithm}"
        return string

    def nodes(self, area=None):
        """Produce iterator over the nodes of the maze."""
        if area is None:
            return (node for row in self._grid for node in row)
        else:
            (x0,y0,x1,y1) = area
            return (node for row in self._grid[y0:y1+1] for node in row[x0:x1+1])

    def edges(self, area=None):
        """Produce iterator over the edges of the maze."""
        edge_iterators = []
        if area is None:
            rows = self._grid
            # Horizontal edges
            for row in rows:
                row_shifted_right = iter(row) ; next(row_shifted_right)
                edge_iterators.append(zip(row,row_shifted_right))
            # Vertical edges
            rows_below = iter(rows) ; next(rows_below)
            for row,row_below in zip(rows,rows_below):
                edge_iterators.append(zip(row,row_below))
        else:
            (x0,y0,x1,y1) = area
            edge_iterators = []
            # Horizontal edges
            rows_slice = self._grid[y0:y1+1]
            for row in rows_slice:
                row_slice = row[x0:x1+1]
                row_slice_right = row[x0+1:x1+1]
                edges = zip(row_slice,row_slice_right)
                edge_iterators.append(edges)
            # Vertical edges
            rows_slice_below = self._grid[y0+1:y1+1]
            for row,row_below in zip(rows_slice,rows_slice_below):
                row_slice = row[x0:x1+1]
                row_slice_below = row_below[x0:x1+1]
                edges = zip(row_slice,row_slice_below)
                edge_iterators.append(edges)
        return (edge for itr in edge_iterators for edge in itr)

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

    def connect(self, item0, item1, invert=False):
        """Toggle the connection between two nodes in the maze.

        Args:
            node0, node1 (Node): Two nodes in the maze that lie adjacent
        """
        if isinstance(item0, Node):
            node0, node1 = item0, item1
            (x0,y0), (x1,y1) = item0.coordinates, item1.coordinates
        else:
            node0, node1 = self.node_at(*item0), self.node_at(*item1)
            (x0,y0), (x1,y1) = item0, item1
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

    def adjacent_to(self, node, area=None):
        """Get all cells that are adjacent to node in the maze.

        Args:
            node (Node): Origin node
            connected (bool): Flag to additionally check cells for being connected or disconnected (default is None)

        Yields:
            Node: Neighboring node fulfilling conditions
        """
        (x,y) = node.coordinates
        if area is None:
            (x0,y0,x1,y1) = (0,0,self.width-1,self.height-1)
        else:
            (x0,y0,x1,y1) = area
        if x0 < x: yield self.node_at(x-1,y)
        if x < x1: yield self.node_at(x+1,y)
        if y0 < y: yield self.node_at(x,y-1)
        if y < y1: yield self.node_at(x,y+1)

    def connected_to(self, node, area=None, invert=False):
        (x,y) = node.coordinates
        if area is None:
            (x0,y0,x1,y1) = (0,0,self.width-1,self.height-1)
        else:
            (x0,y0,x1,y1) = area
        if invert:
            if x0 < x and node.has_wall(LEFT):  yield self.node_at(x-1,y)
            if x < x1 and node.has_wall(RIGHT): yield self.node_at(x+1,y)
            if y0 < y and node.has_wall(UP):    yield self.node_at(x,y-1)
            if y < y1 and node.has_wall(DOWN):  yield self.node_at(x,y+1)
        else:
            if x0 < x and node.has_edge(LEFT):  yield self.node_at(x-1,y)
            if x < x1 and node.has_edge(RIGHT): yield self.node_at(x+1,y)
            if y0 < y and node.has_edge(UP):    yield self.node_at(x,y-1)
            if y < y1 and node.has_edge(DOWN):  yield self.node_at(x,y+1)

    def _breadth_first_search(self, start, scanr=lambda _:None):
        if start.distance != float('inf'):
            return
        queue = collections.deque(maxlen=3*max(self.width,self.height))
        queue.append(start)
        start._distance = 0 ; scanr(start)
        while queue:
            current = queue.popleft()
            neighbors = list(self.connected_to(current))
            for neighbor in neighbors:
                if neighbor.distance == float('inf'):
                    queue.append(neighbor)
                    neighbor._distance = current.distance + 1 ; scanr(neighbor)
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
            node._distance = float('inf')
        self._breadth_first_search(start)
        return

    def compute_branchdistances(self):
        for node in self.nodes():
            node._distance = float('inf')
        for node in self.nodes(): # TODO optimize
            if node.distance == float('inf'):
                previous = None
                current = node
                if node._edges in [1,2,4,8]: node._distance = 0 # ugly hack
                while True:
                    neighbors = [nbr for nbr in self.connected_to(current) if nbr!=previous]
                    if len(neighbors) != 1:
                        break
                    previous = current
                    current = neighbors[0]
                    current._distance = previous.distance + 1
        return

    def compute_solution(self, recompute_distances=True):
        if recompute_distances:
            self.compute_distances()
        self._solution_nodes = set()
        if self.exit.distance == float('inf'):
            return
        current = self.exit
        self._solution_nodes.add(self.exit)
        while current != self.entrance:
            current = min(self.connected_to(current), default=False, key=lambda n:n.distance)
            self._solution_nodes.add(current)
        return

    def compute_longest_path(self):
        for node in self.nodes():
            node._distance = float('inf')
        global counter
        counter = 0
        def increment_counter(n):
            global counter
            counter += 1
        for node in self.nodes():
            if counter == self.width*self.height:
                break
            self._breadth_first_search(node, scanr=increment_counter)
        finite_nodes = [n for n in self.nodes() if n.distance<float('inf')]
        farthest = max(finite_nodes, key=lambda n:n.distance)
        self.entrance = farthest
        for node in self.nodes():
            node._distance = float('inf')
        self._breadth_first_search(self.entrance)
        finite_nodes = [n for n in self.nodes() if n.distance<float('inf')]
        farthest = max(finite_nodes, key=lambda n:n.distance)
        self.exit = farthest
        return self.exit.distance

    def make_unicursal(self):
        """Convert self into a unicursal/ maze by removing no dead ends."""
        for node in self.nodes():
            while sum(1 for _ in self.connected_to(node)) <= 1:
                neighbor = random.choice(list(self.connected_to(node,invert=True)))
                self.connect(node,neighbor)
        return

    def generate_algorithm_shares(self):
        null_cat = 'unidentified'
        algorithm_shares = {name:0 for name in Maze.ALGORITHMS}
        algorithm_shares[null_cat] = 0
        for node in self.nodes():
            if node.mark in algorithm_shares:
                algorithm_shares[node.mark] += 1
            else:
                algorithm_shares[null_cat] += 1
        return algorithm_shares

    def generate_stats(self):
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
            if node not in self._solution_nodes:
                node._distance = float('inf')
        if tiles_counts[0b0001]+tiles_counts[0b0010]+tiles_counts[0b0100]+tiles_counts[0b1000] == 0:
            raise ValueError("maze has no dead ends, aborting analysis")
        offshoots_maxlengths = []
        offshoots_avglengths = []
        for node in self._solution_nodes:
            for offshoot in self.connected_to(node):
                if offshoot not in self._solution_nodes:
                    lengths = []
                    length_adder = lambda n: lengths.append(n.distance) if is_dead_end(n) else None
                    self._breadth_first_search(offshoot, scanr=length_adder)
                    maxlength = max(lengths, default=0)
                    avglength = round(sum(lengths)/len(lengths))
                    offshoots_maxlengths.append(maxlength)
                    offshoots_avglengths.append(avglength)
        return (tiles_counts, branch_distances, offshoots_maxlengths, offshoots_avglengths)

    def generate_raster(self, wall_air_ratio=(1,1), columnated=True, show_solution=False, show_distances=False, show_algorithms=False): # TODO wall_air_ratio
        """
        normal:
            wall = +1  air = 0
        show_solution:
            wall = -1  air = 0  marker = [1,2..]
        show_distances:
            wall = -1  air = [0,1..]  unreachable = -2
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
            if self._solution_nodes is None:
                raise RuntimeError("cannot show solution path before computing it")
            mkval = lambda is_wall, x,y, nx,ny: (-1) if is_wall else self.node_at(x,y).distance + 1 if self.node_at(x,y) in self._solution_nodes and nx<self.width and ny<self.height and self.node_at(nx,ny) in self._solution_nodes else 0
        elif show_distances:
            mkval = lambda is_wall, x,y, nx,ny: (-1) if is_wall else (-2) if self.node_at(x,y).distance==float('inf') else self.node_at(x,y).distance
        elif show_algorithms:
            mkval = lambda is_wall, x,y, nx,ny: 'wall' if is_wall else self.node_at(x,y).mark
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
        colors = [value_to_color(value) for row in raster for value in row]
        image = Image.new('RGB', (len(raster[0]),len(raster)))
        image.putdata(colors)
        return image

    def generate_image(self, wall_air_colors=(colortools.BLACK,colortools.WHITE), raster=None):
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
        image.filename = f"{self.name()}_{time.strftime('%Y.%m.%d-%Hh%Mm%S')}.png"
        return image

    def generate_solutionimage(self, wall_air_marker_colors=None, raster=None):
        if raster is None:
            if self._solution_nodes is None:
                self.compute_solution()
            raster = self.generate_raster(show_solution=True)
        # color conversion
        if wall_air_marker_colors is None:
            peak = self.exit.distance or 1
            wall_color = colortools.BLACK
            air_color = colortools.WHITE
            marker_color = lambda value: colortools.rainbow(value/peak, colortools.VIOLET, 'lch_ab')
            #marker_color = lambda value: colortools.change_space((360*value/peak, 1, 1),'HSV','RGB')
            #marker_color = colortools.BLUE
        else:
            wall_color = wall_air_marker_colors[0]
            air_color = wall_air_marker_colors[1]
            marker_color = lambda value: wall_air_marker_colors[2]
        value_to_color = lambda value: wall_color if value==(-1) else air_color if value==0 else marker_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_sol_{time.strftime('%Y.%m.%d-%Hh%Mm%S')}.png"
        return image

    def generate_colorimage(self, gradient_colors=None, raster=None):
        if raster is None:
            raster = self.generate_raster(show_distances=True)
        # color conversion
        wall_color = colortools.BLACK
        unreachable_color = colortools.DARK_GRAY
        if gradient_colors is None:
            gradient_colors = colortools.COLORMAPS['viridis'][::-1]
        air_color = lambda value: colortools.interpolate(gradient_colors, param=value/peak)
        peak = max(val for row in raster for val in row) or 1
        value_to_color = lambda value: wall_color if value==(-1) else unreachable_color if value==(-2) else air_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_dist_{time.strftime('%Y.%m.%d-%Hh%Mm%S')}.png"
        return image

    def generate_algorithmimage(self, raster=None):
        if raster is None:
            raster = self.generate_raster(show_algorithms=True)
        coloring = {
            'wall': colortools.BLACK,
            'unidentified': colortools.GRAY,
            'random_edges': colortools.LIGHT_GRAY,
            'growing_tree': colortools.MOSS,
            'backtracker':  colortools.BLUE,
            'prim':         colortools.CRIMSON,
            'kruskal':      colortools.GOLDENROD,
            'wilson':       colortools.mix(colortools.VIOLET,colortools.PURPLE),
            'division':     colortools.WHITE,
        }
        value_to_color = lambda value: coloring[value]
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_algo_{time.strftime('%Y.%m.%d-%Hh%Mm%S')}.png"
        return image

    @staticmethod
    def save_animation(width, height, maze_runner, image_generator=None, frame_only=1, frame_ms=30, alert_progress_steps=0):
        if image_generator is None:
            image_generator = lambda maze:maze.compute_distances() and()or maze.generate_colorimage(raster=maze.generate_raster(show_distances=True,wall_air_ratio=(1,3)))
            #image_generator = lambda maze:maze.generate_image(raster=maze.generate_raster())
        global counter, frames, n_progress_milestone
        counter = int()
        frames = list()
        frame_total = (width * height) // frame_only
        n_progress_milestone = frame_total//alert_progress_steps if alert_progress_steps > 0 else None
        def record_frame(maze):
            global counter, frames
            counter += 1
            if counter % frame_only == 0:
                frame = image_generator(maze)
                frames.append(frame)
                if alert_progress_steps and counter//frame_only % n_progress_milestone == 0:
                    print(f"{counter} visits made (expect > {frame_total})")
        maze = Maze(width,height)
        maze_runner(maze, record_frame)
        frames.append(image_generator(maze))
        filename = f"{maze.name()}_anim_{time.strftime('%Y.%m.%d-%Hh%Mm%S')}.gif"
        mainframe = frames[0] # lol
        mainframe.save(
            filename,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=frame_ms,
            #loop=0,
        )
        return (filename, maze)

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
        if show_solution and self._solution_nodes is None:
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
                row1 += [f' {"." if show_solution and node in self._solution_nodes else " "} '] * air_ratio
                row1 += ['|' if node.has_wall(RIGHT) else ' ']
                row2 += ['---' if node.has_wall(DOWN) else '   '] * air_ratio
                row2 += ['+']
            linestr += [row1] * air_ratio
            linestr += [row2]
        return '\n'.join(''.join(line) for line in linestr)

    def str_frame_ascii_small(self, show_solution=False, columnated=True):
        """Produce a minimal (ASCII) frame string presentation of the maze."""
        wall = self.has_wall
        if show_solution and self._solution_nodes is None:
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
            if show_solution and self.node_at(x,y) in self._solution_nodes:
                return {'_':'i', ' ':'!'}[char]
            else:
                return char
        def trsfm2(char):
            if show_solution and self.node_at(x,y) in self._solution_nodes and x<self.width-1 and self.node_at(x+1,y) in self._solution_nodes:
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

    def randomize_edges(self, area=None, edge_probability=0.5, record_frame=None):
        """Build a bogus maze by flipping a coin on every edge.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        mark = 'random_edges'
        if record_frame is None:
            record_frame = lambda maze:None
        record_frame(self)
        for (node0,node1) in self.edges(area):
            node0._mark = node1._mark = mark
            if random.random() < edge_probability:
                self.connect(node0,node1)
                record_frame(self)
        return

    def grow_tree(self, area=None, start_coord=None, name_index_choice=None, fast_pop=False, record_frame=None):
        """Build a random maze using the '(random) growing tree' algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
            index_choice (callable(int) -> int): Function to pick an index between 0 and a given max_index, used to determine behaviour of the algorithm (default is lambda max_index: -1 if random.random()<0.95 else random.randint(0,max_index))
            fast_pop (bool): Whether to switch chosen element with last element when removing from active set. This is to speed up generation of large, random mazes (default is False)
        """
        if area is None:
            (x0,y0,x1,y1) = (0,0,self.width-1,self.height-1)
        else:
            (x0,y0,x1,y1) = area
        if start_coord is None:
            start_coord = (random.randint(x0,x1),random.randint(y0,y1))
        if name_index_choice is None:
            name = 'growing_tree'
            index_choice = lambda max_index: -1 if random.random()<0.70 else random.randint(0,max_index)
        else:
            (name,index_choice) = name_index_choice
            #algorithm_variant = (lambda self,area=None,start_coord=None,fast_pop=False:
                #Maze.grow_tree(self,area=area,start_coord=start_coord,name_index_choice=name_index_choice,fast_pop=fast_pop))
            #Maze.algorithms[name] = algorithm_variant
        mark = name
        if record_frame is None:
            record_frame = lambda maze:None
        start = self.node_at(*start_coord)
        start.flag = True
        start._mark = mark
        active_set = [start]
        record_frame(self)
        while active_set:
            idx = index_choice(len(active_set)-1)
            node = active_set[idx]
            if (neighbors:=[nbr for nbr in self.adjacent_to(node, area) if not nbr.flag]):
                neighbor = random.choice(neighbors)
                self.connect(node, neighbor)
                neighbor.flag = True
                neighbor._mark = mark
                active_set.append(neighbor)
                record_frame(self)
            else:
                if fast_pop:
                    if len(active_set) > 1 and idx != -1:
                        active_set[idx],active_set[-1] = active_set[-1],active_set[idx]
                    active_set.pop()
                else:
                    active_set.pop(idx)
        return

    def run_prim(self, area=None, start_coord=None, record_frame=None):
        """Build a random maze using randomized Prim's algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        name_index_choice = ('prim',
            lambda max_index: random.randint(0,max_index))
        self.grow_tree(
            area=area,
            start_coord=start_coord,
            name_index_choice=name_index_choice,
            fast_pop=False,
            record_frame=record_frame
        )
        return

    def run_backtrack(self, area=None, start_coord=None, record_frame=None):
        """Build a random maze using randomized depth first search.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        name_index_choice = ('backtracker',
            lambda max_index: -1)
        self.grow_tree(
            area=area,
            start_coord=start_coord,
            name_index_choice=name_index_choice,
            fast_pop=False,
            record_frame=record_frame
        )
        return

    def run_kruskal(self, area=None, record_frame=None):
        """Build a random maze using randomized Kruskal's algorithm.

        Args:
            width, height (int): Positive integer dimensions of desired maze
        """
        mark = 'kruskal'
        if area is None:
            nodecount = self.width * self.height
        else:
            nodecount = (area[2]-area[0]+1) * (area[3]-area[1]+1)
        if record_frame is None:
            record_frame = lambda maze:None
        edges = list(self.edges(area))
        random.shuffle(edges)
        members = dict()
        record_frame(self)
        for (node0,node1) in edges:
            node0._mark = node1._mark = mark
            if not all([node0.flag,node1.flag]) or node0.flag != node1.flag:
                if not node0.flag:
                    node0.flag, members[node0] = node0, [node0]
                if not node1.flag:
                    node1.flag, members[node1] = node1, [node1]
                self.connect(node0, node1)
                record_frame(self)
                if len(members[node0.flag]) < len(members[node1.flag]):
                    smaller,bigger = node0,node1
                else:
                    smaller,bigger = node1,node0
                for node in members[smaller.flag]:
                    node.flag = bigger.flag
                    members[bigger.flag].append(node)
                if len(members[bigger.flag])==nodecount:
                    break
        return

    def run_wilson(self, area=None, start_coord=None, record_frame=None):
        """Build a random maze using Wilson's uniform spanning tree algorithm..

        Args:
            width, height (int): Positive integer dimensions of desired maze
            start_coord (int,int): Coordinates with 0<=x<width && 0<=y<height (default is random)
        """
        mark = 'wilson'
        if area is None:
            (x0,y0,x1,y1) = (0,0,self.width-1,self.height-1)
        else:
            (x0,y0,x1,y1) = area
        if record_frame is None:
            record_frame = lambda maze:None
        def backtrack_path(tail_node, origin):
            while tail_node != origin:
                prev_node = next(self.connected_to(tail_node, area))
                self.connect(tail_node, prev_node, invert=True)
                tail_node.flag = 0
                tail_node = prev_node
        if start_coord is None:
            start = self.node_at((x1+x0)//2, (y1+y0)//2)
        else:
            start = self.node_at(*start_coord)
        nodes = list(self.nodes(area))
        generation = 1
        start.flag = generation
        random.shuffle(nodes)
        record_frame(self)
        for node in nodes:
            node._mark = mark
            if not node.flag:
                generation += 1
                node.flag = generation
                curr_node = node
                while True:
                    next_node = random.choice(list(self.adjacent_to(curr_node, area)))
                    if not next_node.flag:
                        next_node.flag = generation
                        self.connect(curr_node, next_node)
                        record_frame(self)
                        curr_node = next_node
                    elif next_node.flag == generation:
                        backtrack_path(curr_node,next_node)
                        record_frame(self)
                        curr_node = next_node
                    elif next_node.flag < generation:
                        self.connect(curr_node,next_node)
                        record_frame(self)
                        break
        return

    def run_division(self, area=None, slice_direction_choice=None, pivot_choice=None, roomlength=0, nest_algorithms=[], record_frame=None):
        """Build a random maze using randomized divide-and-conquer.

        Args:
            width, height (int): Positive integer dimensions of desired maze
            slice_bias (float): Probability (0<=slice_bias<=1) to do a reroll when dividing a quadrant along the same direction as parent call
            pivot_choice (callable(int,int) -> int): Function to choose a random index between given lower and upper index along which to make a cut
        """
        mark = 'division'
        if area is None:
            area = (0,0,self.width-1,self.height-1)
        if pivot_choice is None:
            #pivot_choice = lambda l,r: (l+r)//2
            pivot_choice = lambda l,r: min(max(l,int(random.gauss((l+r)/2,(l+r)/2**7))),r)
            #pivot_choice = lambda l,r: random.triangular(l,r)
            #pivot_choice = lambda l,r: random.randint(l,r)
        if slice_direction_choice is None:
            slice_direction_choice = lambda w,h, prev: h > w if h != w else random.getrandbits(1)
            #slice_direction_choice = lambda w,h, prev: prev ^ (random.random() < 1.9)
            #slice_direction_choice = lambda w,h, prev: random.getrandbits(1)
        if record_frame is None:
            record_frame = lambda maze:None
        def divide(area, prev_dir):
            (x0,y0,x1,y1) = area
            ewidth, eheight = (x1-x0), (y1-y0)
            if ewidth < 1 or eheight < 1 or roomlength and ewidth < roomlength and eheight < roomlength and random.random() < 1/((ewidth+1)*(eheight+1))**.5:
                if ewidth < 1 or eheight < 1 or not nest_algorithms:
                    for x in range(x0,x1+1):
                        for y in range(y0,y1+1):
                            self.node_at(x,y)._mark = mark
                            if x < x1:
                                self.node_at(x+1,y)._mark = mark
                                self.connect((x,y),(x+1,y))
                            if y < y1:
                                self.node_at(x,y+1)._mark = mark
                                self.connect((x,y),(x,y+1))
                            record_frame(self)
                else:
                    random.choice(nest_algorithms)(self, area=area, record_frame=record_frame)
                return
            cut_horizontally = slice_direction_choice(ewidth, eheight, prev_dir)
            if cut_horizontally:
                yP = pivot_choice(y0,y1-1)
                x = random.randint(x0,x1)
                self.node_at(x,yP)._mark = mark
                self.node_at(x,yP+1)._mark = mark
                self.connect((x,yP),(x,yP+1))
                record_frame(self)
                divide((x0,y0,x1,yP), True)
                divide((x0,yP+1,x1,y1), True)
            else:
                xP = pivot_choice(x0,x1-1)
                y = random.randint(y0,y1)
                self.node_at(xP,y)._mark = mark
                self.node_at(xP+1,y)._mark = mark
                self.connect((xP,y),(xP+1,y))
                record_frame(self)
                divide((x0,y0,xP,y1), False)
                divide((xP+1,y0,x1,y1), False)
        zeroth_cut = self.width < self.height
        divide(area, zeroth_cut)
        return

    ALGORITHMS = {
        'random_edges':
            randomize_edges,
        'growing_tree':
            grow_tree,
        'backtracker':
            run_backtrack,
        'prim':
            run_prim,
        'kruskal':
            run_kruskal,
        'wilson':
            run_wilson,
        'division':
            run_division,
        'xdivision':
            (lambda maze, area=None, record_frame=None: Maze.run_division(maze,roomlength=float('inf'),nest_algorithms=list(alg for name,alg in Maze.ALGORITHMS.items() if name not in {'random_edges','xdivision'}),area=area,record_frame=record_frame))
    }

# END   CLASSES


# BEGIN MAIN
# No main
# END   MAIN
