# OUTLINE BEGIN
"""
A small module to do handle colors.
"""
# OUTLINE END


# IMPORTS BEGIN
import random
# IMPORTS END


# CONSTANTS BEGIN

#TODO
# TODO
#  TODO
VIGOR = (53, 215, 187) #35D7BB
DISCORD_RED = (237, 66, 69) #ED4245
DISCORD_BLURPLE = (88, 101, 242) #5865F2
PERGAMENT = (239, 226, 207) #EFE2CF
SEPIA = (50, 45, 35) #322D23

# CONSTANTS END


# CLASSES BEGIN
# No classes
# CLASSES END


# FUNCTIONS BEGIN

def hex_to_tuple(hex_color):
    R = (0xFF0000 & hex_color) >> 16
    G = (0x00FF00 & hex_color) >>  8
    B = (0x0000FF & hex_color) >>  0
    tuple_color = (R,G,B)
    return tuple_color

"""
def tuple_to_hex(tuple_color):
    (R,G,B) = tuple_color
    hex_color = (R << 16) | (G << 8) | (B << 0)
    return hex_color
"""

def randrgb():
    """Generates an RGB tuple representing a random color."""
    color_random = tuple(random.randrange(256) for _ in range(3))
    return color_random

def randhue():
	"""Generates an RGB tuple representing a random hue at full saturation."""
	# Throw dice
	p = random.randrange(6)
	# Magic incantation
	val = lambda i:(1-(p%3-i)**2%3)*((1-p%2*2)*(random.randrange(255)-p%2*255))+((p%3-i)**2%3)*(255*(1-(i-2+(p-p%2)//2)**2%3))
	# Return tuple
	color_random = tuple(val(i) for i in range(3))
	return color_random

def invert(color):
    color_inverted = tuple(255-ch for ch in color)
    return color_inverted

def interpolate(color0, color1, param):
    color_mixed = tuple(int((1 - param)*ch0 + param*ch1) for (ch0,ch1) in zip(color0,color1))
    return color_mixed

def average(*colors):
    add = lambda c1,c2: tuple(ch1+ch2 for ch1,ch2 in zip(c1,c2))
    color_sum = (0,0,0)
    count = 0
    for color in colors:
        add(color_sum, color)
        count += 1
    color_average = tuple(int(color_sum/count) for ch in color_sum)
    return color_average

# FUNCTIONS END


# MAIN BEGIN
# No main
# MAIN END
