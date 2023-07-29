# 'Mazing
Generating, visualising, playing around with mazes

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
Features of interest may include:
- Building random (so-called) 'perfect' mazes (guaranteed single solution)
    * Standard algorithms *(Growing tree, backtracker, (simplified) Prim's, Kruskal's, Wilson's, divide-and-conquer)*
    * Mix of different methods *('X' divide-and-conquer)*
    * (Also, make a maze unicursal <=> remove all dead ends)
- Computing information
    * Solution path
    * Longest possible path through maze
    * More, simple statistics (number of dead ends, length of branches, ...)
- Text art
    * 7 different ways to print maze as text (3 with solution path)
- Image generation
    * Normal PNG
    * Indicate solution path
    * Colored by distance from entrance (heatmap)
    * Colored by algorithm used (for mixed maze generation)
- Generation of animations
    * Use any of above imaging methods to visualize building of a maze


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
┌──────────────────────────────┐
│  ┌────────┐  ┌┐  ┌────┐  ┌┐  │
│  └───────┐│  └┘  └────┘  ││  │
└───────┐  │└───────────┐  ││  │
┌───────┘  │┌──────┐┌───┘  └┘  │
│  ┌───────┘│  ┌┐  ││  ┌┐  ┌───┘
│  └────────┘  ││  └┘  ││  └───┐
│  ┌────────┐  ││  ┌───┘│  ┌┐  │
│  └───┐┌───┘  ││  └───┐│  ││  │
└───┐  ││  ┌───┘│  ┌┐  ││  ││  │
┌───┘  ││  │┌───┘  ││  ││  ││  │
│  ┌┐  ││  ││  ┌───┘│  ││  ││  │
│  ││  ││  └┘  │┌───┘  ││  └┘  │
│  ││  ││  ┌┐  ││  ┌───┘└───┐  │
│  └┘  └┘  ││  └┘  └────────┘  │
└──────────┘└──────────────────┘
```

## Images
*` TODO `*

## Animations
*` TODO `*


# Helper Modules

While developing this project I had to come up with some functionality best factored out into different modules.

## `colortools`

To manipulate colors effectively I brewed my own color module.
Important for this project:
- Loads of useful color constants
- Color gradient presets
- Interpolation (mixing) functions
- Conversion between more complex color systems (to generate perceptually uniform rainbows)

## `benchtools`

I used this project to learn a bit about decorators;
- `timed`
- `timed_titled` (for displaying lambdas with no name)

# Code Examples
*` TODO `*
