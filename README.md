# 'Mazing
Generating, visualising, playing around with mazes

<img align="right" src="/Gallery/maze_backtracker-32x32_anim_2023.07.29-06h57m21.gif" width=200 alt="A Mazing animation">

## What is this?
My first project to learn Git.

Mazes are fun, so I wrote up some code to build arbitrarily large ones--and nothing easier for a computer than to solve them, too!

I liked ASCII art visualize them, but PNG is nice too, especially to color stuff. (Along the way animated GIFs also found their way into this.)

In essence, the main `mazing.py` module provides a handy `Maze` class to work with.


## How is it used?
Run `playground.py` as main to directly try most stuff out!
(Making that nicely usable in console took some small effort, too.)

*Concerning direct usage:*
Google-style Docstrings should be added to everything in `mazing.py` (\*and others).
See code examples in section further below.


## What can it do?
Features of interest include but are not limited to:
- **Carving** random (so-called) 'perfect' mazes with unique solution.
    * Standard algorithms *(Growing tree, backtracker, (simplified) Prim's, Kruskal's, Wilson's, divide-and-conquer)*
    * Mix of different methods *('X'-divide-and-conquer)*
- **Text art.**
    * 7 different ways to print maze as text (3 with solution path)
- **Imaging.**
    * Normal PNG
    * Indicate solution path
    * Colored by distance from entrance (heatmap)
    * Colored by algorithm used (for mixed maze generation)
- **Animation.**
    * Use any of above imaging methods to visualize building of a maze
- **Computing information.**
    * Solution path
    * Longest possible path through maze and other stats


## Don't you have exams to write?
Graph algorithms are interesting, and ASCII art is cool, and, messing with mazes is tons of fun, and I, uh, kinda got lost learning about different color systems, Python decorators were kinda cool, and uh...


# Gallery

## Text Art
Mazes for the console!

### ASCII Art
- *ASCII 'frame'*
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
- *'Minimalist' ASCII frame*
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

### Unicode Art
*Note: Unfortunately it may happen that certain special characters don't display correctly (uneven character width);*
- *'Frame'* (box drawing characters)
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
- *'Half-block'*
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
- *'Quarter-block'*
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
- *'Pipes'*
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

## Images
*` TODO `*

## Animations
(Expand to see animations.)

<details><summary>Recursive Algorithm Mix Timelapse</summary>

<img align="left" src="/Gallery/maze_division-128x128_anim_2023.07.29-07h12m21.gif" width=256 alt="xdivision animation">

<img align="right" src="/Gallery/maze_division-128x128_algorithms_2023.07.29-07h13m35.png" width=256 alt="xdivision endresult">

</details>


# Helper Modules

While developing this project I had to come up with some functionality best factored out into different modules.

## `colortools`

To manipulate colors effectively I brewed my own color module.
Important for this project:
- Loads of useful color constants
- Color gradient presets (including standard ones for scientific heatmaps)
- Interpolation functions
- Conversion between more complex color systems (to generate perceptually uniform rainbows)

## `benchtools`

I used this project to learn a bit about decorators;
- `timed`
- `timed_titled` (for displaying lambdas with no name)


# Code Examples

<details><summary>Generate a simple maze and print it to console (Unicode & ASCII).</summary>

```py
from mazing import Maze

# Blank, new maze
my_maze = Maze(16,16)

# Randomize maze
my_maze.backtracker()

# Choose an Unicode string function
print(my_maze.str_frame())

# Choose an ASCII string function
print(my_maze.str_frame_ascii())
```

</details>

<details><summary>Generate a large maze and save a normal- and a solution image in current directory.</summary>

```py
from mazing import Maze

# Blank, new maze
my_maze = Maze(100,100)

# Randomize maze
my_maze.growing_tree()

# Generate normal image, then save it
img = my_maze.generate_image()
img.save(img1.filename)

# Generate solution image, then save it
imgsol = my_maze.generate_solutionimage()
imgsol.save(img1.filename)
```

</details>

<details><summary>Generate an animation of how a maze gets built.</summary>

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

<details><summary>Make very large, rosey maze as desktop wallpaper.</summary>

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

<details><summary>Generate a heterogeneous maze, then stepwise escalate image saving customization.</summary>

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
