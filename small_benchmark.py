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
# No constants
# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def run_and_time(f):
    """Run a function and return its result and execution time as tuple."""
    start_time = time.perf_counter()
    result = f()
    time_taken = time.perf_counter() - start_time
    return (result, time_taken)

# FUNCTIONS END


# MAIN BEGIN

def main():
    main_maze = None
    # Execute sequence of actions
    sequence = [
          ("BEGIN", lambda maze:
            None
        ),("build div&cqr", lambda maze:
            Maze.divide_conquer(2**9,2**9)
        ),("build tree w/fastpop", lambda maze:
            Maze.growing_tree(2**9,2**9,fast_pop=True)
        ),("build wilson", lambda maze:
            Maze.wilson(2**7,2**7)
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.generate_name()}.png") and()or maze # <- cursed sequential expression composition
        ),("join", lambda maze:
            maze.make_unicursal() and()or maze
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.generate_name()}.png") and()or maze
        ),("END  ", lambda maze:
            None
        ),
    ]
    for (title,action) in sequence:
        (main_maze, time_taken) = run_and_time(lambda:action(main_maze))
        print(f"['{title}' completed in {time_taken:.03f}s]")
    return

if __name__=="__main__": main()

# MAIN END
