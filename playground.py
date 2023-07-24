# OUTLINE BEGIN
"""
A script to try out things from `maze.py` interactively.

Run as main and use console to build, view ... mazes.
"""
# OUTLINE END


# IMPORTS BEGIN

import time
import shutil
from maze import Maze
import colortools

# IMPORTS END


# CONSTANTS BEGIN

CANCEL_TEXT = "*canceled\n"
CELL_LIMIT = 10_000
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
    if maze.width*maze.height < CELL_LIMIT:
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
        if not numbers: return f"No valid data for '{heading}' statistics."
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
        if not distribution: return f"No valid data for bar chart."
        CWtitle = max(len(title) for title in distribution)
        CWperc = max(len(fmt_perc(perc)) for perc in distribution.values())
        table = '\n'.join(
            f" :  {title.rjust(CWtitle)} {fmt_perc(perc).rjust(CWperc)} {hbar(CW()-6-CWtitle-CWperc, perc)}"
            for (title,perc) in distribution.items()
        )
        return table
    # General stuff
    nodecount = maze.width * maze.height
    stats_general = f"""
 General Information.
 :    Name  '{maze.name()}'
 :   Width  {maze.width}
 :  Height  {maze.height}
 :    Area  {maze.width*maze.height}
    """.strip()
    # Solution stuff
    if maze.solution_nodes is None:
        benchmark("solving maze", lambda:
            maze.compute_solution())
    len_solution = len(maze.solution_nodes)
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
{fmt_barchart(offshoots_maxlengths_distribution)}
    """.strip()
#{fmt_dataset("Average distance of an offshooting path", offshoots_avglengths)}
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

# FUNCTIONS END


# MAIN BEGIN

def main():
    dimensions = (16,16)
    wall_air_ratio = (1, 1)
    maze = Maze(*dimensions)
    colormap = None
    image = None
    #import textwrap # remove source code multiline string indents
    help_text = """
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
 (Commands are autocompleted if possible)
 Enter blank command to quit
~:--------------------------------------:~
    """.strip()
    commands = {l[1]:selection_flag==';' for line in help_text.splitlines() if (l:=line.split()) and (selection_flag:=l[0]) in ":;"}
    command_prompt = f"\n| {' | '.join(cmd for cmd,sel_flag in commands.items() if sel_flag)} > "
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
                        maze = Maze(*dimensions)
                        benchmark(buildername, lambda:
                            builders[buildername](maze))
                        preview(maze)
                    else:
                        print(f"[unrecognized algorithm '{buildername}']")
                else:
                    print(CANCEL_TEXT,end='')
            case "color":
                user_input = input(f"Choose colormap\n| {' | '.join(colortools.COLORMAPS)} > ").strip()
                if user_input:
                    colormapname = autocomplete(user_input,colortools.COLORMAPS)
                    if colormapname in colortools.COLORMAPS:
                        if colormapname != user_input:
                            print(f"-> {colormapname}")
                        colormap = colortools.COLORMAPS[colormapname][::-1]
                    else:
                        print(f"[unrecognized colormap '{colormapname}']")
            case "dim": # Allow user to save new maze size
                user_input = input(f"Enter sidelength (e.g. '32') or dimensions (e.g. '80 40') (currently = {dimensions[0]} {dimensions[1]}) > ").strip()
                if user_input:
                    try:
                        nums = [int(s) for s in user_input.split()]
                        if len(nums) == 1:
                            dimensions = (nums[0], nums[0])
                        elif len(nums) == 2:
                            dimensions = (nums[0], nums[1])
                        else:
                            raise ValueError("invalid number of arguments")
                    except ValueError as e:
                        print(f"[error: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
            case "goal":
                user_input = input(f"Enter entrance & exit coordinates (default = '0 0 -1 -1', currently = {maze.entrance.coordinates[0]} {maze.entrance.coordinates[1]} {maze.exit.coordinates[0]} {maze.exit.coordinates[1]}) > ").strip()
                if user_input:
                    try:
                        nums = [int(s) for s in user_input.split()]
                        if len(nums) == 4:
                            maze.set_entrance(nums[0], nums[1])
                            maze.set_exit(nums[2], nums[3])
                        else:
                            raise ValueError("invalid number of arguments")
                    except ValueError as e:
                        print(f"[error: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
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
                image = benchmark("generating image", lambda:
                    maze.generate_image(raster=maze.generate_raster(wall_air_ratio=wall_air_ratio)))
                image.show()
            case "imgbrc":
                benchmark("computing distances", lambda:
                    maze.compute_branchdistances())
                image = benchmark("generating image", lambda:
                    maze.generate_colorimage(gradient_colors=colormap,raster=maze.generate_raster(show_distances=True,columnated=False,wall_air_ratio=wall_air_ratio)))
                image.show()
            case "imgcol":
                benchmark("computing distances", lambda:
                    maze.compute_distances())
                image = benchmark("generating image", lambda:
                    maze.generate_colorimage(gradient_colors=colormap,raster=maze.generate_raster(show_distances=True,columnated=False,wall_air_ratio=wall_air_ratio)))
                image.show()
            case "imgsol": # Generate image of current maze with solution and open in external program
                benchmark("solving", lambda:
                    maze.compute_solution())
                image = benchmark("generating image", lambda:
                    maze.generate_solutionimage(raster=maze.generate_raster(show_solution=True,wall_air_ratio=wall_air_ratio)))
                image.show()
            case "join": # Make current maze unicursal
                benchmark("making unicursal", lambda:
                    maze.make_unicursal())
                preview(maze)
            case "load": # Let user load maze from a copied `repr` of a maze
                user_input = input("Enter `repr` string of a maze > ").strip()
                if user_input:
                    try:
                        data = eval(user_input)
                        maze = benchmark("loading into maze", lambda:
                            Maze.from_repr(data))
                        preview(maze)
                    except Exception as e:
                        print(f"[could not load maze: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
            case "maxim":
                len_longest_path = benchmark("computing longest path", lambda:
                    maze.compute_longest_path())
                print(f"Longest path of length {len_longest_path} (of {maze.width*maze.height} total cells) found!")
            case "print": # Print currently stored maze in all available styles
                cellcount = maze.width*maze.height
                if cellcount < CELL_LIMIT or input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
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
                else:
                    print(CANCEL_TEXT,end='')
            case "ratio":
                user_input = input(f"Enter wall:air ratio (default = 1 1, currently = {wall_air_ratio[0]} {wall_air_ratio[1]}) > ").strip()
                if user_input:
                    try:
                        nums = [int(s) for s in user_input.split()]
                        if len(nums) == 2:
                            wall_air_ratio = (nums[0], nums[1])
                        else:
                            raise ValueError("invalid number of arguments")
                    except ValueError as e:
                        print(f"[error: {e}]")
                else:
                    print(CANCEL_TEXT,end='')
            case "save": # Generate image of current maze and save as file
                if image is None:
                    print("No image type has been tried yet, please choose one first (see `help`)")
                else:
                    benchmark(f"saving {image.filename}",lambda:
                        image.save(image.filename))
            case "stats":
                stats_text = benchmark("total maze analysis execution", lambda:
                    analysis(maze))
                print(stats_text)
            case "txtsol":
                benchmark("solving",lambda:
                    maze.compute_solution())
                cellcount = maze.width*maze.height
                if cellcount < CELL_LIMIT or input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
                    printers = {
                        'str_frame_ascii':
                            lambda m:Maze.str_frame_ascii(maze, show_solution=True),
                        'str_frame_ascii_small':
                            lambda m:Maze.str_frame_ascii_small(maze, show_solution=True),
                    }
                    for name,printer in printers.items():
                        print(f"{name}:\n{printer(maze)}")
                else:
                    print(CANCEL_TEXT,end='')
            case "view":
                if image is None:
                    print("No image type has been tried yet, please choose one first (see `help`)")
                else:
                    benchmark(f"opening {image.filename} in external editor",lambda:
                        image.show())
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

#(['2023.07.24-00h41m38', 'tree', 'dfs'], (0, 0), (31, 31), [[1, 13, 5, 12, 9, 5, 5, 5, 5, 12, 1, 13, 5, 12, 8, 9, 5, 5, 5, 13, 13, 5, 5, 5, 5, 5, 12, 9, 5, 5, 12, 8], [9, 6, 1, 7, 6, 8, 9, 5, 12, 3, 5, 6, 9, 6, 11, 7, 4, 9, 12, 2, 3, 12, 9, 5, 5, 4, 10, 11, 12, 8, 10, 10], [10, 9, 12, 9, 4, 11, 6, 9, 14, 9, 13, 12, 10, 1, 7, 12, 9, 6, 3, 5, 5, 6, 3, 12, 9, 5, 6, 2, 10, 10, 3, 14], [11, 6, 10, 3, 5, 6, 9, 6, 10, 10, 10, 2, 3, 5, 12, 10, 10, 9, 13, 5, 12, 9, 13, 6, 10, 1, 13, 5, 6, 10, 9, 6], [10, 8, 3, 12, 9, 5, 6, 1, 6, 10, 10, 9, 5, 5, 6, 2, 10, 2, 3, 12, 2, 10, 10, 9, 6, 9, 6, 1, 13, 14, 3, 12], [10, 3, 12, 10, 10, 9, 12, 9, 5, 6, 10, 10, 9, 12, 9, 12, 3, 13, 12, 11, 5, 6, 3, 6, 9, 6, 9, 13, 6, 2, 9, 6], [10, 9, 14, 10, 11, 6, 3, 14, 1, 12, 3, 6, 10, 3, 6, 3, 12, 2, 10, 3, 12, 1, 13, 5, 6, 9, 14, 2, 9, 12, 10, 8], [3, 6, 10, 10, 2, 9, 12, 3, 5, 7, 12, 9, 7, 12, 1, 12, 10, 9, 6, 8, 10, 9, 6, 9, 5, 6, 3, 5, 6, 3, 7, 14], [9, 4, 10, 3, 5, 6, 3, 5, 12, 8, 10, 3, 12, 10, 9, 6, 3, 6, 9, 7, 6, 10, 8, 3, 12, 1, 13, 5, 12, 9, 12, 10], [11, 5, 6, 9, 13, 12, 9, 5, 6, 10, 10, 1, 6, 10, 10, 9, 5, 5, 6, 9, 5, 14, 11, 5, 7, 5, 6, 1, 6, 10, 10, 10], [3, 12, 1, 6, 10, 2, 3, 12, 9, 14, 3, 5, 5, 6, 10, 10, 9, 4, 9, 6, 9, 14, 2, 9, 5, 5, 5, 5, 5, 14, 10, 2], [8, 10, 9, 12, 3, 12, 9, 6, 10, 3, 12, 1, 5, 12, 11, 6, 11, 12, 11, 4, 10, 10, 9, 6, 9, 5, 12, 9, 12, 2, 3, 12], [10, 3, 6, 11, 5, 6, 11, 12, 11, 12, 11, 5, 5, 6, 10, 1, 6, 3, 6, 9, 6, 10, 10, 8, 10, 1, 7, 6, 3, 5, 5, 14], [11, 5, 4, 10, 9, 12, 10, 10, 2, 10, 2, 9, 5, 12, 3, 5, 5, 13, 5, 6, 1, 6, 10, 10, 10, 9, 5, 12, 9, 12, 9, 6], [11, 5, 5, 6, 10, 10, 2, 10, 9, 6, 9, 6, 9, 14, 9, 12, 9, 6, 9, 5, 5, 5, 6, 10, 3, 6, 9, 6, 10, 2, 3, 12], [3, 5, 12, 9, 6, 3, 5, 6, 10, 9, 6, 8, 10, 2, 10, 3, 6, 9, 6, 9, 5, 5, 5, 7, 12, 9, 6, 8, 11, 12, 9, 6], [8, 9, 6, 3, 5, 5, 5, 12, 3, 7, 5, 6, 3, 5, 6, 9, 5, 6, 1, 7, 5, 4, 9, 5, 14, 10, 1, 7, 14, 3, 6, 8], [10, 10, 1, 13, 5, 12, 9, 6, 9, 5, 12, 9, 5, 5, 5, 6, 8, 9, 13, 5, 5, 5, 6, 8, 10, 3, 5, 12, 3, 5, 12, 10], [10, 3, 5, 6, 9, 6, 3, 12, 3, 12, 10, 3, 12, 9, 5, 5, 7, 6, 3, 12, 9, 5, 12, 10, 10, 9, 12, 10, 9, 4, 10, 10], [11, 5, 5, 4, 10, 9, 12, 3, 5, 6, 10, 9, 6, 3, 5, 5, 5, 12, 9, 6, 10, 9, 6, 3, 7, 6, 10, 10, 10, 9, 6, 10], [11, 5, 5, 12, 10, 10, 3, 5, 5, 12, 10, 3, 5, 5, 12, 9, 4, 10, 3, 12, 10, 3, 5, 12, 1, 12, 10, 10, 3, 7, 5, 14], [3, 13, 4, 3, 6, 3, 5, 12, 8, 11, 7, 5, 5, 12, 10, 11, 12, 10, 8, 10, 3, 12, 8, 3, 12, 10, 10, 10, 9, 5, 12, 2], [8, 10, 9, 5, 5, 5, 12, 10, 3, 6, 9, 5, 12, 2, 10, 2, 3, 7, 6, 3, 13, 6, 3, 12, 10, 11, 6, 10, 11, 4, 3, 12], [11, 6, 3, 5, 5, 12, 3, 6, 9, 12, 10, 8, 3, 12, 10, 9, 5, 5, 5, 12, 3, 5, 12, 10, 10, 3, 12, 3, 6, 9, 12, 10], [10, 9, 5, 5, 4, 10, 9, 5, 6, 3, 6, 3, 12, 10, 10, 10, 9, 5, 4, 3, 5, 12, 3, 14, 3, 12, 11, 4, 9, 6, 10, 10], [10, 3, 12, 9, 13, 6, 3, 5, 5, 12, 1, 13, 6, 10, 3, 6, 10, 9, 5, 13, 12, 10, 9, 7, 4, 10, 2, 9, 6, 8, 3, 14], [10, 9, 6, 10, 2, 9, 5, 5, 5, 6, 9, 6, 9, 6, 9, 5, 7, 6, 9, 6, 2, 10, 2, 9, 12, 10, 9, 6, 9, 7, 5, 6], [10, 11, 12, 3, 12, 10, 9, 4, 9, 5, 7, 12, 3, 12, 3, 5, 5, 12, 3, 5, 12, 3, 5, 14, 3, 6, 10, 1, 14, 9, 12, 8], [10, 10, 3, 12, 10, 10, 3, 5, 7, 12, 8, 11, 12, 11, 12, 9, 4, 3, 12, 9, 14, 9, 5, 6, 9, 5, 6, 8, 11, 6, 3, 14], [10, 10, 9, 6, 10, 3, 5, 5, 12, 3, 14, 10, 2, 10, 3, 6, 9, 5, 6, 10, 2, 10, 9, 4, 10, 9, 5, 6, 2, 9, 12, 10], [10, 2, 3, 12, 3, 13, 5, 4, 3, 12, 2, 3, 12, 3, 5, 5, 6, 1, 12, 3, 5, 6, 3, 12, 10, 3, 5, 5, 5, 6, 10, 10], [3, 5, 5, 7, 4, 3, 5, 5, 5, 7, 5, 5, 7, 5, 5, 5, 5, 5, 7, 5, 5, 5, 5, 6, 3, 5, 5, 5, 5, 5, 6, 2]])
