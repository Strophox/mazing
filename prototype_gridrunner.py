# BEGIN OUTLINE
"""
Interactively navigating grids in console. TODO
"""
# END   OUTLINE


# BEGIN IMPORTS

import curses

# END   IMPORTS


# BEGIN CONSTANTS
# No constants
# END   CONSTANTS


# BEGIN DECORATORS
# No decorators
# END   DECORATORS


# BEGIN CLASSES
class Gridrunner:
    def __init__(self, grid):
        self._grid = grid
        self._user_coordinates = (1, 1) # TODO
        self._goal_coordinates = (-2, -2)
        self._entities = []
        self.won = None

    def run(self):
        #try:
            #stdscr = curses.initscr()
            #curses.cbreak()
            #curses.noecho()
            #stdscr.keypad(True)
            #curses.curs_set(False)
            #self._run(stdscr)
        #finally:
            #curses.nocbreak()
            #curses.echo()
            #stdscr.keypad(False)
            #curses.curs_set(True)
            #curses.endwin()
        curses.wrapper(self._run)
        return

    def _run(self, stdscr):
        # Curses initialization
        curses.curs_set(False) # Invisible cursor
        stdscr.timeout(100) # How long to wait for input before aborting
        #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Make palette
        #stdscr.bkgd(' ', curses.color_pair(1)) # Set palette for window

        # State initialization
        (CH, CW) = stdscr.getmaxyx() # Console Height, Width
        CH -= 1 # Don't wanna deal with bottom right corner
        grid = self._grid
        (gridH, gridW) = len(grid), len(grid[0])
        (screenH, screenW) = CH, CW//2
        (marginH, marginW) = screenH//3, screenW//3
        (goalx, goaly) = self._goal_coordinates

        # Helpers
        def wall_at(y, x):
            return grid[y][x] == 1

        # Store Initial
        (camx, camy) = (0, 0)
        (x, y) = self._user_coordinates

        # Main loop
        while True:
            # Store Update
            (o_x, o_y) = (x, y)

            # Get Update
            try:                 key = stdscr.getkey()
            except curses.error: key = ''
            if key == '\x1b': # Escape
                self.won = False
                break
            # Do computations
            moving = True
            keepmoving = key in "DWAS"
            while moving:
                moving = False
                if   (key in ['d','D','KEY_RIGHT'] and not wall_at(y,x+1)):
                    (y,x) = (y, x+1)
                    moving = keepmoving
                elif (key in ['w','W','KEY_UP']    and not wall_at(y-1,x)):
                    (y,x) = (y-1, x)
                    moving = keepmoving
                elif (key in ['a','A','KEY_LEFT']  and not wall_at(y,x-1)):
                    (y,x) = (y, x-1)
                    moving = keepmoving
                elif (key in ['s','S','KEY_DOWN']  and not wall_at(y+1,x)):
                    (y,x) = (y+1, x)
                    moving = keepmoving

            if x == (gridW-1) - 1 and y == (gridH-1):
                self.won = True
                break

            # Update camera position
            if x < camx+marginW and 0 < camx:
                camx -= 1
            elif camx+screenW-marginW < x and camx+screenW < gridW:
                camx += 1
            if y < camy+marginH and 0 < camy:
                camy -= 1
            elif camy+screenH-marginH < y and camy+screenH < gridH:
                camy += 1
            # Update screen
            to_str = lambda i: '▒▒' if i==1 else '  ' # ░▒▓█
            # Draw grid
            for i in range(min(screenH,gridH)):
                stdscr.addstr(i,0, ''.join(to_str(b) for b in grid[i+camy][camx:camx+screenW]))

            stdscr.addstr((o_y-camy),(o_x-camx)*2, '  ')
            stdscr.addstr((y-camy),(x-camx)*2, '██')
            #stdscr.addstr(0,0,f"{camx =} {camx+screenW-marginW =} {x =} {camx+screenW =} {CW =}")
        return
# END   CLASSES


# BEGIN FUNCTIONS
# No functions
# END   FUNCTIONS


# BEGIN MAIN

def main():
    from mazing import Maze, ALGORITHMS
    maze = Maze(32,32)
    maze.division(
        roomlength=float('inf'),
        nest_algorithms=[
            ALGORITHMS['clear'],
            ALGORITHMS['backtracker'],
            ALGORITHMS['division'],
        ],
    )
    maze.make_unicursal(probability=0.1)
    maze.node_at( 0, 0)._edges |= 0b0010 # Entrance top
    maze.node_at(-1,-1)._edges |= 0b1000 # Entrance bottom
    grid = maze.generate_raster(decolumnated=True)
    gridrunner = Gridrunner(grid)
    gridrunner.run()
    print("G.G." if gridrunner.won else "rip")
    return

if __name__=="__main__": main()

# END   MAIN
