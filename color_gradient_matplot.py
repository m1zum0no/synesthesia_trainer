import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

colormap_hex = []
colormap_rgba = mpl.colormaps['twilight_shifted']

def rgba_to_hex(rgba_val):
    return mpl.colors.to_hex(rgba_val, keep_alpha=False)

i = 0
while i < (len(colormap_rgba.colors) - 1):
  hex_color = rgba_to_hex(colormap_rgba.colors[i])
  colormap_hex.append(hex_color)
  i += 1