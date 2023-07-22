# OUTLINE BEGIN
"""
A script to try out things from `maze.py` interactively.

Run as main and use console to build, view ... mazes.
"""
# OUTLINE END


# IMPORTS BEGIN

from maze import Maze
import time
import shutil

# IMPORTS END


# CONSTANTS BEGIN

CANCEL_TEXT = "*canceled\n"
PRINT_LIMIT = 100_000
WX = lambda: shutil.get_terminal_size()[0]
WY = lambda: shutil.get_terminal_size()[1]

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

def fits_into_console(string):
    stringwidth = string.find('\n') + 1
    stringheight = string.count('\n') + 1
    return stringwidth <= WX() and stringheight <= WY()

def preview(maze, printer=Maze.str_frame):
    """Print maze to the console iff within given size limit."""
    string = printer(maze)
    charcount = len(string)
    if charcount < PRINT_LIMIT and fits_into_console(string):
        print(printer(maze))
    else:
        print(f"[maze too large for console preview ({charcount} characters), consider an image option]")
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
    latest_image = None
    #import textwrap # remove source code multiline string indents
    help_text = """
~:--------------------------------------:~
 A Mazing Playground
~:--------------------------------------:~
 Enter a command to achieve its effect:
 ;  help   - show this menu
 Building:
 ;  build  - make new maze
 :  join   - remove dead ends
 Viewing:
 ;  print  - text art of maze
 ;  img    - png image of maze
 Solving:
 ;  solve  - text art solution
 :  imgsol - png solution
 Visualisation:
 :  data   - stats about current maze
 :  imgcol - png colored distances
 Settings:
 :  size   - set size of next maze
 :  view   - view last generated image
 :  save   - save last generated image
 :  load   - load maze from string
 (Commands are autocompleted)
 Enter blank command to quit
~:--------------------------------------:~
""".strip()
    commands = {l[1]:l[0]==';' for line in help_text.split('\n') if (l:=line.split()) and l[0] in ":;"}
    command_prompt = f"\n| {' | '.join(cmd for cmd, in_selection in commands.items() if in_selection)} > "
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
                user_input = input(f"Choose algorithm\n| {' | '.join(builders)} > ").strip()
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
                hrulefill = lambda: print(f"~:{'-'*(WX()-4)}:~")
                longest_path_distance = benchmark("finding longest path", lambda:maze.set_longest_path())
                (tiles_counts, distances_counts) = benchmark("computing other stats", lambda:maze.compute_stats())
                hrulefill()
                print(" Tile distribution:")
                max_tilecount = max(tiles_counts)
                for tile,tilecount in zip(" ╶╵└╴─┘┴╷┌│├┐┬┤┼",tiles_counts):
                    print(f"{tile} | {'#'*round(tilecount/max_tilecount * (WX()-2-3))}")
                max_distance = max(distances_counts)
                max_distancecount = max(distances_counts.values())
                hrulefill()
                print(" Distance distribution.")
                for dist in range(max_distance+1):
                    distancecount = distances_counts.get(dist, 0)
                    print(f"{dist} | {'#'*round(distancecount/max_distancecount * (WX()-3-3))}")
                hrulefill()
                print(f" The longest path in the maze measures {longest_path_distance}")
                hrulefill()
            case "help": # Show help menu
                print(help_text)
            case "hackerman": # hehe
                injection = []
                while user_input:=input(">>> "):
                    injection.append(user_input)
                try:
                    exec('\n'.join(injection))
                except Exception as e:
                    print(f"<error: {e}>")
            case "img": # Generate image of current maze and open in external program
                latest_image = benchmark("generating image", lambda:maze.generate_image())
                latest_image.show()
            case "imgsol": # Generate image of current maze with solution and open in external program
                benchmark("solving", lambda:maze.compute_solution())
                latest_image = benchmark("generating image", lambda:maze.generate_solutionimage())
                latest_image.show()
            case "imgcol":
                benchmark("computing distances", lambda:maze.compute_distances())
                latest_image = benchmark("generating image", lambda:maze.generate_colorimage())
                latest_image.show()
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
                repr_string = repr(maze)
                charcount = len(repr_string)
                if charcount < PRINT_LIMIT or input(f"Maze contains a lot of cells ({maze.width*maze.height}), proceed anyway ('Y')? >")=='Y':
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
                    ]}
                    for name,printer in printers.items():
                        print(f"{name}:\n{printer(maze)}")
                    print(f"Maze `repr`:\n{repr_string}")
                else:
                    print(CANCEL_TEXT,end='')
            case "save": # Generate image of current maze and save as file
                if latest_image is not None:
                    run_and_print_time("saving",lambda:latest_image.save(latest_image.filename))
                else:
                    print("No image generated yet, see `help` on how to do so")
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
            case "view":
                if latest_image is not None:
                    latest_image.show()
                else:
                    print("No image generated yet, see `help` on how to do so")
            case _: # Non-empty, unrecognized command
                print("Unrecognized command")
        # Get user input and possibly exit loop
        user_input = input(command_prompt).strip()
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
