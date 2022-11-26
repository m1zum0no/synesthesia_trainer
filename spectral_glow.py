import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import seaborn as sns

colormap_hex = []

def rgba_to_hex(rgba_val):
    return mpl.colors.to_hex(rgba_val, keep_alpha=False)

# LinearSegmentedColormap as LSC
def hex_from_LSC():
    # custom colormap from the range of values at the end and beginning of the Spectral 
    # to even out cyclic transition of colors
    purple_red_range = LinearSegmentedColormap.from_list('filler_range', (
                                                        # tool for generating color gradients at
                                                        # https://eltos.github.io/gradient/#filler_range=5C51A3-9E0142
                                                        (0.000, (0.361, 0.318, 0.639)),
                                                        (1.000, (0.620, 0.004, 0.259))), N=128)
    purple_red_range._init()
    rgbas = purple_red_range._lut
    hex_arr = [mpl.colors.rgb2hex(x) for x in rgbas]
    for i in range(len(hex_arr) - 4):  # removing extraneous frames in the end of colormap
        if not (hex_arr[i] in [ '#ffffff', '#000000' ]):
            colormap_hex.append(hex_arr[i]) 

# ListedColormap as LC
def hex_from_LC():
    spectral = ListedColormap(sns.color_palette("Spectral", 256))
    i = 0
    last = len(spectral.colors) - 1
    while i < last:
        hex_color = rgba_to_hex(spectral.colors[i])
        if not (hex_color in [ '#ffffff', '#000000' ]):
            colormap_hex.append(hex_color)
        i += 1
        if i == last:
            hex_from_LSC()
 
speed_arg = 15
hex_from_LC()