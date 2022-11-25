import matplotlib as mpl
from matplotlib.colors import ListedColormap
import seaborn as sns

colormap_hex = []

def rgba_to_hex(rgba_val):
    return mpl.colors.to_hex(rgba_val, keep_alpha=False)

def generate_hex_from_theme():
    cmap = ListedColormap(sns.husl_palette(256))
    i = 0
    while i < (len(cmap.colors) - 1):
        hex_color = rgba_to_hex(cmap.colors[i])
        colormap_hex.append(hex_color)
        i += 1

speed_arg = 10
generate_hex_from_theme()