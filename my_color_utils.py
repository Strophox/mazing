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
def hex_to_tuple(hex_col):
    R = (0xFF0000 & hex_col) >> 16
    G = (0x00FF00 & hex_col) >>  8
    B = (0x0000FF & hex_col) >>  0
    return (R,G,B)

def randrgb():
    """Generates an RGB tuple representing a random color."""
    return tuple(random.randrange(256) for _ in range(3))


def randhue():
	"""Generates an RGB tuple representing a random hue at full saturation."""
	# Throw dice
	p = random.randrange(6)
	# Magic incantation
	val = lambda i:(1-(p%3-i)**2%3)*((1-p%2*2)*(random.randrange(255)-p%2*255))+((p%3-i)**2%3)*(255*(1-(i-2+(p-p%2)//2)**2%3))
	# Return tuple
	color = tuple(val(i) for i in range(3))
	return color

def interpolate(color0, color1, parameter):
    color = tuple((1 - parameter)*c0 + parameter*c1 for (c0,c1) in zip(color0,color1))
    return color
# FUNCTIONS END


# MAIN BEGIN
# No main
# MAIN END
