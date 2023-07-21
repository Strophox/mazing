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

def convert(color, type1, type2):
    """
    Converts between tuples of a color in one of the following representations:
        Red-Green-Blue : 'RGB', <[0,255],[0,255],[0,255]>
        Hue-Value-Saturation : 'HSV', <[0,360],[0.,1.],[0.,1.]>
        CIELAB color model : 'LAB', <???>
    """
    source = type1.upper()
    destination = type2.upper()
    if source=='RGB':
        if destination=='HSV':
            R,G,B = color
            M = max(R,G,B)
            m = min(R,G,B)
            C = M - m
            H1 =           0  if C==0 else \
                 (G-B)/C % 6  if M==R else \
                 (B-R)/C + 2  if M==G else \
                 (R-G)/C + 4  if M==B else None
            H = int(H1 * 60)
            V = M
            S = C/V if V!=0 else 0
            return (H,S,V)
        elif destination=='LAB':
            R,G,B = color
            X = R*0.49    + G*0.31    + B*0.20
            Y = R*0.17697 + G*0.81240 + B*0.01063
            Z = R*0.00    + G*0.01    + B*0.99
            X1,Y1,Z1 = 95.0489, 100, 108.8840 # Standard Illuminant D65
            delta = 6/29
            f = lambda t: t**(1/3) if t>delta**3 else t/(3*delta**2)+4/29
            L = 116*f(Y/Y1) - 16
            A = 500*(f(X/X1) - f(Y/Y1))
            B = 200*(f(Y/Y1) - f(Z/Z1))
            return (L,A,B)
    elif source=='HSV':
        if destination=='RGB':
            H,S,V = color
            C = V * S
            H1 = H // 60
            X = C * (1 - abs(H1%2 - 1))
            (R1,G1,B1) = (C,X,0)  if 0 <= H1 < 1 else \
                         (X,C,0)  if 1 <= H1 < 2 else \
                         (0,C,X)  if 2 <= H1 < 3 else \
                         (0,X,C)  if 3 <= H1 < 4 else \
                         (X,0,C)  if 4 <= H1 < 5 else \
                         (C,0,X)  if 5 <= H1 < 6 else None
            R = R1 + m
            G = G1 + m
            B = B1 + m
            return (R,G,B)
        elif destination=='LAB':
            return convert(convert(color, 'HSV','RGB'), 'RGB','LAB')
    elif source=='LAB':
        if destination=='RGB':
            L,A,B = color
            X1,Y1,Z1 = 95.0489, 100, 108.8840 # Standard Illuminant D65
            delta = 6/29
            f_inv = lambda t: t**3 if t>delta else (t-4/29)(3*delta**2)
            X = X1*f_inv((L+16)/116 + A/500)
            Y = Y1*f_inv((L+16)/116)
            Z = Z1*f_inv((L+16)/116 - B/200)
            R =  X*2.36461385 - Y*0.89654057 - Z*0.46807328
            G = -X*0.51516621 + Y*1.4264081  + Z*0.0887581
            B =  X*0.0052037  - Y*0.01440816 + Z*1.00920446
            return (R,G,B)
        elif destination=='HSV':
            return convert(convert(color, 'LAB','RGB'), 'RGB','HSV')

# FUNCTIONS END


# MAIN BEGIN
# No main
# MAIN END
