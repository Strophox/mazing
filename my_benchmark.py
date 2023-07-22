# OUTLINE BEGIN
"""
A small benchmark script that tests and times some methods from `state.py`.

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
      (r"BEGIN", lambda state: state

    ),("test unit", lambda state:
        print("hello, world")

    ),(r"END", lambda state: state)
]

SEQ_01 = [
      (r"BEGIN", lambda state: state

    ),("maze  0", lambda state:
        Maze(*__(0))
    ),("maze  1", lambda state:
        Maze(*__(1))
    ),("maze  2", lambda state:
        Maze(*__(2))
    ),("maze  3", lambda state:
        Maze(*__(3))
    ),("maze  4", lambda state:
        Maze(*__(4))
    ),("maze  5", lambda state:
        Maze(*__(5))
    ),("maze  6", lambda state:
        Maze(*__(6))
    ),("maze  7", lambda state:
        Maze(*__(7))
    ),("maze  8", lambda state:
        Maze(*__(8))
    ),("maze  9", lambda state:
        Maze(*__(9))
    ),("maze 10", lambda state:
        Maze(*__(10))
    ),("maze 11", lambda state:
        Maze(*__(11))
    ),("maze 12", lambda state:
        Maze(*__(12))
    ),("maze 13", lambda state:
        Maze(*__(13))
    ),("maze 14", lambda state:
        Maze(*__(14))
    ),("maze 15", lambda state:
        Maze(*__(15))
    ),("maze 16", lambda state:
        Maze(*__(16))

    ),(r"END", lambda state: state)
]

SEQ_02 = [
    (N := 10) and()or
      (r"BEGIN", lambda state: state

    ),("random_edges", lambda state:
        Maze.random_edges(*__(N))
    ),("growing_tree", lambda state:
        Maze.growing_tree(*__(N))
    ),("backtracker", lambda state:
        Maze.backtracker(*__(N))
    ),("prim", lambda state:
        Maze.prim(*__(N))
    ),("kruskal", lambda state:
        Maze.kruskal(*__(N))
    ),("wilson", lambda state:
        Maze.wilson(*__(N))
    ),("division", lambda state:
        Maze.division(*__(N))

    ),(r"END", lambda state: state)
]

SEQ_03 = [
      (r"BEGIN", lambda state: state

    ),("division", lambda state:
        Maze.division(*__(9))
    ),("growing_tree", lambda state:
        Maze.growing_tree(*__(9),index_choice=lambda mxi:random.randint(0,mxi+1))
    ),("growing_tree (fast_pop)", lambda state:
        Maze.growing_tree(*__(9),index_choice=lambda mxi:random.randint(0,mxi+1),fast_pop=True)

    ),(r"END", lambda state: state)
]

SEQ_04 = [
      (r"BEGIN", lambda state: state

    ),("backtracker", lambda state:
        Maze.backtracker(*__(10))
    ),("breadth_first_search", lambda state:
        state.breadth_first_search() and()or state# <- cursed sequential expression composition
    ),("SHOW solutionimage", lambda state:
        state.generate_solutionimage().show() and()or state
    ),("make_unicursal", lambda state:
        state.make_unicursal() and()or state
    ),("SHOW solutionimage", lambda state:
        state.generate_solutionimage().show() and()or state

    ),(r"END", lambda state: state)
]

SEQ_05 = [
      (r"BEGIN", lambda state: state

    ),("growing_tree", lambda state:
        Maze.growing_tree(256,256)
    ),("breadth_first_search", lambda state:
        state.breadth_first_search() and()or state
    ),("SAVE colorimage", lambda state:
        state.generate_colorimage().save(f"benchmark_{state.name()}.png") and()or state

    ),(r"END", lambda state: state)
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
    main_state = None
    for (title,action) in sequence:
        begin_time = time.perf_counter()
        main_state  = action(main_state)
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
