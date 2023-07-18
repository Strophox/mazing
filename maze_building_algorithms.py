# OUTLINE BEGIN
"""
This script contains functions to build and modify mazes.
"""
# OUTLINE END


# IMPORTS BEGIN

from maze import *
import random

# IMPORTS END


# CONSTANTS BEGIN
# No constants
# CONSTANTS END


# CLASSES BEGIN
# No classes
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

def recursive_backtrack(maze):
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

# FUNCTIONS END


# MAIN BEGIN
# No main
# MAIN END
