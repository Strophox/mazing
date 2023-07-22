# OUTLINE BEGIN
"""
A script to try out things from `maze.py` interactively.

Run as main and use console to build, view ... mazes.
"""
# OUTLINE END


# IMPORTS BEGIN

from maze import Maze
import time

# IMPORTS END


# CONSTANTS BEGIN

PRINT_LIMIT = 10_000
CANCEL_TEXT = "*canceled\n"

# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def autocomplete(input_word, full_words):
    """Autocomplete word (only) if there's a unique word completion from list.

    Args:
        input_word (str): Word to be completed
        full_words (list(str)): Available words to be completed to

    Returns:
        str: A unique match from full_words, otherwise input_word
    """
    candidates = [w for w in full_words if w.startswith(input_word)]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return input_word

def preview(maze, printer=Maze.str_frame):
    """Print maze to the console iff within given size limit."""
    cellcount = maze.width*maze.height
    if cellcount < PRINT_LIMIT:
        print(printer(maze))
    else:
        print(f"[maze too large for console preview ({cellcount} cells), consider an image option]")
    return

def benchmark(title, function):
    """Run a function, print execution time and return f's result."""
    start_time = time.perf_counter()
    result = function()
    time_taken = time.perf_counter() - start_time
    print(f"['{title}' completed in {time_taken:.03f}s]")
    return result

# FUNCTIONS END


# MAIN BEGIN

def main():
    dimensions = (16,16)
    maze = Maze.growing_tree(*dimensions)
    cache_image = None
    #import textwrap # remove source code multiline string indents
    help_text = """
~:--------------------------------------:~
 A Mazing Playground
~:--------------------------------------:~
 Enter a command to achieve its effect:
 :  help   - show this menu
 Building:
 :  build  - make new maze
 ;  join   - remove dead ends
 Viewing:
 :  print  - text art of maze
 :  img    - png image of maze
 Solving:
 :  solve  - text art solution
 ;  imgsol - png solution
 Visualisation:
 ;  data   - analysis of maze
 ;  imgcol - png colored distances
 Settings:
 ;  size   - set size of next maze
 ;  save   - save last png image
 ;  load   - load maze from string
 (Commands are autocompleted)
 (Blank command to exit)
~:--------------------------------------:~
""".strip()
    commands = {l[1]:l[0]==':' for line in help_text.split('\n') if (l:=line.split()) and l[0] in ":;"}
    command = "help"
    while True:
        match command:
            case "build": # Allow user to choose method and build new maze
                builders = {x.__name__:x for x in [
                    Maze.growing_tree,
                    Maze.backtracker,
                    Maze.prim,
                    Maze.kruskal,
                    Maze.wilson,
                    Maze.division,
                    Maze.random_edges
                ]}
                user_input = input(f"Choose method:\n| " + ' | '.join(builders) + " > ").strip()
                if user_input:
                    buildername = autocomplete(user_input,builders)
                    if buildername in builders:
                        maze = benchmark(buildername, lambda:builders[buildername](*dimensions))
                        preview(maze)
                    else:
                        print(f"[unrecognized building method '{buildername}']")
                else:
                    print(CANCEL_TEXT,end='')
            case "data":
                data = benchmark("maze analysis", lambda:maze.depth_first_search())
                print(data)#TODO
            case "help": # Show help menu
                print(help_text)
            case "hackerman": # hehe
                user_input = input(">>> ").strip()
                if user_input:
                    try:
                        exec(user_input)
                    except Exception as e:
                        print(f"<error: {e}>")
                else:
                    print(CANCEL_TEXT,end='')
            case "img": # Generate image of current maze and open in external program
                cached_image = benchmark("generating image", lambda:maze.generate_image())
                cached_image.show()
            case "imgsol": # Generate image of current maze with solution and open in external program
                benchmark("solving", lambda:maze.compute_solution())
                cached_image = benchmark("generating image", lambda:maze.generate_solutionimage())
                cached_image.show()
            case "imgcol":
                benchmark("computing distances", lambda:maze.compute_distances())
                cached_image = benchmark("generating image", lambda:maze.generate_colorimage())
                cached_image.show()
            case "join": # Make current maze unicursal
                benchmark("making unicursal", lambda:maze.make_unicursal())
                preview(maze)
            case "load": # Let user load maze from a copied `repr` of a maze
                user_input = input("Enter `repr` string of a maze > ").strip()
                if user_input:
                    try:
                        data = eval(user_input)
                        maze = benchmark("loading into maze", Maze.from_repr(data))
                        preview(maze)
                    except Exception as e:
                        print(f"[could not load maze: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
            case "print": # Print currently stored maze in all available styles
                cellcount = maze.width*maze.height
                if cellcount < PRINT_LIMIT or input(f"Maze contains a lot of cells ({cellcount}), proceed ('Y')? >")=='Y':
                    printers = {x.__name__:x for x in [
                        Maze.str_raster,
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
                        print(f"{name}:\n{printer(maze)}")
                else:
                    print(CANCEL_TEXT,end='')
            case "save": # Generate image of current maze and save as file
                if cached_image is not None:
                    run_and_print_time("saving",lambda:cached_image.save(cached_image.filename))
                else:
                    print("No image generated yet, see `help` on ways of doing so")
            case "size": # Allow user to save new maze size
                user_input = input(f"Enter sidelength (e.g. '32') or dimensions (e.g. '80 40') (currently = {dimensions[0]} {dimensions[1]}) > ").strip()
                if user_input:
                    try:
                        nums = [int(s) for s in user_input.split()]
                        if len(nums) == 1:
                            dimensions = (nums[0], nums[0])
                        elif len(nums) == 2:
                            dimensions = (nums[0], nums[1])
                        else:
                            raise ValueError("too many arguments")
                    except ValueError as e:
                        print(f"[error: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
            case "solve":
                benchmark("solving",lambda:maze.compute_solution())
                preview(maze, lambda maze: maze.str_frame_ascii(show_solution=True))
            case _: # Non-empty, unrecognized command
                print("Unrecognized command")
        # Get user input and possibly exit loop
        user_input = input(f"\n| {' | '.join(cmd for cmd,flag in commands.items() if flag)} > ").strip()
        if not user_input:
            print("goodbye")
            break
        # We autocomplete unambiguous user input so the playground program could be used more quickly
        command = autocomplete(user_input.strip().lower(), commands)
        # Show to the user what command he autocompleted to
        if command != user_input:
            print(f"-> {command}")
    return

if __name__=="__main__": main()

# MAIN END


#[[8,9,13,5,5,5,12,1,5,13,13,5,5,4,9,12],[11,6,2,9,12,1,7,5,5,14,2,9,13,5,6,10],[3,12,9,6,3,5,5,5,12,10,9,6,3,12,9,6],[9,14,3,12,1,13,4,9,6,2,10,1,5,6,10,8],[10,3,5,6,9,7,12,3,5,5,6,8,9,5,6,10],[10,9,5,4,10,8,3,5,12,9,5,6,3,12,9,6],[10,11,5,5,6,3,13,4,10,11,5,5,12,10,3,12],[10,3,12,8,9,13,6,1,6,10,1,12,3,14,9,14],[3,12,10,10,10,3,5,12,1,7,12,3,12,3,6,10],[9,14,11,14,11,5,12,3,5,4,10,9,7,4,9,6],[10,10,2,10,10,1,14,8,8,9,6,10,1,12,10,8],[10,3,12,10,10,8,11,6,10,3,5,7,4,3,6,10],[10,8,11,7,14,10,3,12,11,5,5,13,12,8,9,14],[10,10,10,9,6,10,9,6,10,1,13,6,3,6,2,10],[10,10,10,2,9,6,10,1,7,12,3,5,12,1,13,14],[3,6,3,5,6,1,7,5,5,6,1,5,7,5,6,2]]
