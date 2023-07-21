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

SEQ_00 = [
      (r"BEGIN", lambda maze: maze

    ),("test unit", lambda maze:
        print("hello, world")

    ),(r"END", lambda maze: maze)
]

SEQ_01 = [
      (r"BEGIN", lambda maze: maze

    ),("maze  0", lambda maze:
        Maze(*_2(0))
    ),("maze  1", lambda maze:
        Maze(*_2(1))
    ),("maze  2", lambda maze:
        Maze(*_2(2))
    ),("maze  3", lambda maze:
        Maze(*_2(3))
    ),("maze  4", lambda maze:
        Maze(*_2(4))
    ),("maze  5", lambda maze:
        Maze(*_2(5))
    ),("maze  6", lambda maze:
        Maze(*_2(6))
    ),("maze  7", lambda maze:
        Maze(*_2(7))
    ),("maze  8", lambda maze:
        Maze(*_2(8))
    ),("maze  9", lambda maze:
        Maze(*_2(9))
    ),("maze 10", lambda maze:
        Maze(*_2(10))
    ),("maze 11", lambda maze:
        Maze(*_2(11))
    ),("maze 12", lambda maze:
        Maze(*_2(12))
    ),("maze 13", lambda maze:
        Maze(*_2(13))
    ),("maze 14", lambda maze:
        Maze(*_2(14))
    ),("maze 15", lambda maze:
        Maze(*_2(15))
    ),("maze 16", lambda maze:
        Maze(*_2(16))

    ),(r"END", lambda maze: maze)
]

SEQ_02 = [
    (N := 10) and()or
      (r"BEGIN", lambda maze: maze

    ),("random_edges", lambda maze:
        Maze.random_edges(*_2(N))
    ),("growing_tree", lambda maze:
        Maze.growing_tree(*_2(N))
    ),("backtracker", lambda maze:
        Maze.backtracker(*_2(N))
    ),("prim", lambda maze:
        Maze.prim(*_2(N))
    ),("kruskal", lambda maze:
        Maze.kruskal(*_2(N))
    ),("wilson", lambda maze:
        Maze.wilson(*_2(N))
    ),("division", lambda maze:
        Maze.division(*_2(N))

    ),(r"END", lambda maze: maze)
]

SEQ_03 = [
      (r"BEGIN", lambda maze: maze

    ),("division", lambda maze:
        Maze.division(*_2(9))
    ),("growing_tree (fast_pop)", lambda maze:
        Maze.growing_tree(*_2(9),fast_pop=True)
    ),("wilson", lambda maze:
        Maze.wilson(*_2(7))
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
        Maze.backtracker(*_2(10))
    ),("breadth_first_search", lambda maze:
        maze.breadth_first_search() and()or maze
    ),("generate_solutionimage", lambda maze:
        maze.generate_solutionimage() and()or maze

    ),(r"END", lambda maze: maze)
]

SEQ_CHOSEN = SEQ_04

# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def _2(n):
    """Produce a pair (2**n,2**n) given some number n."""
    return (2**n,2**n)

def run_and_time(f):
    """Run a function and return its result and execution time as tuple."""
    start_time = time.perf_counter()
    result = f()
    time_taken = time.perf_counter() - start_time
    return (result, time_taken)

def run_benchmark_on(sequence):
    """Runs and benchmarks a sequence of 'actions'.

    Args:
        sequence (list(str, callable(Maze) -> Maze)): A list of 'actions' where an 'action' has a name and does computation on a Maze and returns a Maze
    """
    main_maze = None
    for (title,action) in sequence:
        (main_maze, time_taken) = run_and_time(lambda:action(main_maze))
        print(f"['{title}' completed in {time_taken:.03f}s]")
    return

# FUNCTIONS END


# MAIN BEGIN

def main():
    run_benchmark_on(SEQ_CHOSEN)
    return

if __name__=="__main__": main()

# MAIN END
