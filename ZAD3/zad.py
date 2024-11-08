from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np

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

    # Display the image
    axes[i // width, i % width].imshow(image, cmap='gray')
plt.show()
# # wczytaj plik
# filename = "samolot08.jpg"
# image = io.imread("./Lab4_images/" + filename)

# # threshold image - powyżej 128 czarny, poniżej biały
# image = thresh(image, 128)



# # Display original image
# io.imshow(image)
# plt.show()

