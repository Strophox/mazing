# OUTLINE BEGIN
"""
A small benchmark script that tests and times some methods from `maze.py`.

Note to self: do `python3 -m scalene small_benchmark.py`
"""
# OUTLINE END


# IMPORTS BEGIN

from maze import Maze
import time

# IMPORTS END


# CONSTANTS BEGIN

__ = lambda n: (2**n, 2**n)

SEQ_00 = [
      (r"BEGIN", lambda maze: maze

    ),("test unit", lambda maze:
        print("hello, world")

    ),(r"END", lambda maze: maze)
]

SEQ_01 = [
      (r"BEGIN", lambda maze: maze

    ),("maze  0", lambda maze:
        Maze(*__(0))
    ),("maze  1", lambda maze:
        Maze(*__(1))
    ),("maze  2", lambda maze:
        Maze(*__(2))
    ),("maze  3", lambda maze:
        Maze(*__(3))
    ),("maze  4", lambda maze:
        Maze(*__(4))
    ),("maze  5", lambda maze:
        Maze(*__(5))
    ),("maze  6", lambda maze:
        Maze(*__(6))
    ),("maze  7", lambda maze:
        Maze(*__(7))
    ),("maze  8", lambda maze:
        Maze(*__(8))
    ),("maze  9", lambda maze:
        Maze(*__(9))
    ),("maze 10", lambda maze:
        Maze(*__(10))
    ),("maze 11", lambda maze:
        Maze(*__(11))
    ),("maze 12", lambda maze:
        Maze(*__(12))
    ),("maze 13", lambda maze:
        Maze(*__(13))
    ),("maze 14", lambda maze:
        Maze(*__(14))
    ),("maze 15", lambda maze:
        Maze(*__(15))
    ),("maze 16", lambda maze:
        Maze(*__(16))

    ),(r"END", lambda maze: maze)
]

SEQ_02 = [
    (N := 10) and()or
      (r"BEGIN", lambda maze: maze

    ),("random_edges", lambda maze:
        Maze.random_edges(*__(N))
    ),("growing_tree", lambda maze:
        Maze.growing_tree(*__(N))
    ),("backtracker", lambda maze:
        Maze.backtracker(*__(N))
    ),("prim", lambda maze:
        Maze.prim(*__(N))
    ),("kruskal", lambda maze:
        Maze.kruskal(*__(N))
    ),("wilson", lambda maze:
        Maze.wilson(*__(N))
    ),("division", lambda maze:
        Maze.division(*__(N))

    ),(r"END", lambda maze: maze)
]

SEQ_03 = [
      (r"BEGIN", lambda maze: maze

    ),("division", lambda maze:
        Maze.division(*__(9))
    ),("growing_tree (fast_pop)", lambda maze:
        Maze.growing_tree(*__(9),fast_pop=True)
    ),("wilson", lambda maze:
        Maze.wilson(*__(7))
    ),("SAVE image", lambda maze:
        maze.generate_image().save(f"{maze.generate_name()}.png") and()or maze # <- cursed sequential expression composition
    ),("make_unicursal", lambda maze:
        maze.make_unicursal() and()or maze
    ),("SAVE image", lambda maze:
        maze.generate_image().save(f"{maze.generate_name()}.png") and()or maze

    ),(r"END", lambda maze: maze)
]

SEQ_04 = [
      (r"BEGIN", lambda maze: maze

    ),("backtracker", lambda maze:
        Maze.backtracker(*__(10))
    ),("breadth_first_search", lambda maze:
        maze.breadth_first_search() and()or maze
    ),("generate_solutionimage", lambda maze:
        maze.generate_solutionimage() and()or maze

    ),(r"END", lambda maze: maze)
]

SEQ_05 = [
      (r"BEGIN", lambda maze: maze

    ),("backtracker", lambda maze:
        Maze.backtracker(64,64)
    ),("breadth_first_search", lambda maze:
        maze.breadth_first_search() and()or maze
    ),("SHOW colorimage", lambda maze:
        maze.generate_colorimage().show() and()or maze

    ),(r"END", lambda maze: maze)
]

SEQ_CHOSEN = SEQ_05

# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def run_benchmark_on(sequence):
    """Runs and benchmarks a sequence of 'actions'.

    Args:
        sequence (list(str, callable(Maze) -> Maze)): A list of 'actions' where an 'action' has a name and does computation on a Maze and returns a Maze
    """
    main_maze = None
    for (title,action) in sequence:
        begin_time = time.perf_counter()
        main_maze  = action(main_maze)
        end_time   = time.perf_counter()
        print(f"['{title}' completed in {end_time-begin_time:.03f}s]")
    return

# FUNCTIONS END


# MAIN BEGIN

def main():
    run_benchmark_on(SEQ_CHOSEN)
    return

if __name__=="__main__": main()

# MAIN END
