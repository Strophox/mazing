# OUTLINE BEGIN
"""
A small benchmark script that tests and times some methods from `state.py`.

Note to self: do `python3 -m scalene small_benchmark.py`
"""
# OUTLINE END


# IMPORTS BEGIN

import time
import random
from maze import Maze
from playground import analysis

# IMPORTS END


# CONSTANTS BEGIN

__ = lambda n: (2**n, 2**n)

SEQ_00 = [
      (r"BEGIN", lambda state: state

    ),("test unit", lambda state:
        print("hello, world")

    ),(r"END", lambda state: state)
]

SEQ_01 = [ # Run incrementally larger maze constructions
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

SEQ_02 = [ # Run all maze builders
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

SEQ_03 = [ # Compare growing tree to growing tree with fast pop
    (N := 10) and()or
      (r"BEGIN", lambda state: state

    ),("growing tree", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi:random.randint(0,mxi+1))
    ),("growing tree (fast pop)", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi:random.randint(0,mxi+1),fast_pop=True)

    ),(r"END", lambda state: state)
]

SEQ_04 = [ # Run and save full analyses of all maze types
    (N := 8) and()or
    (filesaver := lambda string:
        (file:=open("runner_output.txt",'a'))
        and()or file.write(string)
        and()or file.close()
        and()or None) and()or
      (r"BEGIN", lambda state: state

    ),("random edges", lambda state:
        Maze.random_edges(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("growing tree", lambda state:
        Maze.growing_tree(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("backtracker", lambda state:
        Maze.backtracker(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("prim", lambda state:
        Maze.prim(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("kruskal", lambda state:
        Maze.kruskal(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("wilson", lambda state:
        Maze.wilson(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)
    ),("division", lambda state:
        Maze.division(*__(N))
    ),("analysis", lambda state:
        analysis(state)
    ),("save to file", lambda state:
           filesaver(state)

    ),(r"END", lambda state: state)
]

SEQ_05 = [ # Run and save short analyses of growing tree with different randomness
    (N := 9) and()or
    (filesaver := lambda string:
        (file:=open("runner_output.txt",'a'))
        and()or file.write(string)
        and()or file.close()
        and()or None) and()or
    (stringer := lambda state: # (maze, (tiles_counts, branch_distances, offshoots_maxlengths, offshoots_avglengths))
        f"""  Avg branch dist {sum(state[1][1])/len(state[1][1]):.02f}
  Len sol path {len(state[0].solution_nodes)}
  Num sol offshoot {len(state[1][2])}
  Avg sol offshoot {sum(state[1][3])/len(state[1][3]):.02f}
  Var sol offshoot {(sum(x**2 for x in state[1][3])/len(state[1][3]) - (sum(state[1][3])/len(state[1][3]))**2)**.5:.02f}
""") and()or
      (r"BEGIN", lambda state: state

    ),("growing tree 100", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<1.00 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 100:\n{stringer(state)}")

    ),("growing tree 99", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.99 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 99:\n{stringer(state)}")

    ),("growing tree 98", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.98 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 98:\n{stringer(state)}")

    ),("growing tree 97", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.97 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 97:\n{stringer(state)}")

    ),("growing tree 96", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.96 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 96:\n{stringer(state)}")

    ),("growing tree 95", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.95 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 95:\n{stringer(state)}")

    ),("growing tree 90", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.90 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 90:\n{stringer(state)}")

    ),("growing tree 85", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.85 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 85:\n{stringer(state)}")

    ),("growing tree 80", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.80 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 80:\n{stringer(state)}")

    ),("growing tree 75", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.75 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 75:\n{stringer(state)}")

    ),("growing tree 70", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.70 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 70:\n{stringer(state)}")

    ),("growing tree 65", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.65 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 65:\n{stringer(state)}")

    ),("growing tree 60", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.60 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 60:\n{stringer(state)}")

    ),("growing tree 55", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.55 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 55:\n{stringer(state)}")

    ),("growing tree 50", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.50 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 50:\n{stringer(state)}")

    ),("growing tree 45", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.45 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 45:\n{stringer(state)}")

    ),("growing tree 40", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.40 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 40:\n{stringer(state)}")

    ),("growing tree 35", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.35 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 35:\n{stringer(state)}")

    ),("growing tree 30", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.30 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 30:\n{stringer(state)}")

    ),("growing tree 25", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.25 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 25:\n{stringer(state)}")

    ),("growing tree 20", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.20 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 20:\n{stringer(state)}")

    ),("growing tree 15", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.15 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 15:\n{stringer(state)}")

    ),("growing tree 10", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.10 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 10:\n{stringer(state)}")

    ),("growing tree 05", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.05 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 05:\n{stringer(state)}")

    ),("growing tree 00", lambda state:
        Maze.growing_tree(*__(N),index_choice=lambda mxi: -1 if random.random()<0.00 else random.randint(0,mxi))
    ),("set longest path", lambda state:
        state.set_longest_path()
        and()or state
    ),("analysis", lambda state:
        (state, state.compute_stats())
    ),("save to file", lambda state:
           filesaver(f"tree 00:\n{stringer(state)}")

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
    benchmark_start = time.perf_counter()
    state = None
    for no, (title,action) in enumerate(sequence):
        begin_time = time.perf_counter()
        state  = action(state)
        end_time   = time.perf_counter()
        print(f"|{no:02}| +{end_time-begin_time:.03f}s | {title}")
    print(f"Benchmark finished after {time.perf_counter()-benchmark_start:.03f}s.")
    return

# FUNCTIONS END


# MAIN BEGIN

def main():
    run_on(CHOSEN_SEQUENCE)
    return

if __name__=="__main__": main()

# MAIN END
