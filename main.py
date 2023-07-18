# OUTLINE BEGIN
"""
A script to try out building and interacting with mazes.

Work in Progress:
- Refactors: "All done!"
- Carvers: All done!
- Solvers:
  * BFS
  * A* pathfinder
- ETC Dreams:
  * Maze navigator (w/ curses)
  * Interactive picker: distance by color
  * Doom (curses) █▯▓▯▒▯░ ".,-~:;=!*#$@"
"""
# OUTLINE END


# IMPORTS BEGIN

from maze_building_algorithms import *
import time

# IMPORTS END


# CONSTANTS BEGIN
# No constants
# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def autocomplete(input_word, full_words):
    candidates = [w for w in full_words if w.startswith(input_word)]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return input_word

def run_and_time(f):
    start_time = time.perf_counter()
    result = f()
    time_taken = time.perf_counter() - start_time
    return (result, time_taken)

def display(maze, limit=100*100):
    cellcount = maze.width*maze.height
    if cellcount <= limit:
        print(maze.str_frame())
    else:
        print(f"[no print (cellcount {cellcount})]")
    return None

def benchmark():
    """Run `python3 -m scalene maze.py`
    """
    sq = lambda n: (n,n)
    # Execute actions
    benchmark_maze = Maze(1,1)
    for (title,action) in [
          ("BEGIN", lambda maze:
            maze
        ),("div-cqr", lambda maze:
             division_maze(sq(2**9))
        ),("grow w/fastpop", lambda maze:
            growing_tree_maze(sq(2**9),fast_pop=True)
        ),("wilson", lambda maze:
            wilson_maze(sq(2**7))
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.make_name()}.png") and()or maze
        ),("join", lambda maze:
            make_unicursal(maze) and()or maze # cursed sequential composition
        ),("save image", lambda maze:
            maze.generate_image().save(f"{maze.make_name()}.png") and()or maze
        ),("END  ", lambda maze:
            maze
        ),
    ]:
        (benchmark_maze, secs) = run_and_time(lambda:action(benchmark_maze))
        print(f"['{title}' completed in {secs:.03f}s]")
    return None

def sandbox():
    main_dimensions = (16,16)
    main_maze = Maze(*main_dimensions)
    main_image = None
    import textwrap # remove source code multiline string indents
    help_menu_text = textwrap.dedent("""
        A Mazing Sandbox
        | help  : show this menu
        Editing
        | build : new maze
        | join  : /remove dead ends
        | size  : for next maze
        | load  : maze from string
        Viewing
        | print : latest maze, ascii art
        | show  : latest maze, external png
        | save  : external png
        >""")
    commands = ["help","build","join","size","load","print","show","save"]
    command = "help"
    while command:
        match command:
            case "help":
                user_input = input(help_menu_text)
                command = autocomplete(user_input.strip(), commands)
                continue
            case "build":
                builders = {x.__name__:x for x in [
                    backtracker_maze,
                    growing_tree_maze,
                    prim_maze,
                    kruskal_maze,
                    wilson_maze,
                    division_maze,
                    quarter_division_maze,
                ]}
                user_input = input(f"Choose method:\n| " + ' | '.join(builders) + "\n>")
                name = autocomplete(user_input.strip(),builders)
                if name in builders:
                    (main_maze, secs) = run_and_time(lambda: builders[name](main_dimensions))
                    print(f"[{name} completed in {secs:.03f}s]")
                    main_cached_image = None
                    display(main_maze)
                else:
                    print(f"[unrecognized algorithm '{name}']")
            case "join":
                (_, secs) = run_and_time(lambda: make_unicursal(main_maze))
                print(f"[joining completed in {secs:.03f}s]")
                main_cached_image = None
                display(main_maze)
            case "size":
                user_input = input("Enter dimensions 'X Y' >")
                try:
                    main_dimensions = (_, _) = tuple(map(int, user_input.split()))
                except Exception as e:
                    print(f"[invalid dimensions: {e}]")
            case "load":
                user_input = input("Enter string `repr`esentation (e.g. '[[9,5..]]') >")
                try:
                    main_maze = Maze.from_grid(eval(user_input.strip()))
                    display(main_maze)
                except Exception as e:
                    print(f"[could not load maze: {e}]")
            case "print":
                printers = {x.__name__:x for x in [
                    Maze.str_bitmap,
                    Maze.str_block_double,
                    Maze.str_block,
                    Maze.str_block_half,
                    Maze.str_block_quarter,
                    Maze.str_pipes,
                    Maze.str_frame,
                    Maze.str_frame_ascii,
                    Maze.str_frame_ascii_small,
                    repr,
                ]}
                for name,printer in printers.items():
                    print(f"{name}:\n{printer(main_maze)}")
            case "show":
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                print(f"[showing maze in external program]")
                main_cached_image.show()
            case "save":
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                filename = f"{main_maze.make_name()}.png"
                main_cached_image.save(filename)
                print(f"[saved '{filename}']")
            case cmd if cmd in {"debug","exec","sudo","dev","py"}:
                user_input = input(">>> ")
                try:
                    exec(user_input)
                except Exception as e:
                    print(f"<error: {e}>")
            case _:
                print("[unrecognized command]")
        user_input = input(f"""| {' | '.join(commands)} >""")
        command = autocomplete(user_input.strip(), commands)
    print("goodbye")
    return None

# FUNCTIONS END


# MAIN BEGIN

def main():
    if True:
        sandbox()
    else:
        benchmark()

if __name__=="__main__": main()

# MAIN END


#[[8,9,13,5,5,5,12,1,5,13,13,5,5,4,9,12],[11,6,2,9,12,1,7,5,5,14,2,9,13,5,6,10],[3,12,9,6,3,5,5,5,12,10,9,6,3,12,9,6],[9,14,3,12,1,13,4,9,6,2,10,1,5,6,10,8],[10,3,5,6,9,7,12,3,5,5,6,8,9,5,6,10],[10,9,5,4,10,8,3,5,12,9,5,6,3,12,9,6],[10,11,5,5,6,3,13,4,10,11,5,5,12,10,3,12],[10,3,12,8,9,13,6,1,6,10,1,12,3,14,9,14],[3,12,10,10,10,3,5,12,1,7,12,3,12,3,6,10],[9,14,11,14,11,5,12,3,5,4,10,9,7,4,9,6],[10,10,2,10,10,1,14,8,8,9,6,10,1,12,10,8],[10,3,12,10,10,8,11,6,10,3,5,7,4,3,6,10],[10,8,11,7,14,10,3,12,11,5,5,13,12,8,9,14],[10,10,10,9,6,10,9,6,10,1,13,6,3,6,2,10],[10,10,10,2,9,6,10,1,7,12,3,5,12,1,13,14],[3,6,3,5,6,1,7,5,5,6,1,5,7,5,6,2]]
