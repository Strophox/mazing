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
    (constructor := Maze) and()or # <- cursed sequential expression composition
      (r"BEGIN", lambda state: state

    ),("maze 1", lambda state:
        constructor(*__(0))
    ),("maze 2", lambda state:
        constructor(*__(1))
    ),("maze 4", lambda state:
        constructor(*__(2))
    ),("maze 8", lambda state:
        constructor(*__(3))
    ),("maze 16", lambda state:
        constructor(*__(4))
    ),("maze 32", lambda state:
        constructor(*__(5))
    ),("maze 64", lambda state:
        constructor(*__(6))
    ),("maze 128", lambda state:
        constructor(*__(7))
    ),("maze 256", lambda state:
        constructor(*__(8))
    ),("maze 512", lambda state:
        constructor(*__(9))
    ),("maze 1024", lambda state:
        constructor(*__(10))
    ),("maze 2048", lambda state:
        constructor(*__(11))
    ),("maze 4096", lambda state:
        constructor(*__(12))
    ),("maze 8192", lambda state:
        constructor(*__(13))
    ),("maze 16384", lambda state:
        constructor(*__(14))
    ),("maze 32768", lambda state:
        constructor(*__(15))
    ),("maze 65536", lambda state:
        constructor(*__(16))

    ),(r"END", lambda state: state)
]

SEQ_02 = [
    (N := 10) and()or
      (r"BEGIN", lambda state: state

    ),("random edges", lambda state:
        Maze.random_edges(*__(N))
    ),("growing tree", lambda state:
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
    (N := 10) and()or
      (r"BEGIN", lambda state: state

    ),("growing tree", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi:random.randint(0,mxi+1))
    ),("growing tree (fast pop)", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi:random.randint(0,mxi+1),fast_pop=True)

    ),(r"END", lambda state: state)
]

SEQ_04 = [
      (r"BEGIN", lambda state: state

    ),("backtracker", lambda state:
        Maze.backtracker(*__(10))
    ),("breadth firstsearch", lambda state:
        state.breadth_first_search()
        and()or state
    ),("SHOW solutionimage", lambda state:
        state.generate_solutionimage().show()
        and()or state
    ),("make unicursal", lambda state:
        state.make_unicursal()
        and()or state
    ),("SHOW solutionimage", lambda state:
        state.generate_solutionimage().show()
        and()or state

    ),(r"END", lambda state: state)
]

SEQ_05 = [
      (r"BEGIN", lambda state: state

    ),("growing_tree", lambda state:
        Maze.growing_tree(*__(8))
    ),("breadth_first_search", lambda state:
        state.breadth_first_search()
        and()or state
    ),("set furthest entrance", lambda state:
        (entrance_coords := max(state.nodes(),key=lambda n:n.distance).coordinates)
        and()or state.set_entrance(*entrance_coords)
        and()or state
    ),("breadth first search", lambda state:
        state.breadth_first_search()
        and()or state
    ),("set furthest exit", lambda state:
        (exit_coords := max(state.nodes(),key=lambda n:n.distance).coordinates)
        and()or state.set_exit(*exit_coords)
        and()or state
    ),("breadth first search", lambda state:
        state.breadth_first_search()
        and()or state
    ),("output longest path (BFS)", lambda state:
        (res := (state._entrance.coordinates,state._exit.coordinates,state._exit.distance))
        and()or print(f"BFS: {res[0]} --({res[2]})-> {res[1]}")
        and()or state
    ),("output longest path (DFS)", lambda state:
        (res := state.depth_first_search())
        and()or print(f"DFS: {res[0]} --({res[2]})-> {res[1]}")
        and()or state
    ),("SHOW solutionimage", lambda state:
        state.generate_solutionimage().show()
        and()or state

    ),(r"END", lambda state: state)
]

CHOSEN_SEQUENCE = SEQ_05

# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def run_on(sequence):
    """Runs and benchmarks a sequence of 'actions'.

    Args:
        sequence (list(str, callable(Maze) -> Maze)): A list of 'actions' where an 'action' has a name and does computation on a Maze and returns a Maze
    """
    state = None
    for (title,action) in sequence:
        begin_time = time.perf_counter()
        state  = action(state)
        end_time   = time.perf_counter()
        print(f"['{title}' completed in {end_time-begin_time:.03f}s]")
    return

# FUNCTIONS END


# MAIN BEGIN

def main():
    run_on(CHOSEN_SEQUENCE)
    return

if __name__=="__main__": main()

# MAIN END
