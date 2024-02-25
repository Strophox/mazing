# BEGIN OUTLINE
"""
A handrolled color utilities module.
2024-02-18T05:29:04+0000

This module attempts to provide useful color definitions and utility functions
to allow for further (basic) handling of colors. Some color names were inspired
by Jan Misali (www.seximal.net/colors).
    - Greyscale colors
        * `BLACK` `DARK_GRAY` `GRAY` `LIGHT_GRAY` `WHITE`
    - Pure RGB colors
        * `RGB_RED` `RGB_YELLOW` `RGB_GREEN` `RGB_CYAN` `RGB_BLUE` `RGB_MAGENTA`
    - Primary colors
        * `RED`     `YELLOW`     `GREEN`     `CYAN`     `BLUE`     `MAGENTA`
    - Secondary colors
        * `ORANGE`  `LIME`       `TURQUOISE` `AZURE`    `VIOLET`   `ROSE`
    - Dark primary colors
        * `CRIMSON` `GOLDENROD`  `MOSS`      `TEAL`     `NAVY`     `PURPLE`
    - Light primary colors
        * `SALMON`  `VANILLA`    `MINT`      `SKY`      `PERIWINKLE`PINK`
    - Miscellaneous colors dictionary
        * `COLORS`
    - Color palettes dictionary
        * `PALETTES`
    - Color gradients dictionary
        * COLORMAPS`
    - Color spaces available for usage and conversion
         * `RGB` `HSV`
         * `LINRGB` `XYZ`
         * `CIELUV` `LCH_UV`
         * `CIELAB` `LCH_AB`
         * `OKLAB`  `OKLCH`
    - Color conversion functions
        * from_hexcode, to_hexcode, convert_format
    - Random color generation functions
        * randrgb, randhue
    - Color utility functions
        * mix, interpolate, average, rainbow_color, rainbow_palette
"""
# END   OUTLINE


# BEGIN IMPORTS

import math
import random

# END   IMPORTS


# BEGIN CONSTANTS

# Greyscales
BLACK      = (  0,   0,   0) # '#000000'
DARK_GRAY  = ( 63,  63,  63) # '#3f3f3f'
GRAY       = (127, 127, 127) # '#7f7f7f'
LIGHT_GRAY = (191, 191, 191) # '#bfbfbf'
WHITE      = (255, 255, 255) # '#ffffff'

# Pure RGB
RGB_RED    = (255,   0,   0) # '#ff0000'
RGB_YELLOW = (255, 255,   0) # '#ffff00'
RGB_GREEN  = (  0, 255,   0) # '#00ff00'
RGB_CYAN   = (  0, 255, 255) # '#00ffff'
RGB_BLUE   = (  0,   0, 255) # '#0000ff'
RGB_MAGENTA= (255,   0, 255) # '#ff00ff'

# Primary and secondary colors
RED        = (255,  51,  68) # '#ff3344'
ORANGE     = (255, 153,   0) # '#ff9900'
YELLOW     = (255, 238,   0) # '#FFEE00'
LIME       = (187, 238,   0) # '#bbee00'
GREEN      = ( 51, 221,  51) # '#33dd33'
TURQUOISE  = (  0, 238, 170) # '#00eeaa'
CYAN       = ( 17, 238, 238) # '#11eeee'
AZURE      = ( 68, 187, 255) # '#44bbff'
BLUE       = ( 68, 102, 255) # '#4466ff'
VIOLET     = (204,  51, 255) # '#cc33ff'
MAGENTA    = (255, 102, 238) # '#ff55ee'
ROSE       = (255,  85, 170) # '#ff55aa'

# Primary shades
CRIMSON    = (170,  34,  68) # '#aa2244'
GOLDENROD  = (204, 153,   0) # '#cc9900'
MOSS       = (  0, 153,  68) # '#009944'
TEAL       = (  0, 153, 170) # '#0099aa'
NAVY       = ( 17,  17, 153) # '#111199'
PURPLE     = (119,   0, 136) # '#770088'

# Primary tints
SALMON     = (255, 170, 153) # '#ffaa99'
VANILLA    = (255, 255, 221) # '#ffffdd'
MINT       = (187, 255, 187) # '#bbffbb'
SKY        = (187, 255, 255) # '#bbffff'
PERIWINKLE = (187, 204, 255) # '#bbccff'
PINK       = (255, 170, 221) # '#ffaadd'

COLORS = {
    'dark':
        ( 42,  42,  46), # '#2a2a2e'
    'error':
        (176,   0,  32), # '#b00020'
    'symbiogenesis':
        (116, 127, 141), # '#747f8d'
    'geodesic':
        (110, 109, 117), # '#6e6d75'
    'metalrobe':
        ( 74,  78,  91), # '#4a4e5b'
    'rayzngray':
        ( 88,  94, 108), # '#585e6c'
    'rayznblack':
        ( 26,  28,  32), # '#1a1c20'
    'viper':
        (157, 248,  86), # '#9df856'
    'greener':
        ( 47, 229,  80), # '#2fe550'
    'phosphophyllite':
        ( 53, 215, 187), # '#35d7bb'
    'crystal':
        ( 59, 205, 249), # '#3bcdf9'
    'royalpurple':
        (131,  56, 249), # '#8338f9'
    'octahedral':
        (109, 189, 221), # '#6dbddd'
    'tomato':
        (245,  68,  79), # '#f5444f'
    'rosey':
        (243, 102, 144), # '#f36690'
    'pastel_rose':
        (233, 123, 123), # "#E97B7B"
    'dark_rose':
        (108,  57,  79), # "#6C394F"
    'temptation':
        (216, 133, 165), # '#d885a5'
    'wastes':
        (157, 200, 110), # '#9dc86e'
    'industrialcomplex':
        (154, 203, 184), # '#9acbb8'
    'grainsofgravel':
        ( 92, 116, 156), # '#5c749c'
    'lightgold':
        (255, 192, 107), # '#ffc06b'
    'cloudscape':
        (161, 159, 244), # '#a19ff4'
    'dusk':
        (176, 159, 244), # '#b09ff4'
    'pastel_blue':
        (114, 148, 185), # "#7294B9"
    'pastel_ocean':
        (148, 196, 193), # "#94C4C1"
    'pastel_orange':
        (246, 164,  93), # "#F6A45D"
    'pastel_gray':
        (238, 238, 238), # "#EEEEEE"
    'classicblurple':
        (114, 137, 218), # '#7289da'
    'discordblurple':
        ( 88, 101, 242), # '#5865F2'
    'discordred':
        (237,  66,  69), # '#ED4245'
    'discordgray':
        (117, 126, 138), # '#757e8a'
    'ETH_Blue':
        ( 33,  92, 175), # '#215CAF'
    'ETH_Petrol':
        (  0, 120, 148), # '#007894'
    'ETH_Green':
        ( 98, 115,  19), # '#627313'
    'ETH_Bronze':
        (142, 103,  19), # '#8E6713'
    'ETH_Red':
        (183,  53,  45), # '#B6352D'
    'ETH_Purple':
        (167,  17, 122), # '#A7117A'
    'ETH_Grey':
        (111, 111, 111), # '#6F6F6F'
    'vellum':
        (239, 226, 207), # '#EFE2CF'
    'sepia':
        ( 50,  45,  35), # '#322D23'
    'earth':
        ( 75,  68,  58), # "#4B443A"
    'clardigfug':
        (112, 113,  84), # '#707154'
}
"""list(tuple(int,int,int)): Miscellaneous colors."""

PALETTES = {
    'discord': {
    'black':
        ( 30,  31,  34), # '#1e1f22'
    'low':
        ( 43,  45,  49), # '#2b2d31'
    'mid':
        ( 49,  51,  56), # '#313338'
    'high':
        ( 63,  66,  72), # '#3f4248'
    'detail':
        (148, 155, 164), # '#949ba4'
    'white':
        (219, 222, 225), # '#dbdee1'
    },
    'element': {
    'black':
        ( 44,  43,  42), # '#2c2b2a'
    'low':
        ( 68,  65,  59), # '#44413b'
    'mid':
        ( 82,  78,  71), # '#524e47'
    'high':
        (116, 112, 103), # '#747067'
    'detail':
        (158, 155, 149), # '#9e9b95'
    },
    'white':
        (255, 255, 255), # '#ffffff'
}
"""dict(str, dict(str, tuple(int,int,int)): Color palettes."""

COLORMAPS = {
    'kanagawa': [ # 2 values
        (  0,  63, 127), # '#003f7f'
        (247, 241, 231), # '#f7f1e7'
    ],
    'redyellowblue': [ # 15 values
        ( 16,  25,  77), # '#10194D'
        ( 22,  55, 113), # '#163771'
        ( 28,  87, 150), # '#1C5796'
        ( 57, 122, 168), # '#397AA8'
        ( 87, 158, 185), # '#579EB9'
        (137, 192, 196), # '#89C0C4'
        (188, 226, 207), # '#BCE2CF'
        (255, 255, 224), # '#FFFFE0'
        (250, 212, 172), # '#FAD4AC'
        (240, 168, 130), # '#F0A882'
        (228, 121,  97), # '#E47961'
        (198,  81,  84), # '#C65154'
        (165,  39,  71), # '#A52747'
        (117,  18,  50), # '#751232'
        ( 74,   0,  30), # '#4A001E'
    ],
    'viridis': [ # 18 values
        ( 68,   1,  84), # '#440154'
        ( 72,  23, 105), # '#481769'
        ( 71,  42, 122), # '#472a7a'
        ( 67,  61, 132), # '#433d84'
        ( 61,  78, 138), # '#3d4e8a'
        ( 53,  94, 141), # '#355e8d'
        ( 46, 109, 142), # '#2e6d8e'
        ( 41, 123, 142), # '#297b8e'
        ( 35, 137, 142), # '#23898e'
        ( 31, 151, 139), # '#1f978b'
        ( 33, 165, 133), # '#21a585'
        ( 46, 179, 124), # '#2eb37c'
        ( 70, 192, 111), # '#46c06f'
        (101, 203,  94), # '#65cb5e'
        (137, 213,  72), # '#89d548'
        (176, 221,  47), # '#b0dd2f'
        (216, 226,  25), # '#d8e219'
        (253, 231,  37), # '#fde725'
    ],
    'magma': [ # 16 values
        (  0,   0,   5), # '#000005'
        ( 11,   8,  28), # '#0B081C'
        ( 23,  11,  57), # '#170B39'
        ( 45,   0,  94), # '#2D005E'
        ( 67,   0, 106), # '#43006A'
        ( 93,  11, 110), # '#5D0B6E'
        (122,  21, 110), # '#7A156E'
        (148,  27, 106), # '#941B6A'
        (181,  37,  98), # '#B52562'
        (209,  48,  86), # '#D13056'
        (235,  72,  75), # '#EB484B'
        (246, 107,  77), # '#F66B4D'
        (251, 139,  89), # '#FB8B59'
        (252, 179, 114), # '#FCB372'
        (252, 213, 141), # '#FCD58D'
        (251, 255, 178), # '#FBFFB2'
    ],
    'brewerBlue': [ # 9 values
        (  8,  48, 107), # '#08306B'
        (  8,  81, 156), # '#08519C'
        ( 33, 113, 181), # '#2171B5'
        ( 66, 146, 198), # '#4292C6'
        (107, 174, 214), # '#6BAED6'
        (158, 202, 225), # '#9ECAE1'
        (198, 219, 239), # '#C6DBEF'
        (222, 235, 247), # '#DEEBF7'
        (247, 251, 255), # '#F7FBFF'
    ],
    'brewerGreen': [ # 9 values
        (  0,  69,  41), # '#004529'
        (  0, 104,  55), # '#006837'
        ( 35, 132,  67), # '#238443'
        ( 65, 171,  93), # '#41ab5d'
        (120, 198, 121), # '#78c679'
        (173, 221, 142), # '#addd8e'
        (217, 240, 163), # '#d9f0a3'
        (247, 252, 185), # '#f7fcb9'
        (255, 255, 229), # '#ffffe5'
    ],
    'brewerRed': [ # 9 values
        ( 73,   0, 106), # '#49006a'
        (122,   1, 119), # '#7a0177'
        (174,   1, 126), # '#ae017e'
        (221,  52, 151), # '#dd3497'
        (247, 104, 161), # '#f768a1'
        (250, 159, 181), # '#fa9fb5'
        (252, 197, 192), # '#fcc5c0'
        (253, 224, 221), # '#fde0dd'
        (255, 247, 243), # '#fff7f3'
    ],
    'chromaBlue': [ # 11 values
        (  0,  66, 157), # '#00429d'
        ( 40,  84, 166), # '#2854a6'
        ( 62, 103, 174), # '#3e67ae'
        ( 80, 123, 183), # '#507bb7'
        ( 97, 143, 191), # '#618fbf'
        (115, 162, 198), # '#73a2c6'
        (133, 183, 206), # '#85b7ce'
        (154, 203, 213), # '#9acbd5'
        (177, 223, 219), # '#b1dfdb'
        (205, 241, 224), # '#cdf1e0'
        (255, 255, 224), # '#ffffe0'
    ],
    'bamako': [ # 10 values
        (  0,  64,  77), # '#00404D'
        ( 19,  75,  66), # '#134B42'
        ( 38,  87,  55), # '#265737'
        ( 58, 101,  42), # '#3A652A'
        ( 82, 116,  28), # '#52741C'
        (113, 134,  11), # '#71860B'
        (149, 145,   6), # '#959106'
        (196, 173,  50), # '#C4AD32'
        (230, 204, 104), # '#E6CC68'
        (254, 228, 152), # '#FEE498'
    ],
    'acton': [ # 10 values
        ( 46,  33,  77), # '#2E214D'
        ( 75,  59, 102), # '#4B3B66'
        (110,  84, 128), # '#6E5480'
        (145,  99, 143), # '#91638F'
        (177, 103, 148), # '#B16794'
        (208, 123, 164), # '#D07BA4'
        (211, 148, 183), # '#D394B7'
        (211, 172, 200), # '#D3ACC8'
        (218, 200, 219), # '#DAC8DB'
        (229, 229, 239), # '#E5E5EF'
    ],
    'helixClassic': [ # 16 values
        (  0,   0,   1), # '#000001'
        ( 22,  10,  34), # '#160A22'
        ( 24,  32,  68), # '#182044'
        ( 16,  62,  83), # '#103E53'
        ( 14,  94,  74), # '#0E5E4A'
        ( 35, 116,  51), # '#237433'
        ( 80, 125,  35), # '#507D23'
        (138, 122,  45), # '#8A7A2D'
        (190, 117,  85), # '#BE7555'
        (218, 121, 145), # '#DA7991'
        (219, 138, 203), # '#DB8ACB'
        (204, 167, 240), # '#CCA7F0'
        (191, 201, 251), # '#BFC9FB'
        (195, 229, 244), # '#C3E5F4'
        (220, 246, 239), # '#DCF6EF'
        (255, 255, 255), # '#FFFFFF'
    ],
    'helix2': [ # 16 values
        (  0,   1,   0), # '#000100'
        (  0,  28,  14), # '#001C0E'
        (  0,  28,  14), # '#001C0E'
        (  7,  65,  91), # '#07415B'
        ( 35,  71, 135), # '#234787'
        ( 78,  72, 168), # '#4E48A8'
        (129,  72, 184), # '#8148B8'
        (177,  77, 181), # '#B14DB5'
        (214,  90, 165), # '#D65AA5'
        (235, 113, 143), # '#EB718F'
        (238, 142, 128), # '#EE8E80'
        (230, 175, 127), # '#E6AF7F'
        (219, 206, 144), # '#DBCE90'
        (216, 231, 178), # '#D8E7B2'
        (226, 247, 219), # '#E2F7DB'
        (255, 255, 255), # '#FFFFFF'
    ],
    'HQviridis': [ # 256 values
        ( 68,   1,  84), # '#440154'
        ( 68,   2,  86), # '#440256'
        ( 69,   4,  87), # '#450457'
        ( 69,   5,  89), # '#450559'
        ( 70,   7,  90), # '#46075a'
        ( 70,   8,  92), # '#46085c'
        ( 70,  10,  93), # '#460a5d'
        ( 70,  11,  94), # '#460b5e'
        ( 71,  13,  96), # '#470d60'
        ( 71,  14,  97), # '#470e61'
        ( 71,  16,  99), # '#471063'
        ( 71,  17, 100), # '#471164'
        ( 71,  19, 101), # '#471365'
        ( 72,  20, 103), # '#481467'
        ( 72,  22, 104), # '#481668'
        ( 72,  23, 105), # '#481769'
        ( 72,  24, 106), # '#48186a'
        ( 72,  26, 108), # '#481a6c'
        ( 72,  27, 109), # '#481b6d'
        ( 72,  28, 110), # '#481c6e'
        ( 72,  29, 111), # '#481d6f'
        ( 72,  31, 112), # '#481f70'
        ( 72,  32, 113), # '#482071'
        ( 72,  33, 115), # '#482173'
        ( 72,  35, 116), # '#482374'
        ( 72,  36, 117), # '#482475'
        ( 72,  37, 118), # '#482576'
        ( 72,  38, 119), # '#482677'
        ( 72,  40, 120), # '#482878'
        ( 72,  41, 121), # '#482979'
        ( 71,  42, 122), # '#472a7a'
        ( 71,  44, 122), # '#472c7a'
        ( 71,  45, 123), # '#472d7b'
        ( 71,  46, 124), # '#472e7c'
        ( 71,  47, 125), # '#472f7d'
        ( 70,  48, 126), # '#46307e'
        ( 70,  50, 126), # '#46327e'
        ( 70,  51, 127), # '#46337f'
        ( 70,  52, 128), # '#463480'
        ( 69,  53, 129), # '#453581'
        ( 69,  55, 129), # '#453781'
        ( 69,  56, 130), # '#453882'
        ( 68,  57, 131), # '#443983'
        ( 68,  58, 131), # '#443a83'
        ( 68,  59, 132), # '#443b84'
        ( 67,  61, 132), # '#433d84'
        ( 67,  62, 133), # '#433e85'
        ( 66,  63, 133), # '#423f85'
        ( 66,  64, 134), # '#424086'
        ( 66,  65, 134), # '#424186'
        ( 65,  66, 135), # '#414287'
        ( 65,  68, 135), # '#414487'
        ( 64,  69, 136), # '#404588'
        ( 64,  70, 136), # '#404688'
        ( 63,  71, 136), # '#3f4788'
        ( 63,  72, 137), # '#3f4889'
        ( 62,  73, 137), # '#3e4989'
        ( 62,  74, 137), # '#3e4a89'
        ( 62,  76, 138), # '#3e4c8a'
        ( 61,  77, 138), # '#3d4d8a'
        ( 61,  78, 138), # '#3d4e8a'
        ( 60,  79, 138), # '#3c4f8a'
        ( 60,  80, 139), # '#3c508b'
        ( 59,  81, 139), # '#3b518b'
        ( 59,  82, 139), # '#3b528b'
        ( 58,  83, 139), # '#3a538b'
        ( 58,  84, 140), # '#3a548c'
        ( 57,  85, 140), # '#39558c'
        ( 57,  86, 140), # '#39568c'
        ( 56,  88, 140), # '#38588c'
        ( 56,  89, 140), # '#38598c'
        ( 55,  90, 140), # '#375a8c'
        ( 55,  91, 141), # '#375b8d'
        ( 54,  92, 141), # '#365c8d'
        ( 54,  93, 141), # '#365d8d'
        ( 53,  94, 141), # '#355e8d'
        ( 53,  95, 141), # '#355f8d'
        ( 52,  96, 141), # '#34608d'
        ( 52,  97, 141), # '#34618d'
        ( 51,  98, 141), # '#33628d'
        ( 51,  99, 141), # '#33638d'
        ( 50, 100, 142), # '#32648e'
        ( 50, 101, 142), # '#32658e'
        ( 49, 102, 142), # '#31668e'
        ( 49, 103, 142), # '#31678e'
        ( 49, 104, 142), # '#31688e'
        ( 48, 105, 142), # '#30698e'
        ( 48, 106, 142), # '#306a8e'
        ( 47, 107, 142), # '#2f6b8e'
        ( 47, 108, 142), # '#2f6c8e'
        ( 46, 109, 142), # '#2e6d8e'
        ( 46, 110, 142), # '#2e6e8e'
        ( 46, 111, 142), # '#2e6f8e'
        ( 45, 112, 142), # '#2d708e'
        ( 45, 113, 142), # '#2d718e'
        ( 44, 113, 142), # '#2c718e'
        ( 44, 114, 142), # '#2c728e'
        ( 44, 115, 142), # '#2c738e'
        ( 43, 116, 142), # '#2b748e'
        ( 43, 117, 142), # '#2b758e'
        ( 42, 118, 142), # '#2a768e'
        ( 42, 119, 142), # '#2a778e'
        ( 42, 120, 142), # '#2a788e'
        ( 41, 121, 142), # '#29798e'
        ( 41, 122, 142), # '#297a8e'
        ( 41, 123, 142), # '#297b8e'
        ( 40, 124, 142), # '#287c8e'
        ( 40, 125, 142), # '#287d8e'
        ( 39, 126, 142), # '#277e8e'
        ( 39, 127, 142), # '#277f8e'
        ( 39, 128, 142), # '#27808e'
        ( 38, 129, 142), # '#26818e'
        ( 38, 130, 142), # '#26828e'
        ( 38, 130, 142), # '#26828e'
        ( 37, 131, 142), # '#25838e'
        ( 37, 132, 142), # '#25848e'
        ( 37, 133, 142), # '#25858e'
        ( 36, 134, 142), # '#24868e'
        ( 36, 135, 142), # '#24878e'
        ( 35, 136, 142), # '#23888e'
        ( 35, 137, 142), # '#23898e'
        ( 35, 138, 141), # '#238a8d'
        ( 34, 139, 141), # '#228b8d'
        ( 34, 140, 141), # '#228c8d'
        ( 34, 141, 141), # '#228d8d'
        ( 33, 142, 141), # '#218e8d'
        ( 33, 143, 141), # '#218f8d'
        ( 33, 144, 141), # '#21908d'
        ( 33, 145, 140), # '#21918c'
        ( 32, 146, 140), # '#20928c'
        ( 32, 146, 140), # '#20928c'
        ( 32, 147, 140), # '#20938c'
        ( 31, 148, 140), # '#1f948c'
        ( 31, 149, 139), # '#1f958b'
        ( 31, 150, 139), # '#1f968b'
        ( 31, 151, 139), # '#1f978b'
        ( 31, 152, 139), # '#1f988b'
        ( 31, 153, 138), # '#1f998a'
        ( 31, 154, 138), # '#1f9a8a'
        ( 30, 155, 138), # '#1e9b8a'
        ( 30, 156, 137), # '#1e9c89'
        ( 30, 157, 137), # '#1e9d89'
        ( 31, 158, 137), # '#1f9e89'
        ( 31, 159, 136), # '#1f9f88'
        ( 31, 160, 136), # '#1fa088'
        ( 31, 161, 136), # '#1fa188'
        ( 31, 161, 135), # '#1fa187'
        ( 31, 162, 135), # '#1fa287'
        ( 32, 163, 134), # '#20a386'
        ( 32, 164, 134), # '#20a486'
        ( 33, 165, 133), # '#21a585'
        ( 33, 166, 133), # '#21a685'
        ( 34, 167, 133), # '#22a785'
        ( 34, 168, 132), # '#22a884'
        ( 35, 169, 131), # '#23a983'
        ( 36, 170, 131), # '#24aa83'
        ( 37, 171, 130), # '#25ab82'
        ( 37, 172, 130), # '#25ac82'
        ( 38, 173, 129), # '#26ad81'
        ( 39, 173, 129), # '#27ad81'
        ( 40, 174, 128), # '#28ae80'
        ( 41, 175, 127), # '#29af7f'
        ( 42, 176, 127), # '#2ab07f'
        ( 44, 177, 126), # '#2cb17e'
        ( 45, 178, 125), # '#2db27d'
        ( 46, 179, 124), # '#2eb37c'
        ( 47, 180, 124), # '#2fb47c'
        ( 49, 181, 123), # '#31b57b'
        ( 50, 182, 122), # '#32b67a'
        ( 52, 182, 121), # '#34b679'
        ( 53, 183, 121), # '#35b779'
        ( 55, 184, 120), # '#37b878'
        ( 56, 185, 119), # '#38b977'
        ( 58, 186, 118), # '#3aba76'
        ( 59, 187, 117), # '#3bbb75'
        ( 61, 188, 116), # '#3dbc74'
        ( 63, 188, 115), # '#3fbc73'
        ( 64, 189, 114), # '#40bd72'
        ( 66, 190, 113), # '#42be71'
        ( 68, 191, 112), # '#44bf70'
        ( 70, 192, 111), # '#46c06f'
        ( 72, 193, 110), # '#48c16e'
        ( 74, 193, 109), # '#4ac16d'
        ( 76, 194, 108), # '#4cc26c'
        ( 78, 195, 107), # '#4ec36b'
        ( 80, 196, 106), # '#50c46a'
        ( 82, 197, 105), # '#52c569'
        ( 84, 197, 104), # '#54c568'
        ( 86, 198, 103), # '#56c667'
        ( 88, 199, 101), # '#58c765'
        ( 90, 200, 100), # '#5ac864'
        ( 92, 200,  99), # '#5cc863'
        ( 94, 201,  98), # '#5ec962'
        ( 96, 202,  96), # '#60ca60'
        ( 99, 203,  95), # '#63cb5f'
        (101, 203,  94), # '#65cb5e'
        (103, 204,  92), # '#67cc5c'
        (105, 205,  91), # '#69cd5b'
        (108, 205,  90), # '#6ccd5a'
        (110, 206,  88), # '#6ece58'
        (112, 207,  87), # '#70cf57'
        (115, 208,  86), # '#73d056'
        (117, 208,  84), # '#75d054'
        (119, 209,  83), # '#77d153'
        (122, 209,  81), # '#7ad151'
        (124, 210,  80), # '#7cd250'
        (127, 211,  78), # '#7fd34e'
        (129, 211,  77), # '#81d34d'
        (132, 212,  75), # '#84d44b'
        (134, 213,  73), # '#86d549'
        (137, 213,  72), # '#89d548'
        (139, 214,  70), # '#8bd646'
        (142, 214,  69), # '#8ed645'
        (144, 215,  67), # '#90d743'
        (147, 215,  65), # '#93d741'
        (149, 216,  64), # '#95d840'
        (152, 216,  62), # '#98d83e'
        (155, 217,  60), # '#9bd93c'
        (157, 217,  59), # '#9dd93b'
        (160, 218,  57), # '#a0da39'
        (162, 218,  55), # '#a2da37'
        (165, 219,  54), # '#a5db36'
        (168, 219,  52), # '#a8db34'
        (170, 220,  50), # '#aadc32'
        (173, 220,  48), # '#addc30'
        (176, 221,  47), # '#b0dd2f'
        (178, 221,  45), # '#b2dd2d'
        (181, 222,  43), # '#b5de2b'
        (184, 222,  41), # '#b8de29'
        (186, 222,  40), # '#bade28'
        (189, 223,  38), # '#bddf26'
        (192, 223,  37), # '#c0df25'
        (194, 223,  35), # '#c2df23'
        (197, 224,  33), # '#c5e021'
        (200, 224,  32), # '#c8e020'
        (202, 225,  31), # '#cae11f'
        (205, 225,  29), # '#cde11d'
        (208, 225,  28), # '#d0e11c'
        (210, 226,  27), # '#d2e21b'
        (213, 226,  26), # '#d5e21a'
        (216, 226,  25), # '#d8e219'
        (218, 227,  25), # '#dae319'
        (221, 227,  24), # '#dde318'
        (223, 227,  24), # '#dfe318'
        (226, 228,  24), # '#e2e418'
        (229, 228,  25), # '#e5e419'
        (231, 228,  25), # '#e7e419'
        (234, 229,  26), # '#eae51a'
        (236, 229,  27), # '#ece51b'
        (239, 229,  28), # '#efe51c'
        (241, 229,  29), # '#f1e51d'
        (244, 230,  30), # '#f4e61e'
        (246, 230,  32), # '#f6e620'
        (248, 230,  33), # '#f8e621'
        (251, 231,  35), # '#fbe723'
        (253, 231,  37), # '#fde725'
    ],
}
"""dict(str, list(tuple(int,int,int)): Color gradients."""

COLORSPACES = [
     RGB, HSV, LINRGB, XYZ, CIELUV, LCH_UV, CIELAB, LCH_AB, OKLAB, OKLCH,
] = [  0,   1,      2,   3,      4,      5,      6,      7,     8,     9,
]
"""list(str): Available color spaces."""

# END   CONSTANTS


# BEGIN DECORATORS
# No decorators
# END   DECORATORS


# BEGIN CLASSES
# No classes
# END   CLASSES


# BEGIN FUNCTIONS

def from_hexcode(string):
    """Convert hex color code into rgb tuple.

    Args:
        string (str): hex code with or without '#'
    Returns:
        tuple(int,int,int): parsed color
    """
    hex_color = int(code.removeprefix('#'), base=16)
    R = (0xFF0000 & hex_color) >> 16
    G = (0x00FF00 & hex_color) >>  8
    B = (0x0000FF & hex_color) >>  0
    tuple_color = (R,G,B)
    return tuple_color

def to_hexcode(tuple_color):
    """Convert rgb tuple into hex color code.

    Args:
        tuple_color (tuple(int,int,int)): input color
    Returns:
        str: hex code string (without '#')
    """
    (R,G,B) = tuple_color
    hex_color = (R << 16) | (G << 8) | (B << 0)
    string = f"{hex_color:06x}"
    return string

def change_space(input_color, from_space, to_space):
    """
    Convert a color tuple between one of the available spaces.

    Note that currently for implementation simplicity all available spaces
    conversions are bridged over RGB (i.e. worst case it is;
    CIELAB -> LCH_AB == CIELAB -> XYZ -> RGB -> XYZ -> CIELAB -> LCH_AB):
    - 'RGB': ([0,255], [0,255], [0,255])
        * Red, Green, Blue
    - 'LINRGB': ([0,1], [0,1], [0,1])
        * Red, Green, Blue
        * https://bottosson.github.io/posts/colorwrong/#what-can-we-do%3F
    - 'HSV': ([0,360], [0,1], [0,1])
        * Hue, Value, Saturation
        * Hue = Red-Green-Blue-Red
        * https://en.wikipedia.org/wiki/HSL_and_HSV
    - 'XYZ': ([?], [?], [?])
        * ?, ?, ?
        * https://en.wikipedia.org/wiki/SRGB
    - 'CIELAB': ([0,100], [-128,127], [-128,127])
        * Lightness, Green-Magenta, Blue-Yellow
        * https://en.wikipedia.org/wiki/CIELAB_color_space
    - 'LCH_AB': ([0,100], [?], [0,2pi])
        * Lightness, Chroma, Hue
        * Hue = Red-Yellow-Green-Blue-Red
        * https://en.wikipedia.org/wiki/CIELAB_color_space
    - 'CIELUV': ([0,100], [-1??,1??], [-1??,1??])
        * Lightness, ?-?, ?-?
        * https://en.wikipedia.org/wiki/CIELUV
    - 'LCH_UV': ([0,100], [?], [0,2pi])
        * Lightness, Chroma, Hue
        * Hue = ?
        * https://en.wikipedia.org/wiki/CIELUV
    - 'OKLAB': ([0,1], [?], [?])
        * Lightness, Green-Red, Blue-Yellow
        * https://bottosson.github.io/posts/oklab/
    - 'OKLCH': ([0,1], [?], [0,2pi])
        * Lightness, Chroma, Hue
        * Hue = ?
        * https://bottosson.github.io/posts/oklab/

    Args:
        input_color (tupled(int,int,int)): Color tuple in valid space
        from_space (int): A string standing for a valid source space
        to_space (int): A string standing for a valid destination space

    Returns:
        tuple(float,float,float): Output color in valid space.
    """
    to_normalized = lambda *c: tuple(k/255 for k in c)
    from_normalized = lambda *c: tuple(max(0, min(round(255*x), 255)) for x in c)
    cartesian_to_polar = lambda x,y: (math.sqrt(x**2 + y**2), math.atan2(y,x))
    polar_to_cartesian = lambda r,a: (r * math.cos(a), r * math.sin(a))

    # Casefold and make a case distinction on the conversion between spaces
    spaces = (from_space, to_space)
    if spaces == (RGB, RGB):
        output_color = input_color
    elif spaces == (RGB, LINRGB):
        (R,G,B) = input_color
        (R1,G1,B1) = to_normalized(R,G,B)
        def lin(x): # linear-light values
            if x > 0.04045: return ((x + 0.055) / 1.055)**2.4
            else:           return x / 12.92
        (Rl,Gl,Bl) = lin(R1), lin(G1), lin(B1)
        output_color = (Rl,Gl,Bl)
    elif spaces == (LINRGB, RGB):
        (Rl,Gl,Bl) = input_color
        def lin_inv(x):
            if x > 0.0031308: return 1.055 * x**(1/2.4) - 0.055
            else:             return 12.92 * x
        (R1,G1,B1) = lin_inv(Rl), lin_inv(Gl), lin_inv(Bl)
        (R,G,B) = from_normalized(R1,G1,B1)
        output_color = (R,G,B)
    elif spaces == (RGB, HSV):
        (R,G,B) = input_color
        (R1,G1,B1) = to_normalized(R,G,B)
        M = max(R1, G1, B1)
        m = min(R1, G1, B1)
        C = M - m
        H1 =            0  if C == 0  else \
            (G1-B1) / C % 6  if M == R1 else \
            (B1-R1) / C + 2  if M == G1 else \
            (R1-G1) / C + 4  if M == B1 else None
        H = round(H1 * 60)
        V = M
        S = 0 if V==0 else (C / V)
        output_color = (H,S,V)
    elif spaces == (HSV, RGB):
        (H,S,V) = input_color
        def f(n):
            k = (n + H%360 / 60) % 6
            return V - V * S * max(0, min(k,4-k, 1))
        R1,G1,B1 = f(5), f(3), f(1)
        (R,G,B) = from_normalized(R1,G1,B1)
        output_color = (R,G,B)
    elif spaces == (RGB, XYZ):
        (R,G,B) = input_color
        (Rl,Gl,Bl) = change_space((R,G,B), RGB,LINRGB)
        X = 0.4124*Rl + 0.3576*Gl + 0.1805*Bl
        Y = 0.2126*Rl + 0.7152*Gl + 0.0722*Bl
        Z = 0.0193*Rl + 0.1193*Gl + 0.9505*Bl
        output_color = (X,Y,Z)
    elif spaces == (XYZ, RGB):
        (X,Y,Z) = input_color
        Rl =  3.2405*X - 1.5372*Y - 0.4986*Z
        Gl = -0.9689*X + 1.8758*Y + 0.0415*Z
        Bl =  0.0557*X - 0.2040*Y + 1.0570*Z
        (R,G,B) = change_space((Rl,Gl,Bl), LINRGB,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, CIELAB):
        (R,G,B) = input_color
        (X,Y,Z) = change_space((R,G,B), RGB,XYZ)
        (X100,Y100,Z100) = X*100, Y*100, Z*100
        def f(x):
            delta = 6/29
            if x > delta**3: return x**(1/3)
            else:            return x / (3*delta**2) + 4/29
        (XD65,YD65,ZD65) = (95.0489, 100, 108.8840) # Standard illuminant
        L = 116 * f(Y100 / YD65)  - 16
        A = 500 * (f(X100 / XD65) - f(Y100 / YD65))
        B = 200 * (f(Y100 / YD65) - f(Z100 / ZD65))
        output_color = (L,A,B)
    elif spaces == (CIELAB, RGB):
        (L,A,B) = input_color
        def f_inv(x):
            delta = 6/29
            if x > delta: return x**3
            else:         return (x - 4/29) * 3*delta**2
        (XD65,YD65,ZD65) = (95.0489, 100, 108.8840) # Standard illuminant
        X100 = XD65 * f_inv((L + 16)/116 + A/500)
        Y100 = YD65 * f_inv((L + 16)/116)
        Z100 = ZD65 * f_inv((L + 16)/116 - B/200)
        (X,Y,Z) = X100/100, Y100/100, Z100/100
        (R,G,B) = change_space((X,Y,Z), XYZ,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, CIELUV):
        (R,G,B) = input_color
        (X,Y,Z) = change_space((R,G,B), RGB,XYZ)
        (XD65,YD65,ZD65) = (95.0489, 100, 108.8840) # Standard illuminant
        L = 116 * Y/YD65**(1/3) - 16 if Y/YD65 > (6/29)**3 else (29/3)**3 * Y/YD65
        Up = (4*X) / (X + 15*Y + 3*Z)
        Vp = (9*Y) / (X + 15*Y + 3*Z)
        (UD65,VD65) = (0.2009, 0.4610) # Standard illuminant
        U = 13 * L * (Up - UD65)
        V = 13 * L * (Vp - VD65)
        output_color = (L,U,V)
    elif spaces == (CIELUV, RGB):
        (L,U,V) = input_color
        (UD65,VD65) = (0.2009, 0.4610) # Standard illuminant
        Up = U / (13*L) + UD65
        Vp = V / (13*L) + VD65
        (XD65,YD65,ZD65) = (95.0489, 100, 108.8840) # Standard illuminant
        Y = YD65 * ((L + 16) / 116)**3 if L > 8 else YD65 * L * (3/29)**3
        X = Y * (9*Up) / (4*Vp)
        Z = Y * (12 - 3*Up - 20*Vp) / (4*Vp)
        (R,G,B) = change_space((X,Y,Z), XYZ,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, OKLAB):
        (R,G,B) = input_color
        (Rl,Gl,Bl) = change_space((R,G,B), RGB,LINRGB)
        l = 0.4122214708*Rl + 0.5363325363*Gl + 0.0514459929*Bl
        m = 0.2119034982*Rl + 0.6806995451*Gl + 0.1073969566*Bl
        s = 0.0883024619*Rl + 0.2817188376*Gl + 0.6299787005*Bl
        (lp,mp,sp) = l**(1/3), m**(1/3), s**(1/3)
        L = 0.2104542553*lp + 0.7936177850*mp - 0.0040720468*sp
        A = 1.9779984951*lp - 2.4285922050*mp + 0.4505937099*sp
        B = 0.0259040371*lp + 0.7827717662*mp - 0.8086757660*sp
        output_color = (L,A,B)
    elif spaces == (OKLAB, RGB):
        (L,A,B) = input_color
        lp = L + 0.3963377774*A + 0.2158037573*B
        mp = L - 0.1055613458*A - 0.0638541728*B
        sp = L - 0.0894841775*A - 1.2914855480*B
        (l,m,s) = lp**3, mp**3, sp**3
        Rl =  4.0767416621*l - 3.3077115913*m + 0.2309699292*s
        Gl = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
        Bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
        (R,G,B) = change_space((Rl,Gl,Bl), LINRGB,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, LCH_AB):
        (R,G,B) = input_color
        (L,A,B) = change_space((R,G,B), RGB,CIELAB)
        (C,H) = cartesian_to_polar(A,B)
        output_color = (L,C,H)
    elif spaces == (LCH_AB, RGB):
        (L,C,H) = input_color
        (A,B) = polar_to_cartesian(C,H)
        (R,G,B) = change_space((L,A,B), CIELAB,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, LCH_UV):
        (R,G,B) = input_color
        (L,U,V) = change_space((R,G,B), RGB,CIELUV)
        (C,H) = cartesian_to_polar(U,V)
        output_color = (L,C,H)
    elif spaces == (LCH_UV, RGB):
        (L,C,H) = input_color
        (U,V) = polar_to_cartesian(C,H)
        (R,G,B) = change_space((L,U,V), CIELUV,RGB)
        output_color = (R,G,B)
    elif spaces == (RGB, OKLCH):
        (R,G,B) = input_color
        (L,A,B) = change_space((R,G,B), RGB,OKLAB)
        (C,H) = cartesian_to_polar(A,B)
        output_color = (L,C,H)
    elif spaces == (OKLCH, RGB):
        (L,C,H) = input_color
        (A,B) = polar_to_cartesian(C,H)
        (R,G,B) = change_space((L,A,B), OKLAB,RGB)
        output_color = (R,G,B)
    else:
        if any (space not in COLORSPACES for space in spaces):
            raise RuntimeError("unrecognized colorspace conversion '{spaces}'")
        output_color = change_space(
            change_space(input_color, from_space,RGB), RGB,to_space)
    return output_color

def randrgb():
    """Generates an random-valued RGB color tuple."""
    color_random = tuple(random.randrange(256) for _ in range(3))
    return color_random

def randhue():
	"""Generates an HSV-(random Hue)-(full Sat.)-(full Val.) RGB color tuple."""
	p = random.randrange(6) #  Alea iacta est
	val = lambda i:(1-(p%3-i)**2%3)*((1-p%2*2)*(random.randrange(255)-p%2*255))+((p%3-i)**2%3)*(255*(1-(i-2+(p-p%2)//2)**2%3))
	color_random = tuple(val(i) for i in range(3)) # Return tuple
	return color_random

def mix(color0, color1, param=0.5, rnd=True):
    """Mix two color tuples evenly or with an optional weight parameter.

    Args:
        color0, color1 (tuple(float,float,float)): Color tuples in a same
            (arbitrary) space.
        param (float): A linear interpolation parameter 0 <= param <= 1
            used for mixing (default is 0.5).
        rnd (bool): Whether to round channel values, for RGB purposes
            (default is True).

    Returns:
        tuple(float,float,float): Mixed color.
    """
    if not (0 <= param <= 1):
        raise ValueError(f"interpolation parameter must be 0 <= param <= 1: {param}")
    if rnd:
        color_mixed = (
            round((1-param) * color0[0] + param * color1[0]),
            round((1-param) * color0[1] + param * color1[1]),
            round((1-param) * color0[2] + param * color1[2]),
        )
    else:
        color_mixed = (
            (1-param) * color0[0] + param * color1[0],
            (1-param) * color0[1] + param * color1[1],
            (1-param) * color0[2] + param * color1[2],
        )
    #color_mixed = tuple(((1-param) * ch0 + param * ch1) for ch0,ch1 in zip(color0,color1))
    #if rnd:
        #color_mixed = tuple(round(ch) for ch in color_mixed)
    return color_mixed

def interpolate(colors, param, rnd=True):
    """Interpolate a color within a color map using some parameter.

    Args:
        colors (list(tuple(float,float,float))): Color tuples in a same
            (arbitrary) space.
        param (float): A linear interpolation parameter 0 <= param <= 1
            used for interpolation (default is 0.5).
        rnd (bool): Whether to round channel values, for RGB purposes
            (default is True).

    Returns:
        tuple(float,float,float): Interpolated color.
    """
    if not (0 <= param <= 1):
        raise ValueError(f"interpolation parameter must be 0 <= param <= 1: {param}")
    if param == 1.0:
        return colors[-1]
    # Find segment in the color map within which to actually interpolate
    sectors = len(colors) - 1
    segmentlength = 1 / sectors
    sector = int(param // segmentlength)
    # Interpolate between closest two colors
    sectorparam = param % segmentlength / segmentlength
    color_interpolated = mix(colors[sector], colors[sector+1], sectorparam, rnd)
    return color_interpolated

def average(*colors, rnd=True):
    """Arithmetically average an iterable of color tuples.

    Args:
        *colors (tuple(tuple(float,float,float))): Color tuples in a same
            (arbitrary) space.
        rnd (bool): Whether to round channel values, for RGB purposes
            (default is True).

    Returns:
        tuple(float,float,float): Average color.
    """
    # Sum up values per individual channel then make average
    add = lambda c1,c2: tuple(ch1+ch2 for ch1,ch2 in zip(c1,c2))
    color_sum = (0,0,0)
    count = 0
    for color in colors:
        color_sum = add(color_sum, color)
        count += 1
    color_average = tuple((ch/count) for ch in color_sum)
    if rnd:
        color_average = tuple(round(ch) for ch in color_average)
    return color_average

def rainbow_color(param, color0=RED, over_space=OKLCH):
    """Generate a rainbow color using a possibly cycling parameter.

    Args:
        param (float): Cycle parameter with circle period [0, 1].
        color0 (tuple(int,int,int)): Optional initial RGB color
            (default is RED).
        over_space (int): Optional cylindrical color space model
            {HSV ,LCH_AB, LCH_UV, OKLCH} (default is OKLCH)

    Returns:
        tuple(int,int,int): 'Rainbow' RGB color tuple.
    """
    cyclespaces = [HSV, LCH_AB, LCH_UV, OKLCH]
    if over_space == HSV:
        (H0,S0,V0) = change_space(color0, RGB,HSV)
        H = (H0 + 360 * param) % 360 # Reduce period
        S = S0
        V = V0
        (R,G,B) = change_space((H,S,V), HSV,RGB)
    elif over_space in {LCH_AB, LCH_UV, OKLCH}:
        (L0,C0,H0) = change_space(color0, RGB,over_space)
        L = L0
        C = C0
        H = (H0 + math.tau * param) % math.tau # Reduce period
        (R,G,B) = change_space((L,C,H), over_space,RGB)
    else:
        raise RuntimeError("unrecognized colorspace name for hue cycling")
    return (R,G,B)

def rainbow_palette(granularity, color0=RED, over_space=OKLCH, keepend=False):
    """Generate a rainbow palette of specified granularity.

    Args:
        granularity (int): number of different, equally-spaced hues.
        color0 (tuple(int,int,int)): Optional initial RGB color
            (default is RED).
        over_space (str): Optional cylindrical color space model
            {HSV ,LCH_AB, LCH_UV, OKLCH} (default is OKLCH)
        keepend (bool): Whether to additionally include the first hue as last
            (default is False).

    Returns:
        list(tuple(int,int,int)): 'Rainbow' RGB color palette.
    """
    gradient = [
        rainbow_color(k/granularity, color0, over_space)
        for k in range(granularity+keepend)
    ]
    return gradient

# END   FUNCTIONS


# BEGIN MAIN

def main():
    HQviridis_data = [ # 256 normalized 'viridis'-colormpa RGB values
        [0.267004, 0.004874, 0.329415],
        [0.268510, 0.009605, 0.335427],
        [0.269944, 0.014625, 0.341379],
        [0.271305, 0.019942, 0.347269],
        [0.272594, 0.025563, 0.353093],
        [0.273809, 0.031497, 0.358853],
        [0.274952, 0.037752, 0.364543],
        [0.276022, 0.044167, 0.370164],
        [0.277018, 0.050344, 0.375715],
        [0.277941, 0.056324, 0.381191],
        [0.278791, 0.062145, 0.386592],
        [0.279566, 0.067836, 0.391917],
        [0.280267, 0.073417, 0.397163],
        [0.280894, 0.078907, 0.402329],
        [0.281446, 0.084320, 0.407414],
        [0.281924, 0.089666, 0.412415],
        [0.282327, 0.094955, 0.417331],
        [0.282656, 0.100196, 0.422160],
        [0.282910, 0.105393, 0.426902],
        [0.283091, 0.110553, 0.431554],
        [0.283197, 0.115680, 0.436115],
        [0.283229, 0.120777, 0.440584],
        [0.283187, 0.125848, 0.444960],
        [0.283072, 0.130895, 0.449241],
        [0.282884, 0.135920, 0.453427],
        [0.282623, 0.140926, 0.457517],
        [0.282290, 0.145912, 0.461510],
        [0.281887, 0.150881, 0.465405],
        [0.281412, 0.155834, 0.469201],
        [0.280868, 0.160771, 0.472899],
        [0.280255, 0.165693, 0.476498],
        [0.279574, 0.170599, 0.479997],
        [0.278826, 0.175490, 0.483397],
        [0.278012, 0.180367, 0.486697],
        [0.277134, 0.185228, 0.489898],
        [0.276194, 0.190074, 0.493001],
        [0.275191, 0.194905, 0.496005],
        [0.274128, 0.199721, 0.498911],
        [0.273006, 0.204520, 0.501721],
        [0.271828, 0.209303, 0.504434],
        [0.270595, 0.214069, 0.507052],
        [0.269308, 0.218818, 0.509577],
        [0.267968, 0.223549, 0.512008],
        [0.266580, 0.228262, 0.514349],
        [0.265145, 0.232956, 0.516599],
        [0.263663, 0.237631, 0.518762],
        [0.262138, 0.242286, 0.520837],
        [0.260571, 0.246922, 0.522828],
        [0.258965, 0.251537, 0.524736],
        [0.257322, 0.256130, 0.526563],
        [0.255645, 0.260703, 0.528312],
        [0.253935, 0.265254, 0.529983],
        [0.252194, 0.269783, 0.531579],
        [0.250425, 0.274290, 0.533103],
        [0.248629, 0.278775, 0.534556],
        [0.246811, 0.283237, 0.535941],
        [0.244972, 0.287675, 0.537260],
        [0.243113, 0.292092, 0.538516],
        [0.241237, 0.296485, 0.539709],
        [0.239346, 0.300855, 0.540844],
        [0.237441, 0.305202, 0.541921],
        [0.235526, 0.309527, 0.542944],
        [0.233603, 0.313828, 0.543914],
        [0.231674, 0.318106, 0.544834],
        [0.229739, 0.322361, 0.545706],
        [0.227802, 0.326594, 0.546532],
        [0.225863, 0.330805, 0.547314],
        [0.223925, 0.334994, 0.548053],
        [0.221989, 0.339161, 0.548752],
        [0.220057, 0.343307, 0.549413],
        [0.218130, 0.347432, 0.550038],
        [0.216210, 0.351535, 0.550627],
        [0.214298, 0.355619, 0.551184],
        [0.212395, 0.359683, 0.551710],
        [0.210503, 0.363727, 0.552206],
        [0.208623, 0.367752, 0.552675],
        [0.206756, 0.371758, 0.553117],
        [0.204903, 0.375746, 0.553533],
        [0.203063, 0.379716, 0.553925],
        [0.201239, 0.383670, 0.554294],
        [0.199430, 0.387607, 0.554642],
        [0.197636, 0.391528, 0.554969],
        [0.195860, 0.395433, 0.555276],
        [0.194100, 0.399323, 0.555565],
        [0.192357, 0.403199, 0.555836],
        [0.190631, 0.407061, 0.556089],
        [0.188923, 0.410910, 0.556326],
        [0.187231, 0.414746, 0.556547],
        [0.185556, 0.418570, 0.556753],
        [0.183898, 0.422383, 0.556944],
        [0.182256, 0.426184, 0.557120],
        [0.180629, 0.429975, 0.557282],
        [0.179019, 0.433756, 0.557430],
        [0.177423, 0.437527, 0.557565],
        [0.175841, 0.441290, 0.557685],
        [0.174274, 0.445044, 0.557792],
        [0.172719, 0.448791, 0.557885],
        [0.171176, 0.452530, 0.557965],
        [0.169646, 0.456262, 0.558030],
        [0.168126, 0.459988, 0.558082],
        [0.166617, 0.463708, 0.558119],
        [0.165117, 0.467423, 0.558141],
        [0.163625, 0.471133, 0.558148],
        [0.162142, 0.474838, 0.558140],
        [0.160665, 0.478540, 0.558115],
        [0.159194, 0.482237, 0.558073],
        [0.157729, 0.485932, 0.558013],
        [0.156270, 0.489624, 0.557936],
        [0.154815, 0.493313, 0.557840],
        [0.153364, 0.497000, 0.557724],
        [0.151918, 0.500685, 0.557587],
        [0.150476, 0.504369, 0.557430],
        [0.149039, 0.508051, 0.557250],
        [0.147607, 0.511733, 0.557049],
        [0.146180, 0.515413, 0.556823],
        [0.144759, 0.519093, 0.556572],
        [0.143343, 0.522773, 0.556295],
        [0.141935, 0.526453, 0.555991],
        [0.140536, 0.530132, 0.555659],
        [0.139147, 0.533812, 0.555298],
        [0.137770, 0.537492, 0.554906],
        [0.136408, 0.541173, 0.554483],
        [0.135066, 0.544853, 0.554029],
        [0.133743, 0.548535, 0.553541],
        [0.132444, 0.552216, 0.553018],
        [0.131172, 0.555899, 0.552459],
        [0.129933, 0.559582, 0.551864],
        [0.128729, 0.563265, 0.551229],
        [0.127568, 0.566949, 0.550556],
        [0.126453, 0.570633, 0.549841],
        [0.125394, 0.574318, 0.549086],
        [0.124395, 0.578002, 0.548287],
        [0.123463, 0.581687, 0.547445],
        [0.122606, 0.585371, 0.546557],
        [0.121831, 0.589055, 0.545623],
        [0.121148, 0.592739, 0.544641],
        [0.120565, 0.596422, 0.543611],
        [0.120092, 0.600104, 0.542530],
        [0.119738, 0.603785, 0.541400],
        [0.119512, 0.607464, 0.540218],
        [0.119423, 0.611141, 0.538982],
        [0.119483, 0.614817, 0.537692],
        [0.119699, 0.618490, 0.536347],
        [0.120081, 0.622161, 0.534946],
        [0.120638, 0.625828, 0.533488],
        [0.121380, 0.629492, 0.531973],
        [0.122312, 0.633153, 0.530398],
        [0.123444, 0.636809, 0.528763],
        [0.124780, 0.640461, 0.527068],
        [0.126326, 0.644107, 0.525311],
        [0.128087, 0.647749, 0.523491],
        [0.130067, 0.651384, 0.521608],
        [0.132268, 0.655014, 0.519661],
        [0.134692, 0.658636, 0.517649],
        [0.137339, 0.662252, 0.515571],
        [0.140210, 0.665859, 0.513427],
        [0.143303, 0.669459, 0.511215],
        [0.146616, 0.673050, 0.508936],
        [0.150148, 0.676631, 0.506589],
        [0.153894, 0.680203, 0.504172],
        [0.157851, 0.683765, 0.501686],
        [0.162016, 0.687316, 0.499129],
        [0.166383, 0.690856, 0.496502],
        [0.170948, 0.694384, 0.493803],
        [0.175707, 0.697900, 0.491033],
        [0.180653, 0.701402, 0.488189],
        [0.185783, 0.704891, 0.485273],
        [0.191090, 0.708366, 0.482284],
        [0.196571, 0.711827, 0.479221],
        [0.202219, 0.715272, 0.476084],
        [0.208030, 0.718701, 0.472873],
        [0.214000, 0.722114, 0.469588],
        [0.220124, 0.725509, 0.466226],
        [0.226397, 0.728888, 0.462789],
        [0.232815, 0.732247, 0.459277],
        [0.239374, 0.735588, 0.455688],
        [0.246070, 0.738910, 0.452024],
        [0.252899, 0.742211, 0.448284],
        [0.259857, 0.745492, 0.444467],
        [0.266941, 0.748751, 0.440573],
        [0.274149, 0.751988, 0.436601],
        [0.281477, 0.755203, 0.432552],
        [0.288921, 0.758394, 0.428426],
        [0.296479, 0.761561, 0.424223],
        [0.304148, 0.764704, 0.419943],
        [0.311925, 0.767822, 0.415586],
        [0.319809, 0.770914, 0.411152],
        [0.327796, 0.773980, 0.406640],
        [0.335885, 0.777018, 0.402049],
        [0.344074, 0.780029, 0.397381],
        [0.352360, 0.783011, 0.392636],
        [0.360741, 0.785964, 0.387814],
        [0.369214, 0.788888, 0.382914],
        [0.377779, 0.791781, 0.377939],
        [0.386433, 0.794644, 0.372886],
        [0.395174, 0.797475, 0.367757],
        [0.404001, 0.800275, 0.362552],
        [0.412913, 0.803041, 0.357269],
        [0.421908, 0.805774, 0.351910],
        [0.430983, 0.808473, 0.346476],
        [0.440137, 0.811138, 0.340967],
        [0.449368, 0.813768, 0.335384],
        [0.458674, 0.816363, 0.329727],
        [0.468053, 0.818921, 0.323998],
        [0.477504, 0.821444, 0.318195],
        [0.487026, 0.823929, 0.312321],
        [0.496615, 0.826376, 0.306377],
        [0.506271, 0.828786, 0.300362],
        [0.515992, 0.831158, 0.294279],
        [0.525776, 0.833491, 0.288127],
        [0.535621, 0.835785, 0.281908],
        [0.545524, 0.838039, 0.275626],
        [0.555484, 0.840254, 0.269281],
        [0.565498, 0.842430, 0.262877],
        [0.575563, 0.844566, 0.256415],
        [0.585678, 0.846661, 0.249897],
        [0.595839, 0.848717, 0.243329],
        [0.606045, 0.850733, 0.236712],
        [0.616293, 0.852709, 0.230052],
        [0.626579, 0.854645, 0.223353],
        [0.636902, 0.856542, 0.216620],
        [0.647257, 0.858400, 0.209861],
        [0.657642, 0.860219, 0.203082],
        [0.668054, 0.861999, 0.196293],
        [0.678489, 0.863742, 0.189503],
        [0.688944, 0.865448, 0.182725],
        [0.699415, 0.867117, 0.175971],
        [0.709898, 0.868751, 0.169257],
        [0.720391, 0.870350, 0.162603],
        [0.730889, 0.871916, 0.156029],
        [0.741388, 0.873449, 0.149561],
        [0.751884, 0.874951, 0.143228],
        [0.762373, 0.876424, 0.137064],
        [0.772852, 0.877868, 0.131109],
        [0.783315, 0.879285, 0.125405],
        [0.793760, 0.880678, 0.120005],
        [0.804182, 0.882046, 0.114965],
        [0.814576, 0.883393, 0.110347],
        [0.824940, 0.884720, 0.106217],
        [0.835270, 0.886029, 0.102646],
        [0.845561, 0.887322, 0.099702],
        [0.855810, 0.888601, 0.097452],
        [0.866013, 0.889868, 0.095953],
        [0.876168, 0.891125, 0.095250],
        [0.886271, 0.892374, 0.095374],
        [0.896320, 0.893616, 0.096335],
        [0.906311, 0.894855, 0.098125],
        [0.916242, 0.896091, 0.100717],
        [0.926106, 0.897330, 0.104071],
        [0.935904, 0.898570, 0.108131],
        [0.945636, 0.899815, 0.112838],
        [0.955300, 0.901065, 0.118128],
        [0.964894, 0.902323, 0.123941],
        [0.974417, 0.903590, 0.130215],
        [0.983868, 0.904867, 0.136897],
        [0.993248, 0.906157, 0.143936],
    ]
    for [r,g,b] in HQviridis_data:
        R,G,B = round(255*r),round(255*g),round(255*b)
        print(f"({R: 3}, {G: 3}, {B: 3}), # '#{_tuple_to_hex((R,G,B)):06x}'")

#if __name__=="__main__": main() # No main

# END   MAIN
