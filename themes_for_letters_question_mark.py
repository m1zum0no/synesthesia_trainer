import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

colormap_hex = []

def generate_hex_from_theme(theme):
    cmap = mpl.colormaps[theme]
    if theme == 'gist_earth':
        cmap = cmap.reversed()
    cmap._init()
    rgbas = cmap._lut
    hex_arr = [mpl.colors.rgb2hex(x) for x in rgbas]
    # removing extraneous color frames 
    for i in range(len(hex_arr) - 6):
        if not (hex_arr[i] in [ '#ffffff', '#000000' ]):
            colormap_hex.append(hex_arr[i])

themes_options = ['cubehelix', 'gist_earth']
speed_arg = 25
for i in themes_options:
    generate_hex_from_theme(i)