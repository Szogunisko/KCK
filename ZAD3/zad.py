from skimage import io, filters, data, color, measure, exposure
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

def findEdges1(image):
    intensityP = 1
    intensityK = 10
    pp, pk = np.percentile(image, (intensityP, intensityK))
    image = exposure.rescale_intensity(image, in_range=(pp, pk))
    image = color.rgb2hsv(image)
    blackWhite = np.zeros([len(image), len(image[0])])
    for i in range(len(image)):
        for j in range(len(image[i])):
            blackWhite[i][j] = 1 - image[i][j][2]
            image[i][j] = [0, 0, 0]
    contours = measure.find_contours(blackWhite, 0.3)
    return image, contours

def drawPlotsBlack(CurrentImage, ax):
    frame = ax  # Używamy dostarczonej osi (subplotu)
    frame.set_facecolor("black")  # Czarne tło
    frame.axis('off')  # Ukrycie osi
    image, contours = findEdges1(CurrentImage)  # Znajdywanie krawędzi
    for n, contour in enumerate(contours):
        frame.plot(contour[:, 1], contour[:, 0], linewidth=0.8, color="w")  # Rysowanie konturu na obrazie
    frame.imshow(image)  # Wyświetlenie obrazu

height = 2
width = 4
fig, axes = plt.subplots(height, width, figsize=(10, 5))
axes = axes.ravel()  # Spłaszczenie osi do jednej listy, aby można było indeksować je jednym indeksem

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
    drawPlotsBlack(image, axes[i])  # Używamy konkretnej osi
    # Display the image     
plt.show()


# # wczytaj plik
# filename = "samolot08.jpg"
# image = io.imread("./Lab4_images/" + filename)

# # threshold image - powyżej 128 czarny, poniżej biały
# image = thresh(image, 128)



# # Display original image
# io.imshow(image)
# plt.show()