from skimage import io, color, img_as_float
from matplotlib import pyplot as plt
import numpy as np
from skimage.filters.edges import convolve
from scipy.signal import convolve2d
import array

# Define the thresholding function
def thresh(image, t):
    #convert to greyscale
    image = color.rgb2gray(image) * 255  # Convert to grayscale and scale to [0, 255]
    image = image.astype(np.uint8)
    # Create a binary image: pixels > t become 0 (black), <= t become 255 (white)
    binary = np.where(image > t, 0, 255).astype(np.uint8)
    return binary

height = 2
width = 4
fig, axes = plt.subplots(height, width, figsize=(10, 5))

start_nr = 5
end_nr = start_nr + height * width
for i, nr in enumerate(range(start_nr, end_nr, 1)):
    # Load the image
    filename = "samolot"
    if nr < 10:
        filename += "0"
    filename += str(nr) + ".jpg"
    image = io.imread("./Lab4_images/" + filename)

    # Threshold the image
    image = thresh(image, 128)
    
    cam = img_as_float(image)
    Kh = np.array([[ 1, 2, 1],
                [ 0, 0, 0],
                [-1,-2,-1]]) 
    Kh = Kh / 4

    Kv = np.array([[ 1, 0,-1],
                [ 2, 0,-2],
                [ 1, 0,-1]])
    Kv = Kv / 4                    

    hor = np.abs(convolve2d(cam, Kh, mode="same"))
    ver = np.abs(convolve2d(cam, Kv, mode="same"))
    res = (hor+ver)/2
    
    # Display the image
    axes[i // width, i % width].imshow(res, cmap='gray')
plt.show()
# # wczytaj plik
# filename = "samolot08.jpg"
# image = io.imread("./Lab4_images/" + filename)

# # threshold image - powyżej 128 czarny, poniżej biały
# image = thresh(image, 128)



# # Display original image
# io.imshow(image)
# plt.show()

