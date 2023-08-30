# BEGIN OUTLINE
"""
A small benchmark script that tests and times some methods from `state.py`.

Note to self: do `python3 -m scalene small_benchmark.py`
"""
# END   OUTLINE


# BEGIN IMPORTS

import random
import colortools as ct
from os         import makedirs
from benchtools import timed, timed_titled
from mazing     import Maze, ALGORITHMS

# END   IMPORTS


# BEGIN CONSTANTS

# Functions to be run in main
FUNCTIONS_TO_RUN = []
# Directory to store benchmark files in
OUTPUT_DIRECTORY = 'output_benchmark'

# END   CONSTANTS


# BEGIN DECORATORS

def run(f):
    global FUNCTIONS_TO_RUN
    FUNCTIONS_TO_RUN.append(f)
    return f

# END   DECORATORS


# BEGIN CLASSES
# No classes
# END   CLASSES


# BEGIN FUNCTIONS

# Useful helpers

@timed
def clear_file(filename):
    path = f"{OUTPUT_DIRECTORY}/{filename}"
    with open(path,'w') as file:
        file.write('')
    return

@timed
def append_text(filename, string):
    path = f"{OUTPUT_DIRECTORY}/{filename}"
    with open(path,'a') as file:
        file.write(string)
    return

@timed
def save_image(image):
    path = f"{OUTPUT_DIRECTORY}/{image.filename}"
    image.save(path)
    return

@timed
def grid(n):
    return Maze(2**n, 2**n)

# Actual functions to be benchmarked start here

#@run
def test_sizes():
    for n in range(32):
        maze = grid(n)
    return

#@run
def test_builders():
    for builder in ALGORITHMS.values():
        maze = grid(8)
        timed(builder)(maze)
    return

#@run
def test_tree_pop():
    N = 10
    maze = grid(N)
    timed(maze.growing_tree)(
        name_and_index_choice=(
            "random tree",
            (lambda mxi:random.randint(0,mxi)),
        )
    )
    maze = grid(N)
    timed(maze.growing_tree)(
        name_index_choice=(
            "random tree fast",
            (lambda mxi:random.randint(0,mxi)),
        ),
        fast_pop=True,
    )
    return

#@run
def test_tree_probabilites():
    filename = 'growing tree test probabilities.txt'
    clear_file(filename)
    N = 9
    for i in range(100):
        if i < 90 and i % 5 != 0:
            continue
        maze = grid(N)
        timed_with_name(f"growing tree {i}/100", maze.growing_tree)(
            name__and_index_choice=(
                f"tree_{i/100:.02f}",
                (lambda mxi:
                     -1 if random.random() < i/100 else random.randint(0,mxi)
                ),
            ),
        )
        timed(maze.compute_longest_path)()
        stats = timed(maze.generate_stats)()
        string = f"""growing tree {i}/100
  Avg branch dist  {sum(stats[1])/len(stats[1]):.02f}
  Len longest path     {len(maze.solution)}
  Num sol offshoot {len(stats[2])}
  Avg sol offshoot {sum(stats[3])/len(stats[3]):.02f}
  Var sol offshoot {(sum(x**2 for x in stats[3])/len(stats[3]) - (sum(stats[3])/len(stats[3]))**2)**.5:.02f}
"""
        append_text(filename, string)
    return

#@run
def test_kanagawa2():
    m = 1
    while True:
        maze = timed_titled(f"Maze {m}", Maze)(1920,1080)
        timed(maze.backtracker)()
        timed(maze.compute_distances)()
        image = timed(maze.generate_colorimage)(
            gradient_colors=ct.COLORMAPS['kanagawa'][::-1],
            raster=timed(maze.generate_raster)(
                show_distances=True,
                wall_air_ratio=(0,1)
            )
        )
        timed(image.save)(f"{OUTPUT_DIRECTORY}/{image.filename}")
        timed(maze.compute_longest_path)()
        timed(maze.compute_distances)()
        image = timed(maze.generate_colorimage)(
            gradient_colors=ct.COLORMAPS['kanagawa'][::-1],
            raster=timed(maze.generate_raster)(
                show_distances=True,
                wall_air_ratio=(0,1)
            )
        )
        timed(image.save)(f"{OUTPUT_DIRECTORY}/{image.filename}")
        #with open(f"{OUTPUT_DIRECTORY}/{image.filename[:-4]}.dat",'w') as file:
            #file.write(timed(repr)(maze))
        m += 1
    return

#@run
def test_big_images():
    maze = grid(10)
    timed(maze.backtracker)()
    image = timed(maze.generate_algorithmimage)()
    timed(maze.compute_solution)()
    image = timed(maze.generate_solutionimage)()
    timed(maze.compute_distances)()
    image = timed(maze.generate_colorimage)()
    timed(maze.compute_branchdistances)()
    image = timed(maze.generate_colorimage)()
    timed(save_image)(image)
    return

@run
def test_wandering_light():
    MAKE_LOOPED = True
    maze = Maze(64,64)
    timed(maze.kruskal)()
    timed(maze.compute_solution)()
    path = sorted(maze.solution, key=lambda n: n.distance)
    if MAKE_LOOPED:
        path = path + path[::-1]
    palette = ct.COLORMAPS['helix2'][::-1]
    frames = []
    frame_only = 4
    for i,node in enumerate(path):
        if i % frame_only == 0:
            maze.set_entrance(*node.coordinates)
            maze.compute_distances()
            node._distance = max(n.distance for n in maze.nodes())
            image = maze.generate_colorimage(
                gradient_colors=palette,
                raster=maze.generate_raster(
                    wall_air_ratio=(1,2),
                    show_distances=True,
                ),
            )
            frames.append(image)
    frames[0].filename = f"{maze.name()}_l-anim_{maze._stamp()}.gif"
    timed_titled(f"saving {frames[0].filename}", frames[0].save)(
        f"{OUTPUT_DIRECTORY}/{frames[0].filename}",
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=30,
        loop=0,
    )
    return

# END   FUNCTIONS


# BEGIN MAIN

def main():
    # Run all FUNCTIONS_TO_RUN
    makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    for f in FUNCTIONS_TO_RUN:
        print(f"BEGIN {f.__name__.upper()}")
        timed(f)()
        print(f"END   {f.__name__.upper()}")
    print("finished")
    return

if __name__=="__main__": main()

# END   MAIN

    # {{{ BEGIN END }}} ALERT ATTENTION DANGER HACK SECURITY BUG FIXME DEPRECATED TASK TODO TBD WARNING CAUTION NOLINT ### NOTE NOTICE TEST TESTING
