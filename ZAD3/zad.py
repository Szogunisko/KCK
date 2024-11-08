from skimage import filters, data, io
from matplotlib import pyplot as plt
filename = "samolot07.jpg"
image = io.imread("./Lab4_images/" + filename) # Albo: coins(), page(), moon()
io.imshow(image)
plt.show() # Niepotrzebne, jesli ipython notebook --matplotlib=inline