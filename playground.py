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
# No constants
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

def preview(maze, max_cellcount=10000):
    """Print maze to the console iff within given size limit."""
    cellcount = maze.width*maze.height
    if cellcount <= max_cellcount:
        print(maze.str_frame())
    else:
        print(f"[no print (cellcount {cellcount})]")
    return

def run_and_time(f):
    """Run a function and return its result and execution time as tuple."""
    start_time = time.perf_counter()
    result = f()
    time_taken = time.perf_counter() - start_time
    return (result, time_taken)

# FUNCTIONS END


# MAIN BEGIN

def main():
    main_dimensions = (16,16)
    main_maze = Maze(*main_dimensions)
    main_image = None
    import textwrap # remove source code multiline string indents
    help_text = textwrap.dedent("""
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
        Enter blank command to exit
        """).strip()
    commands = ["help","build","join","size","load","print","show","save"]
    command = "help"
    while True:
        match command:
            case "help": # Show help menu
                print(help_text)
            case "build": # Allow user to choose method and build new maze
                builders = {x.__name__:x for x in [
                    Maze.backtracker,
                    Maze.growing_tree,
                    Maze.prim,
                    Maze.kruskal,
                    Maze.wilson,
                    Maze.divide_conquer,
                    Maze.quad_divide_conquer,
                ]}
                user_input = input(f"Choose method:\n| " + ' | '.join(builders) + " > ")
                bname = autocomplete(user_input.strip(),builders)
                if bname in builders:
                    (main_maze, time_taken) = run_and_time(lambda:builders[bname](*main_dimensions))
                    print(f"[{bname} completed in {time_taken:.03f}s]")
                    main_cached_image = None
                    preview(main_maze)
                else:
                    print(f"[unrecognized method '{bname}']")
            case "join": # Make current maze unicursal
                (_, time_taken) = run_and_time(lambda:main_maze.make_unicursal())
                print(f"[joining completed in {time_taken:.03f}s]")
                main_cached_image = None
                preview(main_maze)
            case "size": # Allow user to save new maze size
                user_input = input(f"Enter new dimensions 'X Y' (currently: {main_dimensions[0]} {main_dimensions[1]}) > ")
                try:
                    (x,y) = tuple(map(int, user_input.split()))
                    main_dimensions = (x,y)
                except ValueError as e:
                    print(f"[invalid dimensions: {e}]")
            case "load": # Let user load maze from a copied `repr` of a maze
                user_input = input("Enter `repr` string of a maze > ")
                try:
                    main_maze = Maze.from_template(eval(user_input))
                    preview(main_maze)
                except Exception as e:
                    print(f"[could not load maze: {e}]")
            case "solve": # TODO
                main_maze.breadth_first_search()
                print(main_maze.str_frame_ascii()) # TODO
            case "print": # Print currently stored maze in all available styles
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
            case "show": # Generate image of current maze and open in external program
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                print(f"[showing maze in external program]")
                main_cached_image.show()
            case "save": # Generate image of current maze and save as file
                if main_cached_image is None:
                    main_cached_image = main_maze.generate_image()
                filename = f"{main_maze.generate_name()}.png"
                main_cached_image.save(filename)
                print(f"[saved '{filename}']")
            case cmd if cmd in {"debug","exec","sudo","dev","py"}: # hehe
                user_input = input(">>> ")
                try:
                    exec(user_input)
                except Exception as e:
                    print(f"<error: {e}>")
            case _: # Non-empty, unrecognized command
                print("[unrecognized command]")
        # Get user input and possibly exit loop
        user_input = input(f"| {' | '.join(commands)} > ")
        if not user_input.strip():
            print("goodbye")
            break
        # We autocomplete unambiguous user input so the playground program could be used more quickly
        command = autocomplete(user_input.strip(), commands)
        # Show to the user what command he autocompleted to
        if command != user_input:
            print(f"-> {command}")
    return

if __name__=="__main__": main()

# MAIN END


#[[8,9,13,5,5,5,12,1,5,13,13,5,5,4,9,12],[11,6,2,9,12,1,7,5,5,14,2,9,13,5,6,10],[3,12,9,6,3,5,5,5,12,10,9,6,3,12,9,6],[9,14,3,12,1,13,4,9,6,2,10,1,5,6,10,8],[10,3,5,6,9,7,12,3,5,5,6,8,9,5,6,10],[10,9,5,4,10,8,3,5,12,9,5,6,3,12,9,6],[10,11,5,5,6,3,13,4,10,11,5,5,12,10,3,12],[10,3,12,8,9,13,6,1,6,10,1,12,3,14,9,14],[3,12,10,10,10,3,5,12,1,7,12,3,12,3,6,10],[9,14,11,14,11,5,12,3,5,4,10,9,7,4,9,6],[10,10,2,10,10,1,14,8,8,9,6,10,1,12,10,8],[10,3,12,10,10,8,11,6,10,3,5,7,4,3,6,10],[10,8,11,7,14,10,3,12,11,5,5,13,12,8,9,14],[10,10,10,9,6,10,9,6,10,1,13,6,3,6,2,10],[10,10,10,2,9,6,10,1,7,12,3,5,12,1,13,14],[3,6,3,5,6,1,7,5,5,6,1,5,7,5,6,2]]
