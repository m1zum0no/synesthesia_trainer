import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#from colorspacious import cspace_converter  # pip3 install -U matplotlib
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

colormap_hex = []

def generate_hex_from_theme(theme):
    cmap = mpl.colormaps[theme]
    cmap._init()
    rgbas = cmap._lut
    hex_arr = [mpl.colors.rgb2hex(x) for x in rgbas]
    for i in range(len(hex_arr) - 1):
        colormap_hex.append(hex_arr[i])

themes = ['BuPu', 'YlGnBu', 'RdPu']

for i in themes:
    generate_hex_from_theme(i)