# BEGIN OUTLINE
"""
Interactively navigating grids in console.

NOTICE Unfinished.
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
    """Grid representation to store and navigate a grid."""
    def __init__(self, grid):
        self._grid = grid
        self._player_coordinates = (1, 1)
        self._goal_coordinates = (-2, -2)
        self._entities = []
        self._won = None

    @property
    def won(self):
        """Whether last round was 'won'."""
        return self._won

    def run(self):
        """Run the `curses` in-console grid navigator.

        Wraps the actual navigator with curses.wrapper so cleanup is done nicely
        """
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
        """Navigate the maze given a curses window `stdscr`.

        Navigate with wasd or arrow keys.
        Use WASD (wasd + shift) to long jump within grid.
        """
        # Curses initialization
        curses.curs_set(False) # Invisible cursor
        stdscr.timeout(100) # How long to wait for input before continuing
        #curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE) # Make palette
        #stdscr.bkgd(' ',curses.color_pair(1)) # Use palette

        # State initialization
        (CH, CW) = stdscr.getmaxyx() # Console Height, Width
        CH -= 1 # Don't wanna deal with bottom right corner curses 'bug'
        grid = self._grid
        (gridH, gridW) = len(grid), len(grid[0]) # Grid dimensions
        (screenH, screenW) = CH, CW//2 # Grid cells allowed on screen
        (marginH, marginW) = screenH//3, screenW//3 # Safe padding for player cam
        (goalx, goaly) = self._goal_coordinates # Finish tile

        # Helper functions
        def wall_at(y, x):
            return not(0<=y<gridH and 0<=x<gridW) or grid[y][x] == 1

        # Store Initial
        (camx, camy) = (0, 0) # Top left camera position
        (x, y) = self._player_coordinates # Player position

        # Main loop
        while True:
            # Get Update
            try:                 key = stdscr.getkey()
            except curses.error: key = ''
            if key == '\x1b': # Escape
                self._won = False
                break

            # Do computations
            longjmp = (key in "DWAS") # Jump to wall?
            while True:
                if   (key in ['d','D','KEY_RIGHT'] and not wall_at(y,x+1)):
                    (y,x) = (y, x+1)
                    if longjmp: continue
                elif (key in ['w','W','KEY_UP']    and not wall_at(y-1,x)):
                    (y,x) = (y-1, x)
                    if longjmp: continue
                elif (key in ['a','A','KEY_LEFT']  and not wall_at(y,x-1)):
                    (y,x) = (y, x-1)
                    if longjmp: continue
                elif (key in ['s','S','KEY_DOWN']  and not wall_at(y+1,x)):
                    (y,x) = (y+1, x)
                    if longjmp: continue
                break

            # Test for win condition
            if x >= gridW-1 or y >= gridH-1:
                self._won = True
                break

            # Update camera position
            if   x < camx+marginW         and 0 < camx:             camx -= 1
            elif camx+screenW-marginW < x and camx+screenW < gridW: camx += 1
            if   y < camy+marginH         and 0 < camy:             camy -= 1
            elif camy+screenH-marginH < y and camy+screenH < gridH: camy += 1

            # Update screen
            # Draw grid
            to_str = lambda i: '▒▒' if i==1 else '  ' # ░▒▓█
            for i in range(min(screenH,gridH)):
                stdscr.addstr(i,0, ''.join(to_str(b) for b in grid[i+camy][camx:camx+screenW]))
            # Draw player
            if 0<=y-camy<screenH and 0<=x-camx<screenW:
                stdscr.addstr((y-camy),(x-camx)*2, '██')
            # Draw debug
            #stdscr.addstr(0,0,f"{x,y =} {camx,camy =}")
        return

# END   CLASSES


# BEGIN FUNCTIONS
# No functions
# END   FUNCTIONS


# BEGIN MAIN

def main():
    # Make maze grid
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
    #maze.clear() # Debug
    maze.make_braided(probability=0.1) # Make easier for player
    maze.node_at( 0, 0)._edges |= 0b0010 # Hack top entrance
    maze.node_at(-1,-1)._edges |= 0b1000 # Hack bottom exit
    grid = maze.generate_raster(decolumnated=True)
    # Make and run main grid navigator
    gridrunner = Gridrunner(grid)
    gridrunner.run()
    # End of game
    print("G.G. W.P." if gridrunner.won else "F")
    return

if __name__=="__main__": main()

# END   MAIN
