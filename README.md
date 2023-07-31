# 'Mazing
*Generating, visualising, playing around with mazes*

<img align="right" src="/Gallery/maze_backtracker-32x32_anim_2023.07.29-06h57m21.gif" width=200 alt="A Mazing animation" title="randomized-DFS carving">

## What is this?
A hobby project to familiarize myself with Git.

Mazes are fun, so I whipped up some code to build arbitrarily large ones – and nothing easier for a computer than to solve, print, draw and color them in, too!

In essence, [`mazing.py`](./mazing.py) provides a handy *`Maze`* class to play around with.


## How could I use it?
Run `playground.py` directly to try stuff out on the command line!
(I put some small effort into making this usable, too)

I tried adding [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings to everything, so `help()` should yield sensible information for usage of any script/module (c.f. code examples in last section).


## What can it do?
Functionality includes but is not limited to
- **Randomly carving** (so-called) 'perfect' mazes with a unique solution.
    * Common algorithms implemented [Growing tree, backtracker, (simplified) Prim's, Kruskal's, Wilson's, divide-and-conquer]
    * Mix of different methods ('x-divide-and-conquer')
- **Text art.**
    * 7 different ways to print maze as text (including 3 w/ solution path)
- **Imaging.**
    * Normal PNG
    * Solution path
    * Colored by distance from entrance (heatmap)
    * Colored by algorithm usage (for mixed maze generation)
- **Animation.**
    * Use any of above imaging methods to visualize building of a maze
- **Computing information.**
    * Solution path
    * Longest possible path through maze, and other interesting stats


## Don't you have exams to write?
Messing with mazes is tons of fun, and their [graph algorithms](http://www.jamisbuck.org/presentations/rubyconf2011/index.html) are interesting (lots of different ['flavors' of mazes](https://www.astrolog.org/labyrnth/algrithm.htm)), also [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) is cool, and, then I uh, kinda got lost learning about different [color spaces](https://bottosson.github.io/posts/oklab/) and what makes [good color gradients for scientific graphs](https://www.youtube.com/watch?v=o9KxYxROSgM) too, and, and [Python decorators](https://stackoverflow.com/questions/308999/what-does-functools-wraps-do) kept me occupied *(& did you know that [`yield from`](https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-yield-from-syntax-in-python-3-3) is a valid syntax struct in Python?)*, so anyway uh....


# Gallery

## Text Art

### ASCII
*Timeless maze art for any (any?) console!*

> ASCII 'frame'
```
+   +---+---+---+---+---+---+---+---+---+
|               |                       |
+   +---+   +   +---+---+---+   +---+   +
|   |   |   |       |           |       |
+   +   +   +---+   +   +---+---+   +---+
|       |   |           |               |
+   +---+   +   +---+---+---+---+---+   +
|   |       |   |   |           |   |   |
+   +   +---+   +   +   +---+   +   +   +
|   |       |       |   |       |   |   |
+   +---+   +---+---+   +   +---+   +   +
|   |   |           |   |           |   |
+   +   +---+---+   +   +---+---+---+   +
|   |       |       |               |   |
+   +   +   +   +---+---+---+---+   +   +
|   |   |   |   |           |       |   |
+   +   +   +   +   +   +   +   +---+   +
|   |   |   |       |   |   |   |   |   |
+   +---+   +---+---+   +---+   +   +   +
|                   |           |       |
+---+---+---+---+---+---+---+---+---+   +
```

> 'Minimalist' ASCII frame
```
, ______________________________,
| ,__ |___, |_, , , |___, |___, |
| | , , ,_| __| |_|_, | | __, | |
|_|_| | |__ __|__ | | , | , | , |
| |__ | |___, | ,_| __|___| |_| |
| ,___| | __|__ | | , | ____|_, |
| |__ |_| ________|_|_|___| __| |
| ____| ,_, __| , , |____ ,__ | |
|____ |_| | , |_| |__ , , |_____|
| |_, | ,___|_| |_| , |_|_| ____|
| ,_|__ | | ,__ | ,_|_| | |__ | |
| | | __, ,_| __|_| |_, , |__ , |
| , | , | |__ , |__ __| |__ , | |
| | ,_| |_| , | , __, ,_| __|_| |
| |_| |_| |_| | |_, | | |__ __|_|
| ,__ | , |___|_| |_| | , ,__ __|
|_|_____|___|_________|_|_|____ |
```

### Unicode
> *Note: Unfortunately it may happen that certain special characters don't display correctly (uneven character width)*

<details markdown=1><summary>Show Unicode arts</summary>

> 'Frame'
```
╷ ┌───────────┬─────────────┬───┐
│ ╵ ╷ ┌───┬─╴ └───╴ ╷ ┌─────┘ ╷ │
│ ╶─┼─┘ ╷ └───────┐ ├─┘ ╷ ╶─┬─┘ │
├─╴ │ ╶─┼─────┬─╴ │ │ ┌─┴─╴ │ ┌─┤
│ ╷ └─╴ ├─╴ ╶─┤ ╶─┴─┘ ├─┬───┘ │ │
│ ├─────┤ ┌─┐ └───┬───┘ │ ╶─┬─┘ │
│ │ ╶───┘ │ └───┐ │ ╶───┴─┐ │ ╶─┤
│ │ ╶─┬─┬─┴─╴ ┌─┘ │ ┌───┐ ╵ ├─╴ │
│ └─┐ │ │ ╷ ╶─┴─┬─┘ └─┐ └─┐ ╵ ╷ │
├─╴ │ ╵ │ └───┐ └───┐ ├─╴ └─┬─┘ │
│ ╷ │ ╷ │ ┌─╴ ├─┬─┬─┘ │ ┌───┤ ┌─┤
│ │ └─┤ │ ├─┐ ╵ │ │ ╶─┘ └─┐ ╵ │ │
│ ├─┐ ╵ ╵ │ │ ╶─┤ └───────┼─┬─┘ │
│ │ │ ┌─╴ │ ├─╴ │ ┌───╴ ╷ ╵ │ ╷ │
│ │ │ │ ┌─┘ │ ┌─┘ └─┐ ╶─┴─┬─┴─┘ │
│ ╵ │ └─┘ ┌─┘ └───╴ ├───╴ └─╴ ╷ │
└───┴─────┴─────────┴─────────┘ ╵
```

> 'Half-block'
```
█ ▀▀█▀▀▀▀▀▀▀█▀▀▀█▀▀▀█▀▀▀█▀▀▀▀▀▀▀█
█▀▀ ▀▀▀ █▀▀ ▀▀▀ █▀▀ ▀ ▀▀█▀▀ █▀▀ █
█▀▀▀▀ ▀▀█▀▀▀▀ ▀▀█▀▀ █▀▀▀█▀▀ █▀▀▀█
█▀▀ █▀▀ █▀▀ █ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀▀ █
█▀▀▀▀▀▀ █▀▀▀▀▀▀▀█ ▀▀█▀▀▀▀▀▀▀█▀▀▀█
█ ▀▀█ ▀▀█▀▀ █▀▀ █▀▀ ▀▀▀ █▀▀ ▀ ▀▀█
█▀▀ █▀▀▀▀▀▀ ▀▀▀▀█▀▀▀█ ▀▀█▀▀▀▀ ▀▀█
█ ▀▀▀▀▀ █▀▀ █ ▀▀█▀▀ ▀ ▀▀█▀▀ █▀▀ █
█▀▀▀▀▀▀▀▀ ▀▀█▀▀▀▀▀▀▀█▀▀▀█▀▀▀█▀▀▀█
█▀▀ █ ▀▀█ ▀▀▀ ▀▀█ ▀▀▀▀▀ ▀ ▀▀▀ ▀▀█
█▀▀ ▀▀▀▀█▀▀▀▀▀▀ █▀▀▀▀▀▀ █ ▀▀▀▀▀▀█
█▀▀ █ ▀▀█▀▀ █ ▀▀█▀▀ █▀▀ █▀▀ █▀▀ █
█▀▀ ▀▀▀▀█▀▀▀█▀▀▀█▀▀ █▀▀▀█▀▀▀█▀▀▀█
█▀▀ █ ▀▀█▀▀ ▀▀▀ █▀▀ ▀ ▀▀▀ ▀▀▀▀▀ █
█▀▀▀█ ▀▀▀▀▀ █▀▀▀█ ▀▀▀▀▀▀█▀▀▀█▀▀ █
█▀▀ ▀▀▀ █ ▀▀▀▀▀ █▀▀ █▀▀ █▀▀ ▀▀▀ █
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀
```

> 'Quarter-block'
```
▛▀▀▀▀▀▛▀▀▀▀▀▀▛▀▀▀▀▀▀▛▀▀▀▀▀▀▀▀▀▀▀▌
▌▘▌▀▀▘▌▀▘▀▌▛▘▌▌▘▛▀▘▌▘▛▘▛▀▘▌▀▌▀▘▘▌
▛▀▌▌▌▀▀▀▀▌▘▘▌▌▀▀▘▀▌▀▀▘▌▘▌▌▛▘▀▛▘▌▌
▌▌▘▌▀▀▌▀▘▀▘▀▘▛▘▛▘▌▛▘▛▀▛▘▘▌▘▀▘▘▀▘▌
▌▀▌▛▘▌▘▌▀▀▘▀▀▌▀▌▛▘▌▘▘▘▘▌▀▌▘▌▀▀▀▌▌
▌▘▘▌▌▀▘▌▘▛▘▌▌▀▘▘▌▘▀▌▛▘▛▘▌▀▛▀▘▌▘▘▌
▌▛▀▘▌▀▘▌▘▌▘▘▘▀▛▘▘▀▌▘▌▌▘▀▌▌▘▌▀▀▘▀▌
▌▘▛▀▀▀▛▘▀▛▘▌▀▘▘▀▌▘▀▛▘▛▀▘▘▛▀▀▌▘▌▘▌
▛▀▘▘▌▘▌▘▌▌▌▛▀▘▘▌▀▀▌▌▘▘▀▀▀▌▀▘▘▌▀▀▌
▌▀▀▌▀▌▀▛▘▘▌▘▌▀▀▀▘▌▘▌▀▀▀▘▌▀▘▌▀▀▀▌▌
▌▀▘▀▘▌▘▌▛▀▌▌▀▛▘▛▀▀▘▌▘▛▀▘▌▀▛▘▌▌▘▌▌
▛▀▌▛▘▌▀▘▘▘▘▌▌▘▌▘▘▛▘▀▀▌▀▛▀▌▌▀▌▌▀▘▌
▌▌▌▌▘▀▀▀▀▌▌▘▘▀▘▛▘▘▛▀▘▀▘▌▘▌▀▘▌▘▌▌▌
▌▌▌▌▀▘▌▘▘▘▀▘▀▌▀▌▌▘▌▛▀▌▀▌▘▌▀▘▌▀▘▘▌
▌▘▘▀▌▘▘▌▀▘▘▛▘▘▘▘▌▀▘▌▌▌▘▀▘▛▘▀▀▀▘▌▌
▌▀▀▘▘▀▀▀▀▘▀▘▘▘▀▀▘▌▀▘▌▘▌▀▘▌▘▀▀▀▘▘▌
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▘
```

> 'Pipes'
```
┌──────────┐┌──────────────┐┌──────────────────┐
│  ┌┐  ┌┐  ││  ┌────┐  ┌┐  ││  ┌┐  ┌┐  ┌┐  ┌┐  │
│  ││  ││  └┘  │┌───┘  ││  └┘  ││  ││  ││  ││  │
│  ││  ││  ┌┐  ││  ┌───┘│  ┌───┘│  ││  ││  ││  │
│  └┘  ││  ││  └┘  └────┘  │┌───┘  ││  └┘  └┘  │
│  ┌───┘│  ││  ┌┐  ┌───────┘│  ┌───┘└───┐  ┌───┘
│  │┌───┘  ││  └┘  │┌──────┐│  └───────┐│  └───┐
│  ││  ┌───┘└──────┘│  ┌┐  ││  ┌────┐  ││  ┌┐  │
│  └┘  │┌──────────┐│  ││  └┘  └────┘  ││  └┘  │
│  ┌───┘│  ┌┐  ┌┐  ││  ││  ┌────┐  ┌───┘│  ┌───┘
│  └───┐│  ││  ││  ││  ││  └────┘  └───┐│  └───┐
│  ┌┐  ││  ││  ││  ││  ││  ┌┐  ┌┐  ┌┐  ││  ┌┐  │
│  └┘  ││  └┘  └┘  └┘  ││  └┘  ││  ││  └┘  ││  │
│  ┌───┘└───┐  ┌────┐  ││  ┌───┘│  ││  ┌───┘│  │
│  │┌──────┐│  │┌───┘  ││  └───┐│  └┘  │┌───┘  │
│  ││  ┌┐  ││  ││  ┌───┘│  ┌┐  ││  ┌───┘│  ┌┐  │
│  ││  └┘  ││  └┘  │┌───┘  ││  └┘  └───┐│  ││  │
│  ││  ┌┐  ││  ┌┐  ││  ┌───┘│  ┌────┐  ││  ││  │
│  └┘  ││  ││  └┘  ││  │┌───┘  │┌───┘  ││  └┘  │
└───┐  ││  ││  ┌───┘│  ││  ┌┐  ││  ┌───┘│  ┌┐  │
┌───┘  └┘  ││  └───┐│  └┘  └┘  └┘  └────┘  ││  │
│  ┌────┐  │└───┐  ││  ┌┐  ┌┐  ┌┐  ┌┐  ┌───┘│  │
│  └────┘  └────┘  └┘  ││  └┘  └┘  ││  └────┘  │
└──────────────────────┘└──────────┘└──────────┘
```

</details>

## Images

### One Example

*This 20×20 maze was generated by a randomized-DFS carving method, which usually leads to long, winding tunnels compared to other methods.*

![Test Maze](Gallery/maze_backtracker-20x20_2023.07.29-09h11m07.png)

<details><summary>Solution of above maze</summary>

![Maze Solution](Gallery/maze_backtracker-20x20_solution_2023.07.29-09h11m32.png)

</details>

<details><summary>Distance heatmap of maze</summary>

![Maze Heatmap](Gallery/maze_backtracker-20x20_colormap_2023.07.29-09h11m42.png)

</details>

### Bigger maze samples

> Solution of a 128×128 randomized-Kruskal maze.
![Kruskal Solution](Gallery/maze_kruskal-128x128_solution_2023.07.29-09h00m07.png)

> 'Great Wave off Kanagawa'
![Kanagawa](Gallery/maze128x128_backtracker_dist_2023.07.26-08h27m14.png)

> 1920×1080 maze wallpaper variation ([see others here](Gallery/wallpapers))
![Wallpaper](Gallery/wallpapers/wallpaper_brewerBlue_maze_kruskal-1920x1080_colormap_2023.07.29-09h37m37.png)

> 'Magma' colormap.
![Magma](Gallery/maze1024x1024_TREE_dist_2023.07.24-03h16m55.png)

## Animations

### Comparing Algorithm Animations

<details><summary>Backtracker</summary>

![Backtracker Animation](Gallery/maze_backtracker-16x16_anim_2023.07.29-07h43m17.gif)

</details>


<details><summary>Growing-Tree</summary>

![Growing-Tree Animation](Gallery/maze_growing_tree-16x16_anim_2023.07.29-07h47m32.gif)

</details>


<details><summary>Prim</summary>

![Prim Animation](Gallery/maze_prim-16x16_anim_2023.07.29-07h46m14.gif)

</details>


<details><summary>Kruskal</summary>

![Kruskal Animation](Gallery/maze_kruskal-16x16_anim_2023.07.29-07h46m40.gif)

</details>


<details><summary>Divide and Conquer</summary>

![Divide and Conquer Animation](Gallery/maze_division-16x16_anim_2023.07.29-07h45m26.gif)

</details>

### Mixed Algorithm Timelapse

'x-divide-and-conquer' *(better name pending)* is a variation on normal divide-and-conquer where any recursive call may decide to let an arbitrary algorithm finish the remaining subsection.
This allows mazes to be correctly and seamlessly built using independent perfect maze algorithms.

<details><summary>Mixed Divide-and-Conquer</summary>

<div style="position:relative">

<img align="left" src="/Gallery/maze_division-100x100_anim_2023.07.31-00h43m20.gif" width=400 alt="xdivision animation">

<img align="center" src="/Gallery/maze_division-100x100_algorithms_2023.07.31-00h44m29.png" width=400 alt="xdivision endresult">

</div>

</details>


# Repository File Summaries

Each file (obviously) has some specific purpose;
- `mazing.py` - Main maze functionality (see [beginning](#what-is-this))
- `playground` - Sandbox functionality to try out `mazing`.
- `benchmark.py` - Personal mini-benchmark, not specifically intended for use.
- `colortools.py` - Homebrewn color module.
    * Common/useful color constants
    * Interpolation functions
    * Color gradient presets
    * Conversion between color spaces
- `benchtools.py` - Minimal timing decorators.
    * `timed` to time a function by its name
    * explicit `timed_titled` for lambdas
- `prototype_gridrunner.py` - Unfinished top-down maze navigator implemented using `curses`.
    I don't intend on continuing work on it.
    * Should correctly display and appropriately scroll large mazes.
    * Navigate the maze on-screen using **arrow keys** or **w**, **a**, **s**, **d**.
    * Use **shift** in combination with the latter to jump to next wall.


# Code Examples

<details><summary>Generate a simple maze and print it to console (Unicode & ASCII).</summary>

```py
from mazing import Maze

# Blank, new maze
my_maze = Maze(16,16)

# Randomize maze
my_maze.backtracker()

# Choose a Unicode string function
print(my_maze.str_frame())

# Choose an ASCII string function
print(my_maze.str_frame_ascii())
```

</details>

<details><summary>Generate a large maze and save a normal image and a solution.</summary>

```py
from mazing import Maze

# Blank, new maze
my_maze = Maze(100,100)

# Randomize maze
my_maze.growing_tree()

# Generate normal image, then save it
img = my_maze.generate_image()
img.save(img.filename)

# Generate solution image, then save it
imgsol = my_maze.generate_solutionimage()
imgsol.save(imgsol.filename)
```

</details>

<details><summary>Generate an animation of how `backtracker` works.</summary>

```py
from mazing import Maze

# Generate animation frames
(frames, my_unused_maze) = Maze.generate_animation(16,16, Maze.backtracker)

# Save frames as .gif
frames[0].save(
    frames[0].filename,
    save_all=True,
    append_images=frames[1:],
    duration=30,
)
```

</details>

<details><summary>Make a very large maze to be used as HD desktop wallpaper.</summary>

```py
from mazing import Maze
import colortools as ct

# Blank, new maze
my_maze = Maze(1920,1080) # (<!- Python be slow)

# Randomize maze
my_maze.backtracker()

# Precomputes distances
my_maze.compute_distances()

# Generate image
imgdst = my_maze.generate_colorimage(
    gradient_colors=ct.COLORMAPS['acton'][::-1], # makes bright -> dark
    raster=my_maze.generate_raster(
        wall_air_ratio=(0,1),
        show_distances=True
    )
)

# Save image
imgdst.save(imgdst.filename)
```

</details>

<details><summary>Generate an interesting maze, then slowly escalate customization when saving images.</summary>

```py
from mazing import Maze
import colortools as ct

my_maze = Maze(256,256)
my_maze.xdivision()

# 1) Solution image
imgsol = my_maze.generate_solutionimage()
imgsol.save(imgsol.filename)

# 2) Normal image, altered colors
img = my_maze.generate_image(
    wall_air_colors=(ct.COLORS['sepia'],ct.COLORS['pergament']),
)
img.save(img.filename)

# 3) Algorithms map, raster adapted
imgalg = my_maze.generate_algorithmimage(
    raster=my_maze.generate_raster(
        decolumnated=True,
        wall_air_ratio=(1,2),
        show_algorithms=True,
    ),
)
imgalg.save(imgalg.filename)

# 4) Branch distances, colors and raster adapted
my_maze.compute_branchdistances()
imgdst = my_maze.generate_colorimage(
    gradient_colors=ct.COLORMAPS['redyellowblue'][::-1], # makes bright -> dark
    raster=my_maze.generate_raster(
        decolumnated=True,
        wall_air_ratio=(1,2),
        show_distances=True,
    ),
)
imgdst.save(imgdst.filename)
```

</details>
