import sys  # for cli arguments 
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import seaborn as sns

colormap_hex = []

def generate_hex_from_theme(theme):
    cmap = mpl.colormaps[theme]
    cmap._init()
    rgbas = cmap._lut
    hex_arr = [mpl.colors.rgb2hex(x) for x in rgbas]
    for i in range(len(hex_arr) - 1):
        if not (hex_arr[i] in [ '#ffffff', '#000000' ]):
            colormap_hex.append(hex_arr[i])

extracted_theme = sys.argv
speed_arg = sys.argv[2]
generate_hex_from_theme(extracted_theme[1])
