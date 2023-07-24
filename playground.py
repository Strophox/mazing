# OUTLINE BEGIN
"""
A script to try out things from `maze.py` interactively.

Run as main and use console to build, view ... mazes.
"""
# OUTLINE END


# IMPORTS BEGIN

import random
import time
import shutil
from maze import Maze
import colortools

# IMPORTS END


# CONSTANTS BEGIN

CANCEL_TEXT = "*canceled\n"
CELL_PRINT_LIMIT = 10_000
CW = lambda: shutil.get_terminal_size()[0]
CH = lambda: shutil.get_terminal_size()[1]

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
    if maze.width*maze.height < CELL_PRINT_LIMIT:
        string = printer(maze)
        stringwidth = string.find('\n') + 1
        stringheight = string.count('\n') + 1
        if stringwidth <= CW() and stringheight <= CH():
            print(printer(maze))
            return
    print(f"[maze too large for console preview ({cellcount} cells), consider an image option]")
    return

def benchmark(title, function):
    """Run a function, print execution time and return f's result."""
    start_time = time.perf_counter()
    result = function()
    time_taken = time.perf_counter() - start_time
    print(f"['{title}' completed in {time_taken:.03f}s]")
    return result

def maybe_get_new_from_string_options(options, prompt_text):
    user_input = input(f"| {' | '.join(options)}\n{prompt_text} > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    option = autocomplete(user_input,options)
    if option not in options:
        print(f"[unrecognized option '{builder_name}']")
        return
    return option

def maybe_get_new_dimensions(old_dimensions):
    user_input = input(f"Enter sidelength (e.g. '32') or full dimensions (e.g. '80 40') (previously = {old_dimensions[0]} {old_dimensions[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) not in {1,2}:
            raise ValueError("invalid number of arguments")
        new_dimensions = (nums[0], nums[0]) if len(nums)==1 else (nums[0], nums[1])
        return new_dimensions
    except ValueError as e:
        print(f"[error: {e}]")

def maybe_set_new_entrance_exit(maze):
    user_input = input(f"Enter entrance & exit coordinates (default = '0 0 -1 -1', previously = {maze.entrance.coordinates[0]} {maze.entrance.coordinates[1]} {maze.exit.coordinates[0]} {maze.exit.coordinates[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) != 4:
            raise ValueError("invalid number of arguments")
        maze.set_entrance(nums[0], nums[1])
        maze.set_exit(nums[2], nums[3])
        return True
    except ValueError as e:
        print(f"[error: {e}]")
    return

def maybe_load_new_maze():
    user_input = input("Enter `repr` string of a maze > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        data = eval(user_input)
        new_maze = benchmark("loading maze", lambda: Maze.from_repr(data))
        preview(new_maze)
        return new_maze
    except Exception as e:
        print(f"[could not load maze: {e}]")
    return

def maybe_print_maze(maze):
    cellcount = maze.width * maze.height
    if cellcount >= CELL_PRINT_LIMIT and not input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
        print(CANCEL_TEXT,end='')
        return
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
        repr
    ]}
    for name,printer in printers.items():
        print(f"{name}:\n{printer(maze)}")
    return

def maybe_get_new_ratio(old_ratio):
    user_input = input(f"Enter wall:air ratio (default = 1 1, previously = {old_ratio[0]} {old_ratio[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) != 2:
            raise ValueError("invalid number of arguments")
        else:
            new_ratio = (nums[0], nums[1])
            return new_ratio
    except ValueError as e:
        print(f"[error: {e}]")
    return

def maybe_print_solution(maze):
    benchmark("solving",lambda:
        maze.compute_solution())
    cellcount = maze.width * maze.height
    if cellcount >= CELL_PRINT_LIMIT and not input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
        print(CANCEL_TEXT,end='')
        return
    printers = {
        'str_frame_ascii':
            lambda m:Maze.str_frame_ascii(maze, show_solution=True),
        'str_frame_ascii_small':
            lambda m:Maze.str_frame_ascii_small(maze, show_solution=True),
    }
    for name,printer in printers.items():
        print(f"{name}:\n{printer(maze)}")
    return

def maybe_get_new_only(old_only):
    user_input = input(f"Enter number `n` such that only every `n`th frame is recorded during building process (e.g. '3' saves only third the frames) (previously = {old_only}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        new_only = int(user_input)
        return new_only
    except ValueError as e:
        print(f"[error: {e}]")

def maybe_get_new_ms(old_ms):
    user_input = input(f"Enter number of milliseconds per animation frame (e.g. '17' ~ 60fps) (previously = {old_ms}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return
    try:
        new_ms = int(user_input)
        return new_ms
    except ValueError as e:
        print(f"[error: {e}]")

def animation_helper(dimensions, ratio, colormap_name):
    new_maze = None
    maze_runners = {
        'backtracker': (lambda maze, record_frame:
            Maze.grow_tree(maze,record_frame=record_frame)
        ),
    }
    runner_name = 'backtracker'
    image_generator_name = 'img'
    image_generators = { #### color,ratio
        'img': (lambda maze:
            maze.generate_image(
                raster=maze.generate_raster(
                    wall_air_ratio=ratio
                )
            )
        ),
        'imgbrc': (lambda maze:
            maze.compute_distances()
            and()or maze.generate_colorimage(
                gradient_colors=colortools.COLORMAPS[colormap_name][::-1],
                raster=maze.generate_raster(
                    show_distances=True,
                    columnated=False,
                    wall_air_ratio=ratio
                )
            )
        ),
        'imgcol': (lambda maze:
            maze.compute_branchdistances()
            and()or maze.generate_colorimage(
                gradient_colors=colortools.COLORMAPS[colormap_name][::-1],
                raster=maze.generate_raster(
                    show_distances=True,
                    columnated=False,
                    wall_air_ratio=ratio
                )
            )
        ),
    }
    only = 1
    ms = 30
    options_information_text = lambda: f"""
~:--------------------------------------:~
Animation Helper
~:--------------------------------------:~
 Change values or begin recording anim.:
 :  start  - begin rendering process
 Available settings
 :  build  - choose building method
 ;    = '{runner_name}'
 :  imging - type of images to generate
 ;    = '{image_generator_name}'
 :  color  - set colormap (if used)
 ;    = '{colormap_name}'
 :  dim    - set dimensions of maze
 ;    = {dimensions[0]} {dimensions[1]}
 :  ratio  - ratio of wall:air in image
 ;    = {ratio[0]} {ratio[1]}
 :  timefr - ms between animation frames
 ;    = {ms}
 :  onlyfr  - only record n-th frame
 ;    = {only}
 Expected resolution       = {1+dimensions[0]*sum(ratio)} x {1+dimensions[1]*sum(ratio)}
 Expected number of frames = {dimensions[0]*dimensions[1] // only}
 Expected animation length = {ms * (dimensions[0]*dimensions[1] // only) / 1000:.02f}s
~:--------------------------------------:~
    """.strip()
    options = {l[1] for line in options_information_text().splitlines() if (l:=line.split()) and (selection_flag:=l[0]) in ":"}
    options_selection_text = f"Change settings or start animation with 'start' >"
    option = 'help'
    while True:
        match option:
            case 'build':
                new_runner_name =  maybe_get_new_from_string_options(maze_runners, "Choose algorithm to build maze")
                if new_runner_name is not None:
                    runner_name = new_runner_name
            case 'imging':
                new_image_generator_name =  maybe_get_new_from_string_options(image_generators, "Choose imaging technique to make animation")
                if new_image_generator_name is not None:
                    image_generator_name = new_image_generator_name
            case 'color':
                new_colormap_name = maybe_get_new_from_string_options(colortools.COLORMAPS, f"Choose colormap (previously = {old_colormap_name})")
                if new_colormap_name is not None:
                    colormap_name = new_colormap_name
            case 'dim':
                new_dimensions = maybe_get_new_dimensions(dimensions)
                if new_dimensions is not None:
                    dimensions = new_dimensions
            case 'ratio':
                new_ratio = maybe_get_new_ratio(ratio)
                if new_ratio is not None:
                    ratio = new_ratio
            case 'onlyfr':
                new_only = maybe_get_new_only(only)
                if new_only is not None:
                    only = new_only
            case 'timefr':
                new_ms = maybe_get_new_ms(ms)
                if new_ms is not None:
                    ms = new_ms
            case 'help':
                pass
            case 'start':
                (filename, new_maze) = benchmark("animation process", lambda:
                    Maze.save_animation(
                        *dimensions,
                        maze_runner=maze_runners[runner_name],
                        image_generator=image_generators[image_generator_name],
                        frame_only=only,
                        frame_ms=ms,
                        alert_progress_steps=10,
                    )
                )
                print(f"Animation was saved under {filename}")
            case _:
                print("Unrecognized option")
        print(options_information_text())
        user_input = input(options_selection_text).strip()
        if not user_input:
            print("Exiting Animation Helper")
            break
        option = autocomplete(user_input, options)
        if option != user_input:
            print(f"-> {option}")
    return new_maze

# {{{
def analysis(maze):
    # This function is a huge f*cking mess
    temp = (maze.entrance,maze.exit)
    # Statistics helpers
    expectation = lambda sample: not sample or sum(sample) / len(sample)
    variance = lambda sample: not sample or sum(x**2 for x in sample)/len(sample) - expectation(sample)**2
    def sample_to_distribution_chart(pos_int_sample, bars=8):
        if not pos_int_sample: return dict()
        distribution = [pos_int_sample.count(x) for x in range(int(max(pos_int_sample))+1)]
        sum_distribution = len(pos_int_sample)
        #distr_upper = len(distribution) # Naïve: take all values
        #xs = [x for x in range(len(distribution)) if sum(distribution[0:x+1])/sum_distribution > 0.95]
        #distr_upper_ = min(xs) # Better: take 95% and go linear
        l,r = 0,len(distribution)
        x = (l+r)//2
        strictly_increasing = True
        while l < r:
            key = sum(distribution[0:x+1]) / sum_distribution
            if key < 0.95:
                l, x = x, (x+r)//2+1
                if not strictly_increasing:
                    break
            else:
                strictly_increasing = False
                x, r = (l+x)//2, x
        distr_upper = x # Best: Binary search
        sum_distr = sum(distribution)
        slotwidth = (distr_upper // bars) or 1
        distribution_chart = {
            f"[{x}, {x+slotwidth})":
                sum(distribution[x:x+slotwidth]) / sum_distr
            for x in range(0, distr_upper, slotwidth)
        }
        return distribution_chart
    # Formatter helpers
    hbar = lambda num_cols, fill_level: '#' * round(fill_level * num_cols)
    fmt_perc = lambda perc: f"{perc:.2%}"
    fmt_float = lambda float_: f"{float_:.01f}"
    def fmt_dataset(heading, numbers):
        if not numbers: return f" : -- No valid data for '{heading}' statistics."
        statistics = {
            "Expectation":
                expectation(numbers),
            "Deviation":
                variance(numbers)**.5,
            "Maximum":
                max(numbers),
        }
        CWtitle = max(len(title) for title in statistics)
        CWstat = max(len(fmt_float(stat)) for stat in statistics.values())
        stats_header = f" :  {heading}"
        stats_list = '\n'.join(
            f" :      {title.rjust(CWtitle)}  {fmt_float(stat).rjust(CWstat)}"
            for (title,stat) in statistics.items()
        )
        string = f"""{stats_header}\n{stats_list}"""
        return string
    def fmt_barchart(distribution):
        if not distribution: return f" : -- No valid data for bar chart."
        CWtitle = max(len(title) for title in distribution)
        CWperc = max(len(fmt_perc(perc)) for perc in distribution.values())
        table = '\n'.join(
            f" :  {title.rjust(CWtitle)} {fmt_perc(perc).rjust(CWperc)} {hbar(CW()-6-CWtitle-CWperc, perc)}"
            for (title,perc) in distribution.items()
        )
        return table
    # General stuff
    nodecount = maze.width * maze.height
    algorithm_shares = {alg_name:alg_nodecount/nodecount for alg_name,alg_nodecount in maze.generate_algorithm_shares().items()}
    stats_general = f"""
 General Information.
 :    Name  '{maze.name()}'
 :   Width  {maze.width}
 :  Height  {maze.height}
 :    Area  {maze.width*maze.height}
 :  Distribution chart of node types, by algorithm used:
{fmt_barchart(algorithm_shares)}
    """.strip()
    # Solution stuff
    if maze.solution is None:
        benchmark("solving maze", lambda:
            maze.compute_solution())
    len_solution = len(maze.solution)
    (tiles_counts,branch_distances,offshoots_maxlengths,offshoots_avglengths) = benchmark("computing other stats", lambda:
        maze.generate_stats())
    offshoots_maxlengths_distribution = benchmark("distr. chart 2",lambda:
        sample_to_distribution_chart(offshoots_maxlengths))
    offshoots_avglengths_distribution = benchmark("distr. chart 3",lambda:
        sample_to_distribution_chart(offshoots_avglengths))
    stats_solution = f"""
 Solution Path Statistics.
 :  Length of solution path
 :      {len_solution}  ({fmt_perc(len_solution/nodecount)} of area)
 :  Number of offshooting paths from solution
 :      {len(offshoots_maxlengths)}
{fmt_dataset("Maximum distance of an offshooting path", offshoots_maxlengths)}
 :  Distribution chart:
{fmt_barchart(offshoots_maxlengths_distribution)}
    """.strip()
#{fmt_dataset("Average distance of an offshooting path", offshoots_avglengths)}
# :  (Distribution chart:)
#{fmt_barchart(offshoots_avglengths_distribution)}
    # Node stuff
    make_perc = lambda *tileselection: sum(tiles_counts[t] for t in tileselection) / nodecount
    nodetypes = {
        "dead ends":
            make_perc(0b0001,0b0010,0b0100,0b1000),
        "tunnels":
            make_perc(0b0011,0b0101,0b0110,0b1001,0b1010,0b1100),
        "three-ways":
            make_perc(0b0111,0b1011,0b1101,0b1110),
        "intersections":
            make_perc(0b1111)
    }
    stats_nodes = f"""
 Node Statistics.
 :  Distribution chart of node types, by connectivity:
{fmt_barchart(nodetypes)}
    """.strip()
    # Distance stuff
    len_longest_path = benchmark("finding longest path", lambda:
        maze.compute_longest_path())
    sum_branch_distances = sum(branch_distances)
    branch_distance_distribution_chart = benchmark("distr. chart 1",lambda:sample_to_distribution_chart(branch_distances))
    stats_distance = f"""
 Distance Statistics.
 :  Longest possible path
 :      {len_longest_path}  ({fmt_perc(len_longest_path/nodecount)} of area)
 :  Number of nodes on spanning tree leaf branches
 :      {sum_branch_distances}  ({fmt_perc(sum_branch_distances/nodecount)} of area)
{fmt_dataset("Distance from dead end to nearest three-way/intersection", branch_distances)}
 :  Distribution chart:
{fmt_barchart(branch_distance_distribution_chart)}
    """.strip()
    # Final print
    hrulefill = f"~:{'-'*(CW()-4)}:~"
    stats_all = f"""
{hrulefill}
 {stats_general}
{hrulefill}
 {stats_nodes}
{hrulefill}
 {stats_distance}
{hrulefill}
 {stats_solution}
{hrulefill}
    """.strip('\n')
    (maze.entrance,maze.exit) = temp
    return stats_all
# }}}

# FUNCTIONS END


# MAIN BEGIN

def main():
    dimensions = (16,16)
    ratio = (1, 1)
    maze = Maze(*dimensions)
    random.choice(list(Maze.ALGORITHMS.values()))(maze)
    colormap_name = 'viridis'
    image = None
    #import textwrap # remove source code multiline string indents
    commands_information_text = lambda: f"""
~:--------------------------------------:~
 A Mazing Playground
~:--------------------------------------:~
 Enter a command to achieve its effect:
 ;  help   - show this menu
 Maze Generation
 ;  build  - make new maze
 :  dim    - set dimensions for next build
 :  load   - load maze from input
 Modification
 :  maxim  - find & set longest path
 :  goal   - manually set entrance & exit
 :  join   - remove dead ends
 Console Viewing
 ;  print  - text art of maze
 :  txtsol - text art, solutions
 :  stats  - ~statistics of maze
 External Imaging
 ;  img    - png image
 ;  imgsol - png solution image
 :  imgcol - png distance map
 :  imgbrc - branch dist. of spann. tree
 :  color  - set colormap -> `imgcol`
 :  ratio  - set ratio of wall:air size
 :  view   - view latest image
 :  save   - save latest image
 :  anim!  - open animation helper
 (Commands are autocompleted if possible)
 Enter blank command to quit
~:--------------------------------------:~
    """.strip()
    commands = {l[1]:selection_flag==';' for line in commands_information_text().splitlines() if (l:=line.split()) and (selection_flag:=l[0]) in ":;"}
    commands_selection_text = f"\n| {' | '.join(cmd for cmd,sel_flag in commands.items() if sel_flag)} > "
    command = 'help'
    while True:
        match command:
            case 'anim!':
                new_maze = animation_helper(dimensions, ratio, colormap_name)
                if new_maze is not None:
                    maze = new_maze
            case 'build': # Allow user to choose method and build new maze
                new_builder_name = maybe_get_new_from_string_options(Maze.ALGORITHMS, "Choose algorithm to build maze")
                if new_builder_name is not None:
                    maze = Maze(*dimensions)
                    benchmark(new_builder_name, lambda:
                        Maze.ALGORITHMS[new_builder_name](maze))
                    preview(maze)
            case 'color':
                new_colormap_name = maybe_get_new_from_string_options(colortools.COLORMAPS, f"Choose colormap (previously = {old_colormap_name})")
                if new_colormap_name is not None:
                    colormap_name = new_colormap_name
            case 'dim': # Allow user to save new maze size
                new_dimensions = maybe_get_new_dimensions(dimensions)
                if new_dimensions is not None:
                    dimensions = new_dimensions
            case 'goal':
                maybe_set_new_entrance_exit(maze)
            case 'help': # Show help menu
                print(commands_information_text())
            case 'hackerman': # hehe
                injection = []
                while user_input:=input(">>> "): injection.append(user_input)
                try: exec('\n'.join(injection))
                except Exception as e: print(f"<error: {e}>")
            case 'img': # Generate image of current maze and open in external program
                image = benchmark("generating image", lambda:
                    maze.generate_image(raster=maze.generate_raster(wall_air_ratio=ratio)))
                image.show()
            case 'imgbrc':
                benchmark("computing distances", lambda:
                    maze.compute_branchdistances())
                image = benchmark("generating image", lambda:
                    maze.generate_colorimage(gradient_colors=colortools.COLORMAPS[colormap_name][::-1],raster=maze.generate_raster(show_distances=True,columnated=False,wall_air_ratio=ratio)))
                image.show()
            case 'imgcol':
                benchmark("computing distances", lambda:
                    maze.compute_distances())
                image = benchmark("generating image", lambda:
                    maze.generate_colorimage(gradient_colors=colortools.COLORMAPS[colormap_name][::-1],raster=maze.generate_raster(show_distances=True,columnated=False,wall_air_ratio=ratio)))
                image.show()
            case 'imgsol': # Generate image of current maze with solution and open in external program
                benchmark("solving", lambda:
                    maze.compute_solution())
                image = benchmark("generating image", lambda:
                    maze.generate_solutionimage(raster=maze.generate_raster(show_solution=True,wall_air_ratio=ratio)))
                image.show()
            case 'join': # Make current maze unicursal
                benchmark("making unicursal", lambda: maze.make_unicursal())
                preview(maze)
            case 'load': # Let user load maze from a copied `repr` of a maze
                new_maze = maybe_load_new_maze()
                if new_maze is not None:
                    maze = new_maze
            case 'maxim':
                len_longest_path = benchmark("computing longest path", lambda:
                    maze.compute_longest_path())
                print(f"Longest path of length {len_longest_path} (of {maze.width*maze.height} total cells) found.")
            case 'print': # Print currently stored maze in all available styles
                maybe_print_maze(maze)
            case 'ratio':
                new_ratio = maybe_get_new_ratio(ratio)
                if new_ratio is not None:
                    ratio = new_ratio
            case 'save': # Generate image of current maze and save as file
                if image is None:
                    print("Please generate at least one image first (-> `help`)")
                else:
                    benchmark(f"saving {image.filename}",lambda:
                        image.save(image.filename))
            case 'stats':
                try:
                    stats_text = benchmark("complete maze analysis", lambda: analysis(maze))
                    print(stats_text)
                except ValueError as e:
                    print(f"<error: {e}>")
            case 'txtsol':
                maybe_print_solution(maze)
            case 'view':
                if image is None:
                    print("Please generate at least one image first (-> `help`)")
                else:
                    benchmark(f"opening {image.filename} in external editor",lambda:
                        image.show())
            case _: # Non-empty, unrecognized command
                print("Unrecognized command")
        # Get user input and possibly exit loop
        user_input = input(commands_selection_text).strip()
        if not user_input:
            print("goodbye")
            break
        # We autocomplete unambiguous user input so the playground program could be used more quickly
        command = autocomplete(user_input, commands)
        # Show to the user what command he autocompleted to
        if command != user_input:
            print(f"-> {command}")
    return

if __name__=="__main__": main()

# MAIN END
