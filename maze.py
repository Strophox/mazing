
# OUTLINE BEGIN

# A small script to generate some mazes
"""
Work in Progress:
- Carvers:
  * wilsons,
  * recursive division
- Solvers:
  * A* pathfinder
- ETC Dreams:
  * Maze navigator (w/ curses)
  * Interactive picker: distance by color
  * Doom (curses) █▯▓▯▒▯░
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
        self.name = f"maze_{self.width}x{self.height}_blank"

    def __repr__(self):
        return self.grid.__repr__() # "["+ ','.join("["+ ','.join(str(n._connectivity) for n in row) +"]" for row in self.grid) + "]"

    def __iter__(self):
        return itertools.chain(*self.grid)

    def clear(self):
        for y,row in enumerate(self.grid):
            for x,node in enumerate(row):
                row[x] = Node(x,y)
        self.info = dict()

    def set_name(self, carver_name):
        size = f"{self.width}" if self.width==self.height else f"{self.width}x{self.height}"
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        self.name = f"maze_{carver_name}_{size}_{timestamp}"

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
        if wall is None:
            make_wall = lambda: random.choice(['##','#@','%#'])
        elif callable(wall):
            make_wall = wall
        else:
            make_wall = lambda: wall
        if air is None:
            make_air = lambda: ' '*len(make_wall())
        elif callable(air):
            make_air = air
        else:
            make_air = lambda: air
        # Produce actual string
        string = '\n'.join(''.join(make_wall() if b else make_air() for b in row) for row in bitmap)
        return string

    def str_block(self):
        """Produce full-block (unicode) bitmap art of the maze.
        """
        return self.str_bitmap(wall='█',air=' ')

    def str_halfblock(self):
        """Produce half-block (unicode) bitmap art of the maze.
        """
        tiles = " ▄▀█"
        bmap = self.bitmap()
        if len(bmap)%2!=0:
            bmap.append([False for _ in bmap[0]])
        string = '\n'.join(''.join(tiles[2*hi + 1*lo] for (hi,lo) in zip(bmap[y],bmap[y+1])) for y in range(0,len(bmap),2))
        return string

    def str_quarterblock(self):
        """Produce quarter-block (unicode) bitmap art of the maze.
        """
        #tiles = " ▯▘▯▝▯▀▯▖▯▌▯▞▯▛▯▗▯▚▯▐▯▜▯▄▯▙▯▟▯█"
        tiles = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
        bmap = self.bitmap()
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

    def str_ascii(self):
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

    def str_connections(self):
        """Display the node connections in the maze.
        """
        return '\n'.join(''.join(str(node) for node in row) for row in self.grid)

    def generate_image(self, bitmap=None):
        """Generate an Image of the maze and store it in the instance.
        - bitmap : custom bitmap (2D list)
        """
        if bitmap is None:
            bitmap = self.bitmap()
        width,height = len(bitmap[0]),len(bitmap)
        bit_to_rgb = lambda bit: (0,0,0) if bit else (255,255,255)
        img = tuple(bit_to_rgb(bit) for bit in itertools.chain(*bitmap))
        # Convert to Image
        self.image = Image.new('RGB', (width,height))
        self.image.putdata(img)

    def save_image(self, filename=None):
        """Save the image of the maze to file.
        - filename : str of image filename including extension (-> PIL)
        """
        if filename is None:
            filename = f"{self.name}.png"
        # Generate image if not done yet
        if getattr(self, 'image', None) is None:
            self.generate_image()
        # Save image
        self.image.save(filename)

    def show_image(self):
        """Show an image of the maze.
        """
        if getattr(self, 'image', None) is None:
            self.generate_image()
        self.image.show()

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

def bogus(maze):
    """Carve complete bogus into a maze by essentially randomizing it.
    """
    for node in maze:
        node.toggle_edge(random.randint(0b0000,0b1111))
    maze.set_name("bogus")

def growingtree(maze, start=None, choose_index=None, optimize_pop=False):
    """Carve a maze using the 'growing binary tree' algorithm.
    - start : origin `Node`
    - choose_index : callable that returns a valid index given an indexable `bucket`
    * Note that this carver can be made equivalent to other algorithms by tweaking `choose_index`:
      - always `-1` (newest element) is recursive backtracker / depth first search
      - always `0` (oldest element) is breadth first search
      - always random is randomized prim's algorithm.
    """
    if start is None:
        start = random.choice(list(maze))
    if choose_index is None:
        choose_index = lambda bucket: -1 if random.random()<0.95 else random.randrange(len(bucket))
    start.flag = True
    bucket = [start]
    while bucket:
        n = choose_index(bucket)
        node = bucket[n]
        neighbors = [nb for nb in maze.adjacent_to(node) if not nb.flag]
        if neighbors:
            neighbor = random.choice(neighbors)
            maze.connect(node,neighbor)
            neighbor.flag = True
            bucket.append(neighbor)
        else:
            if optimize_pop:
                if len(bucket) > 1 and n!=-1:
                    bucket[n],bucket[-1] = bucket[-1],bucket[n]
                bucket.pop()
            else:
                bucket.pop(n)
    maze.set_name("growing-tree")

def randomprim(maze):
    """Carve a maze using randomized Prim's algorithm.
    """
    growingtree(maze, choose_index=lambda bucket: random.randrange(len(bucket)))
    maze.set_name("prim")

def backtracker(maze):
    """Carve a maze using simple randomized depth-first-search.
    * More robust than `recursive backtracker` for larger mazes.
    """
    growingtree(maze, choose_index=lambda bucket: -1)
    maze.set_name("backtracker")

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
    maze.set_name("recursive_backtracker")

def randomkruskal(maze):
    """Carve a maze using randomized Kruskal's algorithm.
    """
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
    maze.set_name("kruskal")

def wilson(maze, start=None):
    """Carve a maze using Wilson's random uniform spanning tree algorithm.
    """
    def backtrack_walk(tail_node, origin):
        while tail_node != origin:
            prev_node = next(maze.adjacent_to(tail_node,connected=True))
            maze.connect(tail_node,prev_node) # DANGER actually disconnecting
            tail_node.flag = 0
            tail_node = prev_node
    if start is None:
        start = maze.node_at(maze.width//2,maze.height//2)
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


    maze.set_name("wilson")

# FUNCTIONS END


# MAIN BEGIN

def title_art():
    def from_mask(template):
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
    maze = from_mask(template)
    recursive_backtracker(maze)
    return maze.str_pipes()

def main():
    print(title_art())
    import textwrap # remove source code multiline string indents
    main_menu_text = textwrap.dedent(f"""
        Maze Sandbox
        -- Editing
        | carve  (new maze pattern)
        | resize (maze)
        | load   (maze str repr)
        -- Viewing
        | print  (latest maze, ascii art)
        | show   (latest maze, external png)
        | save   (external png)
        >""")
    printers = {p.__name__:p for p in (
        Maze.str_bitmap,
        Maze.str_block,
        Maze.str_halfblock,
        Maze.str_quarterblock,
        Maze.str_pipes,
        Maze.str_frame,
        Maze.str_ascii,
        Maze.str_connections,
        repr,
    )}
    carvers = {c.__name__:c for c in (
        bogus,
        backtracker,
        growingtree,
        randomprim,
        randomkruskal,
        wilson,
    )}
    N = 16
    maze = Maze(N,N)
    while ui := input(main_menu_text).strip():
        match ui:
            case "carve":
                prompt = f"Choose algorithm:\n| " + ' | '.join(carvers) + "\n>"
                if carver := carvers.get(input(prompt).strip()):
                    maze.clear()
                    start = time.perf_counter()
                    carver(maze)
                    print(f"<carve completed in {time.perf_counter()-start:.03f}s>")
                    print(maze.str_frame() if maze.width*maze.height<10000 else f"<no print (cellcount {maze.width*maze.height})>")
                else:
                    print("<carver not found>")
            case "resize":
                try:
                    prompt = "Dimensions X,Y >"
                    maze = Maze(*tuple(map(int, input(prompt).split(','))))
                except Exception as e:
                    print(f"<something went wrong: {e}>")
            case "load":
                try:
                    prompt = "Maze grid repr >"
                    grid = eval(input())
                    width,height = len(grid[0]),len(grid)
                    maze = Maze(width,height)
                    for x in range(height):
                        for y in range(width):
                            maze.node_at(x,y).set_edges(grid[y][x])
                except Exception as e:
                    print(f"<something went wrong: {e}>")
            case "print":
                for name,printer in printers.items():
                    print(f"{name}:\n{printer(maze)}")
            case "show":
                maze.show_image()
            case "save":
                maze.save_image()
            case "exec":
                try:
                    exec(input(">>> "))
                except Exception as e:
                    print(f"<exception: {e}>")
            case _:
                print("<invalid option>")
    print("goodbye")

def benchmark():
    """Run `python3 -m scalene maze.py`
    """
    def run(n, carver):
        maze = Maze(n,n)
        start = time.perf_counter()
        carver(maze)
        print(f"<run completed in {time.perf_counter() - start}s>")
        maze.save_image()
        print(f"<saved '{maze.name}'>")
    configs = [
        #(2**10, lambda maze:growingtree(maze,optimize_pop=True)),
        (2**9, wilson)
    ]
    for config in configs: run(*config)

if __name__=="__main__":
    #main()
    benchmark()

#[[8,9,13,5,5,5,12,1,5,13,13,5,5,4,9,12],[11,6,2,9,12,1,7,5,5,14,2,9,13,5,6,10],[3,12,9,6,3,5,5,5,12,10,9,6,3,12,9,6],[9,14,3,12,1,13,4,9,6,2,10,1,5,6,10,8],[10,3,5,6,9,7,12,3,5,5,6,8,9,5,6,10],[10,9,5,4,10,8,3,5,12,9,5,6,3,12,9,6],[10,11,5,5,6,3,13,4,10,11,5,5,12,10,3,12],[10,3,12,8,9,13,6,1,6,10,1,12,3,14,9,14],[3,12,10,10,10,3,5,12,1,7,12,3,12,3,6,10],[9,14,11,14,11,5,12,3,5,4,10,9,7,4,9,6],[10,10,2,10,10,1,14,8,8,9,6,10,1,12,10,8],[10,3,12,10,10,8,11,6,10,3,5,7,4,3,6,10],[10,8,11,7,14,10,3,12,11,5,5,13,12,8,9,14],[10,10,10,9,6,10,9,6,10,1,13,6,3,6,2,10],[10,10,10,2,9,6,10,1,7,12,3,5,12,1,13,14],[3,6,3,5,6,1,7,5,5,6,1,5,7,5,6,2]]

# MAIN END
