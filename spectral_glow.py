import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import seaborn as sns

letters_fg_color_range = []


# LinearSegmentedColormap as LSC
def hex_from_LSC(cmap, event_colors_hex_array):
    cmap._init()
    rgbas = cmap._lut
    hex_arr = [mpl.colors.rgb2hex(x) for x in rgbas]
    for i in range(len(hex_arr) - 4):  # removing extraneous frames in the end of colormap
        if not (hex_arr[i] in [ '#ffffff', '#000000' ]):
            event_colors_hex_array.append(hex_arr[i]) 


# ListedColormap as LC
def hex_from_LC(cmap, event_colors_hex_array):
    for i in range(len(cmap.colors)):
        hex_color = mpl.colors.to_hex(cmap.colors[i], keep_alpha=False)
        if not (hex_color in [ '#ffffff', '#000000' ]):
            event_colors_hex_array.append(hex_color)
 

# colormaps to pass as the arguments to functions that convert cmaps of corresponding type to an array of hex values 
spectral = ListedColormap(sns.color_palette("Spectral", 256))

# custom colormap from the range of values at the end and beginning of the Spectral 
# to even out cyclic transition of colors
purple_red_range = LinearSegmentedColormap.from_list('filler_range', (
                                                    # tool for generating color gradients at
                                                    # https://eltos.github.io/gradient/#filler_range=5C51A3-9E0142
                                                    (0.000, (0.361, 0.318, 0.639)),
                                                    (1.000, (0.620, 0.004, 0.259))), N=128)

hex_from_LSC(purple_red_range, letters_fg_color_range)
hex_from_LC(spectral, letters_fg_color_range)