# BEGIN OUTLINE
"""
Module implementing broadly interactable `Maze` object.

Comprehensive list of public interface methods:
- Building & Main Modification.
    + Algorithms.
        * clear
        * random_edges
        * growing_tree
        * backtracker
        * prim
        * kruskal
        * wilson
        * division
        * xdivision
    + Modification algorithms.
        * make_unicursal
- Generating Strings.
    * str_block
    * str_block_half
    * str_block_quarter
    * str_pipes
    * str_frame
    * str_frame_ascii
    * str_frame_ascii_small
- Generating Data.
    + Information
        * generate_algorithm_shares
        * generate_stats
        * generate_raster
    + Images.
        * generate_image
        * generate_solutionimage
        * generate_colorimage
        * generate_algorithmimage
    + Animations.
        * generate_animation (staticmethod)
- Computations & Light Modifications.
    * set_entrance, set_exit
    * compute_solution
    * compute_distances
    * compute_branchdistances
    * compute_longest_path
- 'Low-level.'
    + Magics.
        * __init__, __repr__
    + Parser.
        * from_repr (staticmethod)
    + Read-only properties.
        * width, height, solution
    + Other access.
        * name, nodes, edges
        * node_at, has_wall, adjacent_to, connected_to
        * connect

NOTE - Ideas in Progress:
- Solvers
    * A* pathfinder
- ETC Dreams
    * CHALLENGE doom; "░▒▓█.,-~:;=!*#$@"
    * curses maze navigator
"""
# END   OUTLINE


# BEGIN IMPORTS

import random
import time # strftime
import collections # deque, OrderedDict
import colortools as ct
from PIL import Image

# END   IMPORTS


# BEGIN CONSTANTS

ALGORITHMS = collections.OrderedDict()
"""Public list of available maze algorithms."""

# Directions
RIGHT = 0b0001
UP    = 0b0010
LEFT  = 0b0100
DOWN  = 0b1000

_INFINITY = float('inf')

# END   CONSTANTS


# BEGIN DECORATORS

def maze_algorithm(f):
    """Maze algorithm decorator: add to ALGORITHMS."""
    ALGORITHMS[f.__name__] = f
    return f

# END   DECORATORS


# BEGIN CLASSES

class Node:
    """
    A class representing a rectangular grid cell / maze node.
    """
    def __init__(self, x, y):
        """Initialize a node by its grid coordinates."""
        self.flag = None
        self._coordinates = (x, y)
        self._distance = _INFINITY
        self._alg_id = 0
        self._edges = 0b0000

    def __repr__(self):
        return self._coordinates.__repr__()

    @property
    def coordinates(self):
        """Location of node."""
        return self._coordinates

    @property
    def distance(self):
        """Distance of node to some target."""
        return self._distance

    def has_wall(self, direction):
        """Check whether there is a wall in some direction from the node."""
        return not (self._edges & direction)

    def has_edge(self, direction):
        """Check whether there is an edge in some direction from the node."""
        return self._edges & direction

    def set_edges(self, direction):
        """Set node to be connected exactly into the given direction(s)."""
        self._edges = direction

    def put_edge(self, direction):
        """Connect node into the given direction(s)."""
        self._edges |= direction

    def remove_edge(self, direction):
        """Connect node into the given directions."""
        self._edges &= ~direction

    def toggle_edge(self, direction):
        """Connect/disconnect node into the given directions."""
        self._edges ^= direction

class Maze:
    """
    A class to store and interact with a maze grid.

    All methods of this class fall into these broad categories:
    - Lower-level Interaction
        *
    """

    def __init__(self, width, height):
        """Initialize an unmodified grid by size.

        Args:
            width, height (int): Positive integer dimensions of grid.

        Returns:
            Maze
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
            [
                [
                    node._edges + (node._alg_id << 4) for node in row
                ] for row in self._grid
            ],
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
        for y in range(maze.height):    # `x` and `y` were swapped for these
            for x in range(maze.width): #   two loops for a long time - epic bug
                assert (type(grid[y][x]) == int)
                raw = grid[y][x]
                node = maze.node_at(x,y)
                node._edges  = raw % 0b10000
                node._alg_id = raw // 0b10000
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
        """Width of the maze."""
        return self._width

    @property
    def height(self):
        """Height of the maze."""
        return self._height

    @property
    def solution(self):
        """Set of nodes on maze solution path. Empty if no solution."""
        return self._solution_nodes#.copy()

    def name(self):
        """Get a human-readable, informative shortname for the maze.

        Returns:
            str"""
        candidates = self.generate_algorithm_shares()
        main_algorithm = f"{max(candidates,key=candidates.get)}".replace(' ','-')
        size = f"{self.width}x{self.height}"
        string = f"maze_{main_algorithm}-{size}"
        return string

    def _stamp(self):
        """Get a timestamp as str."""
        # return f"{random.getrandbits(32):032b}"
        return time.strftime('%Y.%m.%d-%Hh%Mm%S')

    def nodes(self, area=None):
        """Produce iterator over the `Node`s of the maze.

        Args:
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0),
                and bottom (x1,y1) corner within which to return nodes from.
                (default is (0,0, self.width-1,self.height-1))
        Returns:
            iter(Node): Iterator over nodes.
        """
        if area is None:
            return (node for row in self._grid for node in row)
        else:
            (x0,y0,x1,y1) = area
            return (node for row in self._grid[y0:y1+1] for node in row[x0:x1+1])

    def edges(self, area=None):
        """Produce iterator over the edges of the maze.

        Args:
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0),
                and bottom (x1,y1) corner within which to return edges from,
                that don't cross outside.
                (default is (0,0, self.width-1,self.height-1))
        Returns:
            iter(tuple(Node,Node)): Iterator over 'edges'.
        """
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

    def node_at(self, x, y):
        """Access node at those coordinates in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height

        Returns:
            Node: Node object at position (x,y) in maze
        """
        return self._grid[y][x]

    def has_wall(self, x, y, direction):
        """Check for wall when facing some direction at some node in the maze.

        Args:
            x, y (int): Coordinates with 0<=x<self.width && 0<=y<self.height
            direction (int): One of (RIGHT,UP,LEFT,DOWN) = (1,2,4,8)

        Returns:
            bool
        """
        return self.node_at(x,y).has_wall(direction)

    def adjacent_to(self, node, area=None):
        """Get all nodes that are adjacent to one in the maze.

        Args:
            node (Node): A node.
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to return
                adjacent's from (default is (0,0, self.width-1,self.height-1)).

        Yields:
            Node: Adjacent grid node within area.
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
        """Get all nodes that are connected to one in the maze.

        Args:
            node (Node): A node.
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to return
                neighbors from (default is (0,0, self.width-1,self.height-1)).

        Yields:
            Node: Neighboring grid node within area.
        """
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

    def connect(self, item0, item1, invert=False):
        """Enable/disable edge connection between two nodes in the maze.

        Args:
            node0, node1 (Node or tuple(int,int)): Two nodes in the maze that
                lie adjacent.
            invert (bool): Erase connection if True (default is False).
        """
        if type(item0) == tuple:
            node0, node1 = self.node_at(*item0), self.node_at(*item1)
            (x0,y0), (x1,y1) = item0, item1
        else: # Node
            node0, node1 = item0, item1
            (x0,y0), (x1,y1) = item0.coordinates, item1.coordinates
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

    def set_entrance(self, x, y):
        """Mark new entrance of maze."""
        self.entrance = self.node_at(x,y)
        return

    def set_exit(self, x, y):
        """Mark new exit of maze."""
        self.exit = self.node_at(x,y)
        return

    def _breadth_first_search(self, start, scanr=lambda _:None):
        """Start a breadth first search at some node in the maze.

        BFS won't start if start doesn't have infinite `distance`.
        Otherwise BFS will set the start distance to 0 and then look for
        unvisited nodes (distance infinity) until no more are found as usual.

        Args:
            start (Node): Node to start at.
            scanr (callable(Node)): Arbitrary function that gets called on every
                node exactly once (default: lambda _: None)
        """
        if start.distance < _INFINITY:
            return
        queue = collections.deque(maxlen=3*max(self.width,self.height))
        queue.append(start)
        start._distance = 0
        scanr(start)
        while queue:
            current = queue.popleft()
            neighbors = list(self.connected_to(current))
            for neighbor in neighbors:
                if neighbor.distance == _INFINITY:
                    queue.append(neighbor)
                    neighbor._distance = current.distance + 1
                    scanr(neighbor)
        return

    def compute_solution(self, recompute_distances=True):
        """Recompute distances and solve maze by backtracking.

        Args:
            recompute_distances (bool): Whether to recompute distances using
                `computer_distances` (default is True).
        """
        if recompute_distances:
            self.compute_distances()
        self._solution_nodes = set()
        if self.exit.distance == _INFINITY:
            return
        current = self.exit
        self._solution_nodes.add(self.exit)
        while current != self.entrance:
            current = min(self.connected_to(current), default=False, key=lambda n:n.distance)
            self._solution_nodes.add(current)
        return

    def compute_distances(self, start_coord=None):
        """Reset and compute all node distances within maze.

        Args:
            start_coord (int,int): Starting coordinates with
                0<=x<width && 0<=y<height (default is (0,0))
        """
        if start_coord is None:
            start = self.entrance
        else:
            start = self.node_at(*start_coord)
        for node in self.nodes():
            node._distance = _INFINITY
        self._breadth_first_search(start)
        return

    def compute_branchdistances(self):
        """Reset and compute all distances from nearest dead end within branch.

        This will compute the distance a node that are within a 'branch',
        i.e. between an intersection and a dead end.
        """
        for node in self.nodes():
            node._distance = _INFINITY
        for node in self.nodes():
            if node.distance == _INFINITY:
                previous = None
                previous_distance = -1
                current = node
                while True:
                    neighbors = [nbr for nbr in self.connected_to(current) if nbr!=previous]
                    if len(neighbors) != 1:
                        break
                    current._distance = previous_distance + 1
                    previous_distance = current._distance
                    previous = current
                    current = neighbors[0]
        return

    def compute_longest_path(self):
        """Compute and set as entrance&exit a longest path within the maze."""
        for node in self.nodes():
            node._distance = _INFINITY
        global counter
        counter = 0
        def increment_counter(n):
            global counter
            counter += 1
        for node in self.nodes():
            if counter == self.width*self.height:
                break
            self._breadth_first_search(node, scanr=increment_counter)
        finite_nodes = [n for n in self.nodes() if n.distance < _INFINITY]
        farthest = max(finite_nodes, key=lambda n:n.distance)
        self.entrance = farthest
        for node in self.nodes():
            node._distance = _INFINITY
        self._breadth_first_search(self.entrance)
        finite_nodes = [n for n in self.nodes() if n.distance < _INFINITY]
        farthest = max(finite_nodes, key=lambda n:n.distance)
        self.exit = farthest
        return self.exit.distance

    def generate_algorithm_shares(self):
        """Count number of nodes written by any algorithm.

        Returns:
            dict(str,int): A table of algorithm names and how many nodes
                they wrote/visited within the maze.
        """
        null_cat = 'unidentified'
        algorithm_amounts = [0] * len(ALGORITHMS)
        for node in self.nodes():
            if 0 <= node._alg_id < len(algorithm_amounts):
                algorithm_amounts[node._alg_id] += 1
        algorithm_shares = dict(zip(ALGORITHMS,algorithm_amounts))
        return algorithm_shares

    def generate_stats(self):
        """Compute some mildly interesting statistics about the maze.

        Returns:
            tuple(list(int),list(int),list(int)): The first list describes the
                numberof appearance of ach tile type [...]
                The second is a list of all the distances found within branch
                nodes from their nearest dead end.
                The third list is a list of all maximum distances of paths that
                branch off the current solution path.
        """
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
                node._distance = _INFINITY
        if tiles_counts[0b0001]+tiles_counts[0b0010]+tiles_counts[0b0100]+tiles_counts[0b1000] == 0:
            raise ValueError("maze has no dead ends, aborting analysis")
        offshoots_maxlengths = []
        for node in self._solution_nodes:
            for offshoot in self.connected_to(node):
                if offshoot not in self._solution_nodes:
                    lengths = []
                    length_adder = lambda n: lengths.append(n.distance) if is_dead_end(n) else None
                    self._breadth_first_search(offshoot, scanr=length_adder)
                    maxlength = max(lengths, default=0)
                    offshoots_maxlengths.append(maxlength)
        return (tiles_counts, branch_distances, offshoots_maxlengths)

    def generate_raster(self, wall_air_ratio=(1,1), decolumnated=False, show_solution=False, show_distances=False, show_algorithms=False):
        """Generate a rasterized representation of the maze for print usage etc.

        The wall-air ratio multiplies the walls/air thicknesses respectively,
        therefore (2,2) will yield a 4-times bigger image than (1,1).

        When four nodes form a square, unwanted 'columns' in such cycles are
        prevented by setting `decolumnated` to True.

        Depending on which (mutually exclusive) `show_X` option is activated,
        the raster will contain the following values:
        (none)          : wall =  1  air = 0
        show_solution   : wall = -1  air = 0        marker = [1,2..]
        show_distances  : wall = -1  air = [0,1..]  unreachable = -2
        show_algorithms : wall = -1  air = [0,1..]

        Args:
            wall_air_ratio (tuple(int,int)): Thickness of wall and air parts.
            decolumnated (bool): Whether free-standing 'column' pieces should
                be removed in free 4x4 sections of the maze (default is False).
            show_solution (bool): Whether to include solution path in raster.
            show_distances (bool): Whether to include distances in raster.
            show_algorithms (bool): Whether to include algorithm IDs in raster.

        Returns:
            list(list(bool)): 2D raster 'image' of the maze.
        """
        (wallM, airM) = wall_air_ratio
        if not decolumnated:
            column = lambda node, dirc, wall, air: wall
        else:
            column = (lambda node, dirc, wall, air:
                wall if dirc!=3
                or node.has_wall(RIGHT) or node.has_wall(DOWN)
                or x==self.width-1 or y==self.height-1
                or (xp:=1+node.coordinates[0])and()or(yp:=1+node.coordinates[1])and()
                or self.node_at(xp,yp).has_wall(UP) or self.node_at(xp,yp).has_wall(LEFT)
                else air
            )
        # `pxl` takes three values:
        # - `node`: current node we're situated at, None if drawing wall
        # - `dirc`: direction which we're painting away from, None if centered on node
        # - `nbr` : neighboring node into direction, for certain checks, None if fringe
        if show_solution:
            if self._solution_nodes is None:
                raise RuntimeError("cannot show solution path before computing it")
            is_sol = lambda n: n in self._solution_nodes
            pxl = (lambda node, dirc, nbr:
                column(nbr,dirc,(-1),0) if node is None # wall
                else (node.distance+1 if is_sol(node) else 0) if dirc is None # center air
                else (-1) if node.has_wall(dirc) # directional wall
                else (node.distance+1 if is_sol(node) else 0) if nbr is not None and is_sol(nbr) # directional colored air
                else 0 # directional air
            )
        elif show_distances:
            dist_col = lambda node: node.distance if node.distance!=_INFINITY else -2 # None check only because py not lazily evaluated <curse words here>
            pxl = (lambda node, dirc, nbr:
                column(nbr,dirc,(-1),dist_col(nbr) if nbr is not None else (-1)) if node is None # wall
                else dist_col(node) if dirc is None # center air
                else (-1) if node.has_wall(dirc) # directional wall
                else dist_col(node) # directional colored air
            )
        elif show_algorithms:
            pxl = (lambda node, dirc, nbr:
                column(nbr,dirc,(-1),nbr._alg_id if nbr is not None else 0) if node is None # wall
                else node._alg_id if dirc is None # center air
                else (-1) if node.has_wall(dirc) # directional wall
                else node._alg_id if nbr is not None and node._alg_id==nbr._alg_id # directional colored air
                else 0 # directional air
            )
        else:
            pxl = (lambda node, dirc, nbr:
                column(nbr,dirc,( 1),0) if node is None # wall
                else 0 if dirc is None # center air
                else ( 1) if node.has_wall(dirc) # directional wall
                else 0 # directional colored air
            )
        rows = self._grid
        raster = []
        # Top-left corner
        row1 = [pxl(None, 0, None)] * wallM
        # Top wall
        for x,node in enumerate(rows[0]):
            row1 += [pxl(node, UP, None)] * airM
            row1 += [pxl(None, 1, None)] * wallM
        raster += [row1] * wallM
        # Middle and bottom rows of string
        for y,row in enumerate(rows):
            # Left wall
            row1 = [pxl(row[0], LEFT, None)] * wallM
            row2 = [pxl(None, 2, None)] * wallM
            # Middle and bottom walls (2 blocks/node)
            for x,node in enumerate(row):
                row1 += [pxl(node, None, None)] * airM
                row1 += [pxl(node, RIGHT, None if x==self.width-1 else self.node_at(x+1,y))] * wallM
                row2 += [pxl(node, DOWN, None if y==self.height-1 else self.node_at(x,y+1))] * airM
                row2 += [pxl(None, 3, node)] * wallM
            raster += [row1] * airM
            raster += [row2] * wallM
        return raster

    @staticmethod
    def _raster_to_image(raster, value_to_color):
        """Convert a raster into a PIL Image object using a conversion function.

        Args:
            raster (list(list(int))): 2D 'map'.
            value_to_color (callable(int) -> tuple(int,int,int)): a function to
                convert raster values to RGB integer tuples.

        Returns:
            PIL.Image: Image object.
        """
        image = Image.new('RGB', (len(raster[0]),len(raster)))
        image.putdata([value_to_color(value) for row in raster for value in row])
        return image

    def generate_image(self, wall_air_colors=(ct.BLACK,ct.WHITE), raster=None):
        """Generate an Image object showing the maze.

        Args:
            wall_air_colors (tuple(tuple(int,int,int),tuple(int,int,int))):
                RGB integer color tuples for the wall- and air pixel colors,
                respectivel (default is (ct.BLACK,ct.WHITE)).
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster()).

        Returns:
            PIL.Image: Image object with additional `filename` attribute.
        """
        if raster is None:
            raster = self.generate_raster()
        # color conversion
        (wall_color, air_color) = wall_air_colors
        value_to_color = lambda value: wall_color if value else air_color
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_{self._stamp()}.png"
        return image

    def generate_solutionimage(self, wall_air_marker_colors=None, raster=None):
        """Generate an Image object showing the maze and its solution.

        Args:
            wall_air_marker_colors (
                tuple(tuple(int,int,int),tuple(int,int,int)),tuple(int,int,int)
                ): RGB integer color tuples for the wall-, air- and solution-
                marked pixel colors (default is (ct.BLACK,ct.WHITE) and a
                cycling (OKLCH) rainbow for the solution path).
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster(show_solution=True)).

        Returns:
            PIL.Image: Image object with additional `filename` attribute.
        """
        if raster is None:
            if self._solution_nodes is None:
                self.compute_solution()
            raster = self.generate_raster(show_solution=True)
        # color conversion
        if wall_air_marker_colors is None:
            peak = self.exit.distance or 1
            wall_color = ct.BLACK
            air_color = ct.WHITE
            rainbow = ct.rainbow_palette(32, ct.VIOLET, keepend=True)
            marker_color = lambda value: ct.interpolate(rainbow, (value-1)/peak)
            #marker_color = lambda value: ct.rainbow(-value/peak, ct.VIOLET, ct.OKLCH)
            #marker_color = lambda value: ct.change_space((360*value/peak, 1, 1),ct.HSV,ct.RGB)
            #marker_color = ct.BLUE
        else:
            wall_color = wall_air_marker_colors[0]
            air_color = wall_air_marker_colors[1]
            marker_color = lambda value: wall_air_marker_colors[2]
        value_to_color = lambda value: wall_color if value==(-1) else air_color if value==0 else marker_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_solution_{self._stamp()}.png"
        return image

    def generate_colorimage(self, gradient_colors=None, raster=None):
        """Generate an Image object showing the maze and its node distances.

        Args:
            gradient_colors (list(tuple(int,int,int))): RGB integer color tuple
                list for the node distance gradient pixel colors
                (default is ct.COLORMAPS['viridis']).
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster(show_distances=True)).

        Returns:
            PIL.Image: Image object with additional `filename` attribute.
        """
        if raster is None:
            raster = self.generate_raster(show_distances=True)
        # color conversion
        wall_color = ct.BLACK
        unreachable_color = ct.DARK_GRAY
        if gradient_colors is None:
            gradient_colors = ct.COLORMAPS['viridis'][::-1]
        air_color = lambda value: ct.interpolate(gradient_colors, param=value/peak)
        peak = max(val for row in raster for val in row) or 1
        value_to_color = lambda value: wall_color if value==(-1) else unreachable_color if value==(-2) else air_color(value)
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_colormap_{self._stamp()}.png"
        return image

    def generate_algorithmimage(self, raster=None):
        """Generate Image object showing the maze and its algorithms colored in.

        Args:
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster(show_algorithms=True)).

        Returns:
            PIL.Image: Image object with additional `filename` attribute.
        """
        if raster is None:
            raster = self.generate_raster(show_algorithms=True)
        coloring = [
            ct.WHITE,
            ct.GRAY,
            ct.MOSS,
            ct.BLUE,
            ct.CRIMSON,
            ct.GOLDENROD,
            ct.mix(ct.VIOLET,ct.PURPLE),
            ct.LIGHT_GRAY,
            ct.BLACK, # Wall
        ]
        value_to_color = lambda value: coloring[value]
        # Convert to image
        image = Maze._raster_to_image(raster, value_to_color)
        image.filename = f"{self.name()}_algorithms_{self._stamp()}.png"
        return image

    @staticmethod
    def generate_animation(width, height, maze_runner, image_generator=None, frame_only=1, alert_progress_steps=0):
        """Generate a list of Image objects showing an animation of a maze.

        The animation shows an algorithm working a blank maze.
        The algorithm and the way images are generated can be customized.
        The rate at which frames are recorded can be customized.

        Args:
            width, height (int): Integer dimensions of new maze.
            maze_runner (callable(Maze, callable(Maze))): An algorithm that
                takes as input the maze to carve, as well as a record_frame
                function to periodically call after changes have been made.
            image_generator (callable(Maze) -> PIL.Image): A function producing
                the frames for the animation (default is
                    lambda maze:
                        maze.compute_distances() and()or
                        maze.generate_colorimage(
                            raster=maze.generate_raster(
                                show_distances=True,
                                wall_air_ratio=(1,3)
                            )
                        )
                )
            frame_only (int): Determines to takes a screenshot every n-th frame.
                (default is 1 (every frame)).
            alert_progress_steps (int): TODO (vaguely: give feedback after
                n-th part of the process).

        Returns:
            (list(PIL.Image),Maze): Animation and end result maze.
                The first Image object has an additional `filename` attribute.
        """
        if image_generator is None:
            #image_generator = lambda maze:maze.compute_distances() and()or maze.generate_colorimage(raster=maze.generate_raster(show_distances=True,wall_air_ratio=(1,3)))
            image_generator = (lambda maze:
                maze.generate_image(
                    raster=maze.generate_raster(wall_air_ratio=(1,3))
                )
            )
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
        frames[0].filename = f"{maze.name()}_anim_{maze._stamp()}.gif"
        return (frames, maze)

    @staticmethod
    def _raster_to_string(raster, value_to_chars):
        """Convert a raster into a string using a conversion function.

        Args:
            raster (list(list(int))): 2D 'map'.
            value_to_chars (callable(int) -> str): a function to
                convert raster values to text characters.

        Returns:
            str: Maze text art.
        """
        string = '\n'.join(
            ''.join(
                value_to_chars(value) for value in row
            ) for row in raster
        )
        return string

    def str_block(self, raster=None, slim=False, show_solution=False):
        """Produce a (Unicode) block string presentation of the maze.

        Args:
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster()).
            slim (bool): Whether to make string half as wide (default is False).
            show_solution (bool): Whether to include solution path in string
                (default is False).

        Returns:
            str: Presentation of the maze.
        """
        if raster is None:
            raster = self.generate_raster(show_solution=show_solution)
        if show_solution:
            value_to_chars = lambda value: (2-slim)*('█' if value==-1 else ':' if value else ' ')
        else:
            value_to_chars = lambda value: (2-slim)*('█' if value else ' ')
        string = Maze._raster_to_string(raster, value_to_chars)
        return string

    def str_block_half(self, raster=None):
        """Produce a (Unicode) half-block string presentation of the maze.

        Args:
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster()).

        Returns:
            str: Presentation of the maze.
        """
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
        """Produce a (Unicode) quarter-block string presentation of the maze.

        Args:
            raster (list(list(bool))): Custom raster map to be rendered
                (default is self.generate_raster()).

        Returns:
            str: Presentation of the maze.
        """
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
        """Produce a (Unicode) pipe-like string presentation of the maze."""
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
        """Produce a (Unicode) frame-like string presentation of the maze.

        Args:
            slim (bool): Whether to make string half as wide (default is False).

        Returns:
            str: Presentation of the maze.
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
        """Produce an ASCII frame-like string presentation of the maze.

        Args:
            air_ratio (int): Multiplier of how much wider corridors should be
                (default is 1)
            show_solution (bool): Whether to include solution path in string.
                (default is False).

        Returns:
            str: Presentation of the maze.
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
                row1 += [f' {"o" if show_solution and node in self._solution_nodes else " "} '] * air_ratio
                row1 += ['|' if node.has_wall(RIGHT) else ' ']
                row2 += ['---' if node.has_wall(DOWN) else '   '] * air_ratio
                row2 += ['+']
            linestr += [row1] * air_ratio
            linestr += [row2]
        return '\n'.join(''.join(line) for line in linestr)

    def str_frame_ascii_small(self, show_solution=False, decolumnated=False):
        """Produce a minimal ASCII frame-like string presentation of the maze.

        Args:
            show_solution (bool): Whether to include solution path in string.
                (default is False).
            decolumnated (bool): Whether free-standing 'column' pieces should
                be removed in free 4x4 sections of the maze (default is False).

        Returns:
            str: Presentation of the maze.
        """
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
            else: return ' ' if decolumnated else '.'
        def cornersegment_top(x):
            if wall(x,0,RIGHT) and not (wall(x,0,UP) and x<self.width-1 and wall(x+1,0,UP)): return ','
            elif wall(x,0,UP) or (x<self.width-1 and wall(x+1,0,UP)): return '_'
            else: return ' ' if decolumnated else '.'
        def cornersegment_left(y):
            if wall(0,y,LEFT): return '|'
            elif y!=self.height-1 and wall(0,y+1,LEFT): return ','
            elif wall(0,y,DOWN): return '_'
            else: return ' ' if decolumnated else '.'
        def cornersegment(x, y):
            if wall(x,y,RIGHT): return '|'
            elif y<self.height-1 and wall(x,y+1,RIGHT) and not (wall(x,y,DOWN) and x<self.width-1 and wall(x+1,y,DOWN)): return ','
            elif wall(x,y,DOWN) or (x<self.width-1 and wall(x+1,y,DOWN)): return '_'
            else: return ' ' if decolumnated else '.'
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

    @staticmethod
    def _algorithm_name_to_id(string):
        """Canonically mapping str to int using ALGORITHMS (OrderedDict)."""
        return list(ALGORITHMS.keys()).index(string)

    @maze_algorithm
    def clear(self, record_frame=None, area=None):
        """Routine that clears a maze of its edges.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
        """
        if area is None:
            area = (0,0,self.width-1,self.height-1)
        if record_frame is None:
            record_frame = lambda maze:None
        alg_id = Maze._algorithm_name_to_id('clear')
        record_frame(self)
        for (node0,node1) in self.edges(area):
            self.connect(node0,node1)
            record_frame(self)
        self._solution_nodes = None

    @maze_algorithm
    def random_edges(self, record_frame=None, area=None, edge_probability=0.5):
        """Routine that uniformly randomly assigns edges between nodes in grid.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            edge_probability (float): Probability 0<=p<=1 with which to roll.
        """
        alg_id = Maze._algorithm_name_to_id('random_edges')
        if record_frame is None:
            record_frame = lambda maze:None
        record_frame(self)
        for (node0,node1) in self.edges(area):
            node0._alg_id = node1._alg_id = alg_id
            if random.random() < edge_probability:
                self.connect(node0,node1)
                record_frame(self)
        return

    @maze_algorithm
    def growing_tree(self, record_frame=None, area=None, start_coord=None, name_and_index_choice=None, fast_pop=False):
        """Growing Tree algorithm to carve a maze.

        The algorithm works by having an active set of nodes at a time, and
        randomly choosing one from which to choose and add an unvisited
        neighbor node to the active set. If an active node has no neighbors,
        remove it.
        New nodes are appended at the back of the list, yet the next node to
        draw can be arbitrary, which allows for some flexibility:
        - Draw back node [stack-like / latest neighbor]:
            'Backtracker' algorithm, DFS-like.
        - Draw random node [random active node]:
            '(Simplified) Prim' algorithm.
        - Draw front node [queue-like / oldest neighbor]:
            Uninteresting, leads to straight corridors all the way, BFS-like.
        - Mixed behaviours:
            [Undeterminted, subject to experimenting.]

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            start_coord (int,int): Coordinates 0<=x<width && 0<=y<height from
                which to start the alg. (default is uniformly random choice).
            name_and_index_choice (str, callable(int) -> int): Algorithm name
                and choice function to draw next index between 0 and
                the given (max_index).
                Note that the algorithm will be added to ALGORITHMS if it has
                a unique name
                (default is
                    'growing_tree', lambda max_index:
                        -1 if random.random()<0.95
                        else random.randint(0,max_index)
                ).
            fast_pop (bool): Activate small optimization, each switching chosen
                element with last element in active set (list) when removing it
                (default is False).
        """
        if area is None:
            area = (0,0,self.width-1,self.height-1)
        (x0,y0,x1,y1) = area
        if record_frame is None:
            record_frame = lambda maze:None
        if start_coord is None:
            start_coord = (random.randint(x0,x1),random.randint(y0,y1))
        if name_and_index_choice is None:
            name = 'growing_tree'
            index_choice = lambda max_index: -1 if random.random()<0.70 else random.randint(0,max_index)
        else:
            (name,index_choice) = name_and_index_choice
            if name not in ALGORITHMS:
                ALGORITHMS[name] = (lambda maze, area, record_frame:
                    Maze.growing_tree(
                        maze,
                        record_frame=record_frame,
                        area=area,
                        name_and_index_choice=name_and_index_choice,
                    )
                )
        alg_id = Maze._algorithm_name_to_id(name)
        start = self.node_at(*start_coord)
        start.flag = True
        start._alg_id = alg_id
        active_set = [start]
        record_frame(self)
        while active_set:
            idx = index_choice(len(active_set)-1)
            node = active_set[idx]
            if (neighbors:=[nbr for nbr in self.adjacent_to(node, area) if not nbr.flag]):
                neighbor = random.choice(neighbors)
                self.connect(node, neighbor)
                neighbor.flag = True
                neighbor._alg_id = alg_id
                active_set.append(neighbor)
                record_frame(self)
            else:
                if fast_pop:
                    if len(active_set) > 1 and idx != -1:
                        (
                            active_set[idx], active_set[-1]
                        ) = (
                            active_set[-1],  active_set[idx]
                        )
                    active_set.pop()
                else:
                    active_set.pop(idx)
        return

    @maze_algorithm
    def backtracker(self, record_frame=None, area=None, start_coord=None):
        """Depth-First-Search like 'backtracker' algorithm to produce rndm maze.

        See `growing_tree` algorithm.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            start_coord (int,int): Coordinates 0<=x<width && 0<=y<height from
                which to start the alg. (default is uniformly random choice).
        """
        self.growing_tree(
            record_frame=record_frame,
            area=area,
            start_coord=start_coord,
            name_and_index_choice=(
                'backtracker',
                (lambda max_index: -1),
            ),
        )
        return

    @maze_algorithm
    def prim(self, record_frame=None, area=None, start_coord=None):
        """'Simplified Prim' algorithm to produce random maze.

        See `growing_tree` algorithm.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            start_coord (int,int): Coordinates 0<=x<width && 0<=y<height from
                which to start the alg. (default is uniformly random choice).
            start_coord (int,int): Coordinates 0<=x<width && 0<=y<height from
                which to start the alg. (default is uniformly random choice).
        """
        self.growing_tree(
            record_frame=record_frame,
            area=area,
            start_coord=start_coord,
            name_and_index_choice=(
                'prim',
                (lambda max_index: random.randint(0,max_index)),
            ),
        )
        return

    @maze_algorithm
    def kruskal(self, record_frame=None, area=None):
        """Randomized Kruskal's algorithm to produce random maze.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
        """
        alg_id = Maze._algorithm_name_to_id('kruskal')
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
            node0._alg_id = node1._alg_id = alg_id
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

    @maze_algorithm
    def wilson(self, record_frame=None, area=None, start_coord=None):
        """Wilson's uniform random spanning tree algorithm to make a rndm maze.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            start_coord (int,int): Coordinates 0<=x<width && 0<=y<height from
                which to start the alg. (default is uniformly random choice).
        """
        alg_id = Maze._algorithm_name_to_id('wilson')
        if area is None:
            area = (0,0,self.width-1,self.height-1)
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
            node._alg_id = alg_id
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

    @maze_algorithm
    def division(self, record_frame=None, area=None, slice_direction_choice=None, pivot_choice=None, roomlength=0, nest_algorithms=[]):
        """Divide-and-conquer approach to making a random maze.

        Customizable through choice of direction and position of area cut.
        Additionally supports leaving open rooms, or nesting algorithms therein.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            slice_direction_choice (callable(int,int,bool) -> bool): Function to
                determine whether to slice *horizontally* next, based on area
                width&height and whether previous cut was horizontal
                (default is
                    lambda w,h, prev:
                        h > w if h != w else random.getrandbits(1)
                ).
            pivot_choice (callable(int,int) -> int): Function to determine where
                to make the cut within the interval [l, r]
                (default is
                    lambda l,r:
                        min(max(l,int(random.gauss((l+r)/2,(l+r)/2**7))),r)
                ).
            roomlength (int): Maximum sidel ength of rooms to randomly leave
                open/fill recursively (default is 0).
            nest_algorithms (
                list(callable(Maze, tuple(int,int,int,int), callable(Maze)))
                ): List of recursively callable maze algorithms.
                To qualify, an algorithm must accept a maze to modify,
                an area to selectively carve and a record_frame for snapshots.
        """
        alg_id = Maze._algorithm_name_to_id('division')
        if area is None:
            area = (0,0,self.width-1,self.height-1)
        if record_frame is None:
            record_frame = lambda maze:None
        if pivot_choice is None:
            #pivot_choice = lambda l,r: (l+r)//2
            pivot_choice = lambda l,r: min(max(l,int(random.gauss((l+r)/2,(l+r)/2**7))),r)
            #pivot_choice = lambda l,r: random.triangular(l,r)
            #pivot_choice = lambda l,r: random.randint(l,r)
        if slice_direction_choice is None:
            slice_direction_choice = lambda w,h, prev: h > w if h != w else random.getrandbits(1)
            #slice_direction_choice = lambda w,h, prev: prev ^ (random.random() < 1.9)
            #slice_direction_choice = lambda w,h, prev: random.getrandbits(1)
        def divide(area, prev_dir):
            (x0,y0,x1,y1) = area
            ewidth, eheight = (x1-x0)+1, (y1-y0)+1
            room1 = ewidth <= 1 or eheight <= 1
            event_room = (
                roomlength > 0
                and ewidth <= roomlength and eheight <= roomlength
                and random.random() < 1/(ewidth*eheight)**.5
            )
            if room1 or (event_room and not nest_algorithms):
                for x in range(x0,x1+1):
                    for y in range(y0,y1+1):
                        self.node_at(x,y)._alg_id = alg_id
                        if x < x1:
                            self.node_at(x+1,y)._alg_id = alg_id
                            self.connect((x,y),(x+1,y))
                        if y < y1:
                            self.node_at(x,y+1)._alg_id = alg_id
                            self.connect((x,y),(x,y+1))
                        record_frame(self)
                return
            elif event_room:
                random.choice(nest_algorithms)(self, record_frame, area)
                return
            cut_horizontally = slice_direction_choice(ewidth, eheight, prev_dir)
            if cut_horizontally:
                yP = pivot_choice(y0,y1-1)
                x = random.randint(x0,x1)
                if not nest_algorithms:
                    self.node_at(x,yP)._alg_id = alg_id
                    self.node_at(x,yP+1)._alg_id = alg_id
                self.connect((x,yP),(x,yP+1))
                record_frame(self)
                divide((x0,y0,x1,yP), True)
                divide((x0,yP+1,x1,y1), True)
            else:
                xP = pivot_choice(x0,x1-1)
                y = random.randint(y0,y1)
                if not nest_algorithms:
                    self.node_at(xP,y)._alg_id = alg_id
                    self.node_at(xP+1,y)._alg_id = alg_id
                self.connect((xP,y),(xP+1,y))
                record_frame(self)
                divide((x0,y0,xP,y1), False)
                divide((xP+1,y0,x1,y1), False)
        hello_reader = self.width < self.height
        divide(area, hello_reader)
        return

    @maze_algorithm
    def xdivision(self, record_frame=None, area=None, roomlength=0):
        """Div&Cqr to make a random maze with other recursive algorithm calls.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
        """
        self.division(
            record_frame=record_frame,
            area=area,
            roomlength=float('inf'),
            nest_algorithms=[
                alg for name,alg in ALGORITHMS.items() if name not in {
                    'random_edges', 'xdivision'
                }
            ],
        )
        return

    def make_unicursal(self, record_frame=None, area=None, probability=1):
        """Convert maze into a unicursal maze.

        A unicursal maze has no dead ends (and only cycles), the conversion
        is done by finding all dead ends and randomly connecting them again.

        Args:
            record_frame (callable(Maze)): Function to take snapshot of maze
                periodically (default is lambda _: None).
            area (tuple(int,int,int,int)): Coordinates of upper left (x0,y0,..),
                and bottom right (..,x1,y1) corners between which to execute
                (default is (0,0, self.width-1,self.height-1)).
            probability (float): Probability 0<=p<=1 to connect a dead end with
                a random neighbor (default is 1).
        """
        if area is None:
            area = (0,0,self.width-1,self.height-1)
        if record_frame is None:
            record_frame = lambda maze:None
        for node in self.nodes(area):
            if random.random() < probability:
                while sum(1 for _ in self.connected_to(node)) <= 1:
                    neighbor = random.choice(
                        list(self.connected_to(node,invert=True)))
                    self.connect(node,neighbor)
                    record_frame(self)
        return

# END   CLASSES


# BEGIN FUNCTIONS
# No functions
# END   FUNCTIONS


# BEGIN MAIN
# No main
# END   MAIN
