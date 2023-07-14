
# OUTlINE BEGIN


# OUTINE END


# IMPORTS BEGIN

import random

# IMPORTS END


# CLASSES BEGIN

class Maze:
    """A class to store and interact with a maze grid."""

    # Direction Masks
    RIGHT,UP,LEFT,DOWN = 0b0001,0b0010,0b0100,0b1000

    def __init__(self, width_, height_):
        assert(width_ > 0 and height_ > 0)
        self.width = width_
        self.height = height_
        self.grid = [[random.randint(0,8) for _ in range(width_)] for _ in range(height_)]

    def __format__(self, *args):
        if args[0]=='':
            return self.ascii_compact()
        else:
            raise NotImplementedError # TODO

    def ascii_compact(self):
        """Produce a compact ASCII representation."""
        wall = lambda x,y,direction: not self.edge_toward((x,y),direction)
#,___, ,___, ,___, ,___,
#|   | | __| | | | | |_|
#|___| |___| |___| |___|
#,___, ,___, ,___, ,___,
#|__ | |___| |_| | |_|_|
#|___| |___| |___| |___|
#,___, ,___, ,___, ,___,
#| , | | ,_| | | | | |_|
#|_|_| |_|_| |_|_| |_|_|
#,___, ,___, ,___, ,___,
#|_, | |___| |_| | |_|_|
#|_|_| |_|_| |_|_| |_|_|
        string = f",{'_'*(2*self.width-1)}," # Top fence
        # Add to string row-wise
        for y,row in enumerate(self.grid):
            string += '\n|' # Left fence
            # Add two chars per node
            for x,node in enumerate(row):
                # Decide middle segment
                if y==self.height-1 or wall(x,y,self.DOWN):
                    string += '_'
                else:
                    string += ' '
                # Decide right segment
                if x==self.width-1 or wall(x,y,self.RIGHT):
                    string += '|'
                elif (y<self.height-1 and wall(x,y+1,self.RIGHT)
                      and not (wall(x,y,self.DOWN) and wall(x+1,y,self.DOWN))): # Wall below left and right
                    string += ','
                elif (y==self.height-1
                      or wall(x,y,self.DOWN) or wall(x+1,y,self.DOWN)):
                    string += '_'
                else:
                    string += ' '
        return string

    def edge_toward(self, node_coordinate, direction): # TODO bad idea?..
        """Check whether there is an edge from a specified node into some direction.
        - node_coordinate : (x,y) where 0<=x<width && 0<=y<height
        - direction : one of self.{RIGHT,UP,LEFT,DOWN}"""
        (x,y) = node_coordinate
        return self.grid[y][x] & direction


# CLASSES END


# FUNCTIONS BEGIN


# FUNCTIONS END


# MAIN BEGIN

def main():
    maze = Maze(10,10)
    print(f"{maze}")

if __name__=="__main__": main()

# MAIN END
