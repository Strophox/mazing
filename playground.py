# BEGIN OUTLINE
"""
A script to interactively play with functionality from `maze.py`.

Intended to be run as main.

Help menu shown upon execution:
~:--------------------------------------:~
           A Mazing Playground
~:--------------------------------------:~
 Enter a command to achieve its effect:
 ;  help   - show this menu
 Maze Generation
 ;  build  - make new maze
 :  dim    - set dimensions for next build
 :  load   - load maze from temp.txt
 :  store  - store maze to  temp.txt
 Modification
 :  maxim  - find & set longest path
 :  goal   - manually set entrance & exit
 :  unicrs - unicursal = remove dead ends
 Console View
 ;  print  - text art of maze
 :  txtsol - text art, solutions
 :  stats  - ~statistics of maze
 Imaging
 ;  img    - png image
 ;  imgsol - png solution image
 :  imgdst - png distance map
 :  imgbrc - branch dist. of spann. tree
 :  imgalg - alg's used (for `xdivision`)
 :  color  - set color map
 :  ratio  - set ratio of wall:air size
 :  view   - view latest image
 :  save   - save latest image
 Animation
 ;  anim   - open animation helper
 (Commands are autocompleted if possible)
 Enter blank command to quit
~:--------------------------------------:~

"""
# END   OUTLINE


# BEGIN IMPORTS

import colortools
from shutil     import get_terminal_size
from benchtools import timed, timed_titled
from maze       import Maze, ALGORITHMS

# END   IMPORTS


# BEGIN CONSTANTS

CANCEL_TEXT = "*canceled\n" # When cancling out of a menu
CELL_PRINT_LIMIT = 10_000 # Max cell count before maze gets stopped from printing
CW = lambda: get_terminal_size()[0] # Console Width
CH = lambda: get_terminal_size()[1] # Console Height

# END   CONSTANTS


# BEGIN DECORATORS
# No decorators
# END   DECORATORS


# BEGIN CLASSES
# No classes
# END   CLASSES


# BEGIN FUNCTIONS

def dedent(text, indent_unit=1):
    """Remove common indent from multiline string.

    Args:
        text (str): Text to unindent.
        indent_unit: units of whitespace in which to unindent.

    Returns:
        str
    """
    lines = text.split('\n')
    indent = min(len(line) - len(line.lstrip()) for line in lines if line)
    indent -= indent % indent_unit
    if indent:
        dedented_text = '\n'.join(line[indent:] for line in lines)
    else:
        dedented_text = text
    return dedented_text

def dedent4_concat_strip(*texts):
    """Merge together strings; used for ASCII menus.

    Steps executed are:
        1. Remove trailing newlines from input texts.
        2. Dedent input texts in space units of 4.
        3. Join together texts with newlines.

    Args:
        *texts (iter(str)): Strings to glue.

    Returns:
        str: Glued strings.
    """
    string = '\n'.join(
        proc for text in texts
        if (proc:=dedent(text, indent_unit=4).strip('\n'))
    )
    return string

def autocomplete(input_word, full_words):
    """Autocomplete word iff there's a unique word completion from list.

    Args:
        input_word (str): String to be completed.
        full_words (list(str)): Available strings to possibly be completed to.

    Returns:
        str: A unique match from full_words, otherwise input_word.
    """
    candidates = [w for w in full_words if w.startswith(input_word)]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return input_word

def preview(maze, printer=Maze.str_frame):
    """Print maze to the console if it is within given global print limit.

    Args:
        maze (Maze): Maze to be printed to console.
        printer (callable(Maze)): Function to print maze with.
    """
    cellcount = maze.width*maze.height
    if maze.width*maze.height >= CELL_PRINT_LIMIT:
        print(f"[for console preview too large ({cellcount} cells), consider image options]")
        return None
    print(printer(maze))
    return

def maybe_get_new_from_string_options(options, prompt_text):
    """Helper: user selects one of several string options, return None else.

    Args:
        options (list(str)): List of string options to return choice from.
        prompt_text: Appropriate string prompt for the user.

    Returns:
        str or None
    """
    user_input = input(f"| {' | '.join(options)}\n{prompt_text} > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    option = autocomplete(user_input,options)
    if option not in options:
        print(f"[unrecognized option '{option}']")
        return None
    if option != user_input:
        print(f"-> {option}")
    return option

def maybe_get_new_dimensions(old_dimensions):
    """Helper: Get two integers ('dimensions') from user, return None else.

    Args:
        old_dimensions (tuple(int,int)): Previous dimensions for context.

    Returns:
        tuple(int,int) or None
    """
    user_input = input(f"Enter sidelength (e.g. '32') or full dimensions (e.g. '80 40') (previously = {old_dimensions[0]} {old_dimensions[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) not in {1,2}:
            raise ValueError("invalid number of arguments")
        new_dimensions = (nums[0], nums[0]) if len(nums)==1 else (nums[0], nums[1])
    except ValueError as e:
        print(f"[error: {e}]")
        return None
    return new_dimensions

def maybe_set_new_entrance_exit(maze):
    """Helper: Let user set maze entrance and exit coordinates.

    Args:
        maze (Maze): Maze to be mutated.
    """
    user_input = input(f"Enter entrance & exit coordinates (default = '0 0 -1 -1', previously = {maze.entrance.coordinates[0]} {maze.entrance.coordinates[1]} {maze.exit.coordinates[0]} {maze.exit.coordinates[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) != 4:
            raise ValueError("invalid number of arguments")
        maze.set_entrance(nums[0], nums[1])
        maze.set_exit(nums[2], nums[3])
    except ValueError as e:
        print(f"[error: {e}]")
        return None
    return

def maybe_load_new_maze():
    """Helper: Get maze from user maze `repr` string, return None else.

    Returns:
        Maze or None
    """
    user_input = input("Enter `repr` string of a maze > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        data = eval(user_input)
        new_maze = timed_titled("loading maze", Maze.from_repr)(data)
        preview(new_maze)
    except Exception as e:
        print(f"[could not load maze: {e}]")
        return None
    return new_maze

def maybe_print_maze(maze):
    """Helper: Print maze if it satisfies conditions (`CELL_PRINT_LIMIT`).

    Args:
        maze (Maze): Maze to be printed.
    """
    cellcount = maze.width * maze.height
    if cellcount >= CELL_PRINT_LIMIT and not input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
        print(CANCEL_TEXT,end='')
        return None
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
    return

def maybe_get_new_ratio(old_ratio):
    """Helper: Get two integers ('ratio') from user, return None else.

    Args:
        old_ratio (tuple(int,int)): Previous ratio for context.

    Returns:
        tuple(int,int) or None
    """
    user_input = input(f"Enter wall:air ratio (default = 1 1, previously = {old_ratio[0]} {old_ratio[1]}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        nums = [int(s) for s in user_input.split()]
        if len(nums) != 2:
            raise ValueError("invalid number of arguments")
        else:
            new_ratio = (nums[0], nums[1])
    except ValueError as e:
        print(f"[error: {e}]")
        return None
    return new_ratio

def maybe_print_solution(maze):
    """Helper: Print solution if it satisfies conditions (`CELL_PRINT_LIMIT`).

    Args:
        maze (Maze): Maze whose solution is to be printed.
    """
    timed(maze.compute_solution)()
    cellcount = maze.width * maze.height
    if cellcount >= CELL_PRINT_LIMIT and not input(f"Maze contains a lot of cells ({cellcount}), proceed anyway ('Y')? >")=='Y':
        print(CANCEL_TEXT,end='')
        return None
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
    """Helper: Get an integer ('only') from user, return None else.

    Args:
        old_only (int): Previous 'only' for context.

    Returns:
        int or None
    """
    user_input = input(f"Enter number 'n' such that only every n-th frame is recorded during building process (e.g. '3' saves only third the frames) (default = 1, previously = {old_only}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        new_only = int(user_input)
    except ValueError as e:
        print(f"[error: {e}]")
        return None
    return new_only

def maybe_get_new_ms(old_ms):
    """Helper: Get an integer ('ms') from user, return None else.

    Args:
        old_ms (ms): Previous ms for context.

    Returns:
        int or None
    """
    user_input = input(f"Enter number of milliseconds per animation frame (e.g. '17' ~ 60fps) (default = 30, previously = {old_ms}) > ").strip()
    if not user_input:
        print(CANCEL_TEXT,end='')
        return None
    try:
        new_ms = int(user_input)
    except ValueError as e:
        print(f"[error: {e}]")
        return None
    return new_ms

def animation_helper():
    """Run console routine to assist in the creation of maze animations.

    Returns:
        Maze: Latest maze animated.
    """
    maze = None # Different maze we can return later
    dimensions = (32, 32)
    ratio = (1, 1)
    colormap_name = 'viridis'
    only = 1
    ms  = 30
    builder_name = 'backtracker'
    image_generator_name = 'img'
    image_generators = { #### color,ratio
        'img': (lambda maze:
            maze.generate_image(
                raster=maze.generate_raster(
                    wall_air_ratio=ratio
                )
            )
        ),
        'imgsol': (lambda maze:
            maze.compute_solution()
            and()or maze.generate_solutionimage(
                raster=maze.generate_raster(
                    show_solution=True,
                    wall_air_ratio=ratio
                )
            )
        ),
        'imgdst': (lambda maze:
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
        'imgbrc': (lambda maze:
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
        'imgalg': (lambda maze:
            maze.generate_algorithmimage(
                raster=maze.generate_raster(
                    show_algorithms=True,
                    wall_air_ratio=ratio
                )
            )
        ),
    }
    helper_text = lambda: dedent4_concat_strip(
        f"""
        ~:--------------------------------------:~
                    Animation Helper
        ~:--------------------------------------:~
         Change values or begin recording anim.:
         :  start  - begin rendering process
         Available settings
         :  build  - choose building method
         ;    = '{builder_name}'
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
        """
    )
    options = { # To autocomplete
        l[1] for line in helper_text().splitlines()
        if (l:=line.split()) and l[0] == ":"
    }
    options_menu_text = f"Change settings or start animation with `start` > "
    option = 'help'
    while True:
        match option:
            case 'build':
                new_builder_name =  maybe_get_new_from_string_options(
                    ALGORITHMS,
                    "Choose algorithm to build maze")
                if new_builder_name is not None:
                    builder_name = new_builder_name
            case 'imging':
                new_image_generator_name =  maybe_get_new_from_string_options(
                    image_generators,
                    "Choose imaging technique to make animation")
                if new_image_generator_name is not None:
                    image_generator_name = new_image_generator_name
            case 'color':
                new_colormap_name = maybe_get_new_from_string_options(
                    colortools.COLORMAPS,
                    f"Choose colormap (previously = {colormap_name})")
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
            case 'start':
                (filename, maze) = timed(Maze.save_animation)(
                    *dimensions,
                    maze_runner=(lambda maze, record_frame:
                        ALGORITHMS[builder_name](maze, record_frame=record_frame)
                    ),
                    image_generator=timed(image_generators[image_generator_name]),
                    frame_only=only,
                    frame_ms=ms,
                    alert_progress_steps=10,
                )
                print(f"Animation was saved under {filename}")
            case _:
                print("Unrecognized option")
        print(helper_text())
        user_input = input(options_menu_text).strip()
        if not user_input:
            print("Exiting Animation Helper")
            break
        option = autocomplete(user_input.lower(), options)
        if option != user_input:
            print(f"-> {option}")
    return maze

def analysis(maze):
    """Helper: Produce string presenting statistical analysis of current maze.

    Args:
        maze (Maze): Maze to be analysed.

    Returns:
        str: Presentation of statistics for the console etc.
    """
    # This function is a huge mess
    _maze_entrance_exit = (maze.entrance, maze.exit) # So we can restore state
    # Statistics helper
    def chart_sample(pos_int_sample, bars=10):
        """Take a list of positive integer data points and group them."""
        all_datapoints = len(pos_int_sample)
        if not all_datapoints:
            return (0, 0, [])
        # Make a probability distribution
        distribution = [
            pos_int_sample.count(x)
            for x in range(int(max(pos_int_sample))+1)
        ]
        distr_lower = 0
        while not distribution[distr_lower]:
            distr_lower += 1
        # Attempt 1. Take all values
        # Attempt 2. Go through all points and stop at 95%
        # Attempt 3. Binary search (failed, omitted)
        # Attempt 4. Exponential decay
        distr_upper = 1
        integ = lambda n: sum(distribution[distr_lower:round(n)])
        while (coverage := integ(distr_upper)) < 0.95 * all_datapoints:
            distr_upper *= 1.5
        distr_upper = min(len(distribution)-1, round(distr_upper))
        # Make chart values to be displayed
        barwidth = ((distr_upper - distr_lower) // bars) or 1
        chart = [
            (x, x+barwidth, sum(distribution[x:x+barwidth]))
            for x in range(distr_lower, distr_upper, barwidth)
        ]
        return (all_datapoints, coverage, chart)
    # Formatter helpers
    fmt_perc  = lambda perc: f"{perc:.2%}"
    fmt_float = lambda float_: f"{float_:.01f}"
    def fmt_stats(sample):
        """Calculate standard statistics of data set and format them as string."""
        if not sample:
            return dedent4_concat_strip(
                f"""
                 : -- No valid data to calculate statistics.
                """,
            )
        expectation = lambda smple: not smple or (
            sum(smple)/len(smple))
        variance    = lambda smple: not smple or (
            sum(x**2 for x in smple)/len(smple)- (sum(smple)/len(smple))**2)
        evaluations = {
            "Expectation":
                expectation(sample),
            "Deviation":
                variance(sample)**.5,
            "Maximum":
                max(sample),
        }
        CWtitle = max(len(title) for title in evaluations.keys())
        CWstat  = max(len(fmt_float(stat)) for stat in evaluations.values())
        string = dedent4_concat_strip(
            *(f"""
             :    {title.ljust(CWtitle)}  {fmt_float(stat).rjust(CWstat)}
            """ for (title,stat) in evaluations.items()),
        )
        return string
    def fmt_barchart(chart):
        """Take a normalized distribution and turn contents into bar chart str."""
        if not chart:
            return dedent4_concat_strip(
                f"""
                 :    -- No valid data for bar chart.
                """,
            )
        CWs = [0 for _ in chart[0]]
        for row in chart:
            CWs = [max(a,len(b)) for a,b in zip(CWs,row[:-1])]
        CWs_concat = sum(c+2 for c in CWs) - 2
        CWbar = (CW()-2-4-CWs_concat-1-0-2) * 4 // 5
        hbar = lambda fill_level: '%' * round(fill_level*CWbar)
        table = dedent4_concat_strip(
            f"""
             :    {CWs_concat*' '}  +{(CWbar)*'-'}+
            """,
            *(f"""
             :    {
                 ''.join(f"{val.ljust(CW_)}  " for CW_,val in zip(CWs,row[:-1]))
            }|{hbar(row[-1]).ljust(CWbar)}|
            """ for row in chart),
            f"""
             :    {CWs_concat*' '}  +{(CWbar)*'-'}+
            """,
        )
        return table
    # Solution Stats Data
    node_count = maze.width * maze.height
    if maze.solution is None:
        timed(maze.compute_solution)()
    sol_len = len(maze.solution)
    (
        tiles_counts,
        branch_dist_list,
        offsh_maxlen_list,
    ) = timed_titled("computing stats+", maze.generate_stats)()
    (
        offsh_maxlen_listcount,
        offsh_maxlen_listcovg,
        offsh_maxlen_chart_data
    ) = timed_titled("chart 2", chart_sample)(offsh_maxlen_list)
    offsh_maxlen_chart = [
        (
            f"[{x},{xp})",
            fmt_perc(points / offsh_maxlen_listcount),
            points / offsh_maxlen_listcount,
        ) for (x,xp,points) in offsh_maxlen_chart_data
    ]
    # Solution Stats Text
    stats_solution = dedent4_concat_strip(
        f"""
         Solution Path Statistics.
         :  Start, End coordinates   {maze.entrance.coordinates}, {maze.exit.coordinates}
         :  Path length of solution  {sol_len} = {fmt_perc(sol_len/node_count)} of area
         :  Offshoot paths on sol.   {len(offsh_maxlen_list)}
         :
         :  Offshoot paths maximum distance:
         :  (showing {offsh_maxlen_listcovg} / {offsh_maxlen_listcount} datapoints, {fmt_perc(1 - offsh_maxlen_listcovg/offsh_maxlen_listcount)} not shown)
        """,
        fmt_barchart(offsh_maxlen_chart),
        fmt_stats(offsh_maxlen_list),
    )
    # General Stats Data
    alg_shares = timed(maze.generate_algorithm_shares)()
    alg_chart = sorted([
        (
            fmt_perc(alg_node_count / node_count),
            f"{alg_name}",
            alg_node_count / node_count,
        ) for alg_name,alg_node_count in alg_shares.items()
        if alg_node_count
    ],key=lambda t:t[1])
    node_connectivities = [
        ("dead ends",     [0b0001,0b0010,0b0100,0b1000]),
        ("tunnels",       [0b0011,0b0101,0b0110,0b1001,0b1010,0b1100]),
        ("three-ways",    [0b0111,0b1011,0b1101,0b1110]),
        ("intersections", [0b1111]),
    ]
    node_conn_chart = [
        (
            f"{f_u_python}",
            f"{name}",
            fmt_perc(f_u_python / node_count),
            f_u_python / node_count,
        ) for (name, tile_selection) in node_connectivities
        if (f_u_python:=sum(tiles_counts[t] for t in tile_selection))and()or 1
    ]
    # General Stats Text
    stats_general = dedent4_concat_strip(
        f"""
         General Information.
         :   Width x Height      {maze.width} x {maze.height}
         :   Area / Total Nodes  {node_count}
         :
         :  Algorithms used:
        """,
        fmt_barchart(alg_chart),
        f"""
         :  Node connectivities:
        """,
        fmt_barchart(node_conn_chart),
     )
    # Solution Branching Stats Data
    (
        branch_dist_listcount,
        branch_dist_listcovg,
        branch_dist_chart_data
    ) = timed_titled("chart 1", chart_sample)(branch_dist_list)
    longpath_len = timed(maze.compute_longest_path)()
    branch_dist_sum = sum(branch_dist_list)
    branch_dist_chart = [
        (
            f"[{x},{xp})",
            fmt_perc(points / branch_dist_listcount),
            points / branch_dist_listcount,
        ) for (x,xp,points) in branch_dist_chart_data
    ]
    # Distance Stats
    stats_distance = dedent4_concat_strip(
        f"""
         Distance Statistics.
         :  Longest path       {longpath_len} = {fmt_perc(longpath_len/node_count)} of area
         :  Nodes in branches  {branch_dist_sum} = {fmt_perc(branch_dist_sum/node_count)} of area
         :
         :  Distance from dead end to nearest three-way/intersection:
         :  (showing {branch_dist_listcovg} / {branch_dist_listcount} datapoints, {fmt_perc(1 - branch_dist_listcovg/branch_dist_listcount)} not shown)
        """,
        fmt_barchart(branch_dist_chart),
        fmt_stats(branch_dist_list),
    )
    # Final print
    hrulefill = f"\n~:{'-'*(CW()-4)}:~\n"
    statistics = dedent4_concat_strip(
        hrulefill,
            stats_general,
        hrulefill,
            stats_distance,
        hrulefill,
            stats_solution,
        hrulefill,
    )
    # Restore modified state
    (maze.entrance, maze.exit) = _maze_entrance_exit
    return statistics

# END   FUNCTIONS


# BEGIN MAIN

def main():
    # Sandkasten
    dimensions = (16,16)
    ratio = (1, 1)
    maze = Maze(*dimensions)
    maze.backtracker()
    colormap_name = 'viridis'
    image = None
    maze_storage_file = 'maze_store.dat'
    main_text = dedent4_concat_strip(
    """
        ~:--------------------------------------:~
                   A Mazing Playground
        ~:--------------------------------------:~
         Enter blank command to quit.
         Commands are autocompleted if possible.
         Available commands:
         ;  help   - show this menu
         Mazebuilding
         ;  build  - make new maze
         :  store  - store maze to  temp.txt
         :  load   - load maze from temp.txt
         :  unicrs - 'unicursal' = no dead ends
         Maze Settings
         :  dim    - set dimensions for next build
         :  goal   - set new entrance & exit
         :  maxim  - find & set longest path
         Viewing in Console
         ;  print  - text art of maze
         :  solve  - solution ascii art
         :  stats  - ~statistics of maze
         Viewing as Image
         ;  img    - maze image
         ;  imgsol - maze solution image
         :  imgdst - maze path distance heatmap
         :  imgalg - alg. map (`build` -> `xdiv`)
         :  imgbrc - branch dist. of spann. tree
         :  view   - view latest image
         Image Settings
         :  color  - change colors
         :  ratio  - change pxl ratio of wall:air
         :  save   - save latest image
         Animation
         ;  anim   - open animation helper
        ~:--------------------------------------:~
        """,
    )
    commands = {
        l[1]:sentinel==';' for line in main_text.splitlines()
        if (l:=line.split()) and (sentinel:=l[0]) in ":;"}
    commands_menu_text = f"\n| {' | '.join(cmd for cmd,sel_flag in commands.items() if sel_flag)} > "
    command = 'help'
    while True:
        match command:
            # Open Animation Helper menu
            case 'anim':
                new_maze = animation_helper()
                if new_maze is not None:
                    maze = new_maze
            # Choose method + build new maze
            case 'build':
                new_builder_name = maybe_get_new_from_string_options(
                    ALGORITHMS,
                    "Choose algorithm to build maze")
                if new_builder_name is not None:
                    maze = Maze(*dimensions)
                    timed(ALGORITHMS[new_builder_name])(maze)
                    preview(maze)
            # Change color palette for image generation
            case 'color':
                new_colormap_name = maybe_get_new_from_string_options(
                    colortools.COLORMAPS,
                    f"Choose colormap (previously = {colormap_name})")
                if new_colormap_name is not None:
                    colormap_name = new_colormap_name
            # Set new maze building size
            case 'dim':
                new_dimensions = maybe_get_new_dimensions(dimensions)
                if new_dimensions is not None:
                    dimensions = new_dimensions
            # Set new maze entrance & exit
            case 'goal':
                maybe_set_new_entrance_exit(maze)
            # Show help menu
            case 'help':
                print(main_text)
            # :hehe:
            case 'hackerman':
                injection = []
                while user_input:=input(">>> "): injection.append(user_input)
                try: exec('\n'.join(injection))
                except Exception as e: print(f"<error: {e}>")
            case 'img': # Generate image of maze and open externally
                image = timed(maze.generate_image)(
                    raster=maze.generate_raster(
                        wall_air_ratio=ratio
                    )
                )
                image.show()
            # Generate image of maze colored by algorithm used
            case 'imgalg':
                image = timed(maze.generate_algorithmimage)(
                    raster=maze.generate_raster(
                        show_algorithms=True,
                        columnated=False,
                        wall_air_ratio=ratio
                    )
                )
                image.show()
            # Generate image of maze colored by length of tree branch
            case 'imgbrc':
                timed(maze.compute_branchdistances)()
                image = timed(maze.generate_colorimage)(
                    gradient_colors=colortools.COLORMAPS[colormap_name][::-1],
                    raster=maze.generate_raster(
                        show_distances=True,
                        columnated=True,
                        wall_air_ratio=ratio
                    )
                )
                image.show()
            # Generate image of maze colored by distances
            case 'imgdst':
                timed(maze.compute_distances)()
                image = timed(maze.generate_colorimage)(
                    gradient_colors=colortools.COLORMAPS[colormap_name][::-1],
                    raster=maze.generate_raster(
                        show_distances=True,
                        columnated=False,
                        wall_air_ratio=ratio
                    )
                )
                image.show()
            # Generate image of current maze with solution
            case 'imgsol':
                timed(maze.compute_solution)()
                image = timed(maze.generate_solutionimage)(
                    raster=maze.generate_raster(
                        show_solution=True,
                        wall_air_ratio=ratio
                    )
                )
                image.show()
            # Manually load maze from input string
            #case 'input':
                #new_maze = maybe_load_new_maze()
                #if new_maze is not None:
                    #maze = new_maze
            # Make maze unicursal
            case 'unicrs':
                timed(maze.make_unicursal)()
                preview(maze)
            # Load maze from temporary storage file
            case 'load':
                try:
                    with open(maze_storage_file,'r') as file:
                        string = timed_titled("reading file", file.read)()
                    data = timed_titled("evaluating string", eval)(string)
                    maze = timed_titled("loading maze", Maze.from_repr)(data)
                    #with open(maze_storage_file,'rb') as file:
                        #maze = pickle.load(file)
                    preview(maze)
                except Exception as e:
                    print(f"[could not load maze: {e}]")
            # Find and set longest path in maze as goal
            case 'maxim':
                len_longest_path = timed(maze.compute_longest_path)()
                print(f"Longest path of length {len_longest_path} (of {maze.width*maze.height} total cells) found.")
            # Print maze in all available text art styles
            case 'print':
                maybe_print_maze(maze)
            # Set new wall-to-air ratio for image generation
            case 'ratio':
                new_ratio = maybe_get_new_ratio(ratio)
                if new_ratio is not None:
                    ratio = new_ratio
            # Save last generated image as png
            case 'save':
                if image is None:
                    print("Please generate at least one image first (-> `help`)")
                else:
                    timed_titled(f"saving {image.filename}", image.save)(
                        image.filename
                    )
            # Show solution using text art
            case 'solve':
                maybe_print_solution(maze)
            # Generate and show statistics on the maze
            case 'stats':
                stats_text = timed_titled("total time for maze analysis", analysis)(maze)
                print(stats_text)
            # Store maze to temporary storage file
            case 'store':
                with open(maze_storage_file,'w') as file:
                    data = timed_titled("generating string", repr)(maze)
                    timed_titled("storing file", file.write)(data)
                #with open(maze_storage_file,'wb') as file:
                    #pickle.dump(maze, file, pickle.HIGHEST_PROTOCOL)
            # Re-open last image shown for preview
            case 'view':
                if image is None:
                    print("Please generate at least one image first (-> `help`)")
                else:
                    timed_titled(f"opening {image.filename}", image.show)()
            # billion dollar mistake
            case _:
                print("Unrecognized command")
        # Get new user input and check if user wants to exit
        user_input = input(commands_menu_text).strip()
        if not user_input:
            print("goodbye")
            break
        # We autocomplete unambiguous user input for 'ergonomics'
        command = autocomplete(user_input.lower(), commands)
        if command != user_input:
            print(f"-> {command}")
    return

if __name__=="__main__": main()

# END   MAIN
