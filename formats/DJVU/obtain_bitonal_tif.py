from PIL import Image

file = "example.tif"
img = Image.open(file)
img.convert('1')
im1 = img.save("example_bw.tif")
img.show()