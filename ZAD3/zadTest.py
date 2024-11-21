from skimage import io, color, measure, morphology, exposure, filters
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from skimage.color import rgb2gray
from skimage.filters.edges import convolve
from skimage import img_as_ubyte
from skimage.segmentation import find_boundaries
from skimage.draw import polygon_perimeter, disk


# Funkcja zapisująca zestaw figurek do PDF
def save_figures_to_pdf(figures, filenames):
    for fig, filename in zip(figures, filenames):
        with PdfPages(filename) as pdf:
            pdf.savefig(fig)  # Zapisuje całą figurę
            plt.close(fig)  # Opcjonalne zamknięcie figury po zapisaniu


#Podwyższenie kontrastu
def ContrastUp(image):
    
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]
    
    brightness = (red.mean() + green.mean() + blue.mean()) / 3
    if brightness > 120:
        lowerBound = 1
        upperBound = 25
    else:
        lowerBound = 1
        upperBound = 50
    lb, ub = np.percentile(image, (lowerBound, upperBound))
    image = exposure.rescale_intensity(image, in_range=(lb, ub))
    
    return image

# Funkcja progowania, zamknięcia i filtracji medianowej
def thresh_and_median_filter(image):
    # Konwersja do skali szarości
    hsv_image = color.rgb2hsv(image)

    black_white = 1 - hsv_image[:, :, 2]

    # Progowanie obrazu, aby wyodrębnić obszary samolotów
    threshold_value = filters.threshold_otsu(black_white)
    thresholded_image = black_white > threshold_value
    return black_white, thresholded_image


#Funkcja otwarcia
def openingFunction(image,disk_size):
    # Operacja zamknięcia
    selem = morphology.disk(disk_size)
    opened_image = morphology.opening(image, selem)    
    return opened_image

#Funkcja zamknięcia
def closingFunction(image, disk_size):
   # Operacja zamknięcia
    selem = morphology.disk(disk_size)
    closed_image = morphology.closing(image, selem)    
    return closed_image

#Filtr Sobla
def SobelFilter(image): 
    # Filtr Sobela dla krawędzi pionowych i poziomych
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])
    
    # Konwolucja w kierunku poziomym i pionowym
    edges_x = convolve(image, sobel_x)
    edges_y = convolve(image, sobel_y)
    edges = np.sqrt(edges_x**2 + edges_y**2)
    return edges

def ConnectEdges_and_Random_color(edges):
    if edges.max() - edges.min() > 0:
        edges = (edges - edges.min()) / (edges.max() - edges.min()) * 255
    else:
        edges = np.zeros_like(edges) 
    edges = edges.astype(np.uint8)
    # Etykietowanie samolotów
    labeled_image = measure.label(edges > 0, connectivity=2)
    regions = measure.regionprops(labeled_image)
    # Znajdowanie konturów każdego samolotu
    boundaries = find_boundaries(labeled_image, mode='outer')
    # Przygotowanie pustego obrazu RGB
    color_image = np.zeros((*boundaries.shape, 3), dtype=np.uint8)
    
    # Przypisywanie losowych kolorów każdemu obiektowi
    for label in np.unique(labeled_image):
        if label == 0:
            continue  # pomiń tło
        mask = labeled_image == label
        color = np.random.randint(100, 256, size=3)
        color_image[mask] = color
    return color_image, regions

def overlay_random_colors_on_image(image_colored, random_colored_image, alpha=0.5):
    # Upewnienie się, że obrazy są w formacie RGB
    if len(image_colored.shape) < 3 or image_colored.shape[2] != 3:
        image_colored = color.gray2rgb(image_colored)
    
    if len(random_colored_image.shape) < 3 or random_colored_image.shape[2] != 3:
        random_colored_image = color.gray2rgb(random_colored_image)
    
    # Dopasowanie wymiarów obu obrazów
    assert image_colored.shape == random_colored_image.shape, "Obrazy muszą mieć takie same wymiary."
    
    # Nakładanie obrazów z kontrolą przezroczystości
    blended_image = (1 - alpha) * image_colored + alpha * random_colored_image
    blended_image = blended_image.astype(np.uint8)  # Konwersja do 8-bitowego obrazu
    
    return blended_image

# Funkcja do rysowania konturów na obrazie
def draw_contours_on_image(image, contours, thickness=3):
    # Upewniamy się, że obraz jest w formacie RGB
    if len(image.shape) < 3 or image.shape[2] != 3:
        image = color.gray2rgb(image)
    
    # Tworzymy kopię obrazu
    image_with_contours = image.copy()
    
    # Generujemy losowy kolor dla każdego konturu
    random_colors = [np.random.randint(0, 256, size=3) for _ in range(len(contours))]
    
    # Iteracja przez kontury i ich punkty
    for contour, color in zip(contours, random_colors):
        for point in contour:
            rr, cc = disk((point[0], point[1]), radius=thickness, shape=image.shape[:2])
            image_with_contours[rr, cc] = color  # Kolor konturu dla danego obiektu
    
    return image_with_contours
    
    return image_with_contours
def draw_centroids_on_image(image, regions, color=(255, 255, 255)):
    # Upewnij się, że obraz jest w formacie RGB
    if len(image.shape) < 3 or image.shape[2] != 3:
        image = color.gray2rgb(image)
    
    # Kopia obrazu
    image_with_centroids = image.copy()
    
    # Iteracja przez regiony i rysowanie centroidów
    for region in regions:
        cy, cx = region.centroid  # Współrzędne centroidu
        rr, cc = disk((cy, cx), radius=5, shape=image.shape[:2])
        image_with_centroids[rr, cc] = color  # Zielony kolor
    
    return image_with_centroids




# Parametry wyświetlania
height = 7
width = 3
hv = 40
wv = 32
dpi = 300
# Otwórz plik PDF do zapisu
fig0, axes0 = plt.subplots(height, width, figsize=(hv, wv), dpi=dpi)
fig1, axes1 = plt.subplots(height, width, figsize=(hv, wv), dpi=dpi)
fig2, axes2 = plt.subplots(height, width, figsize=(hv, wv),dpi=dpi)
fig3, axes3 = plt.subplots(height, width, figsize=(hv, wv),dpi=dpi)
fig4, axes4 = plt.subplots(height, width, figsize=(hv, wv),dpi=dpi)
fig5, axes5 = plt.subplots(height, width, figsize=(hv, wv),dpi=dpi)
fig6, axes6 = plt.subplots(height, width, figsize=(hv, wv),dpi=dpi)
start_nr = 0
end_nr = start_nr + height * width
for i, nr in enumerate(range(start_nr, end_nr, 1)):
    # Wczytaj obraz
    filename = "samolot"
    if nr < 10:
        filename += "0"
    filename += str(nr) + ".jpg"
    image = io.imread("./Lab4_images/" + filename)

    image_contrast = ContrastUp(image)
    bw, binary= thresh_and_median_filter(image_contrast)
    image_closed = closingFunction(binary, disk_size=21)
    image_closed = morphology.dilation(image_closed)
    contours = measure.find_contours(image_closed, 0.5)
    #image_edges = SobelFilter(image_closed)
    image_edges = filters.sobel(image_closed)
    image_colored, regions = ConnectEdges_and_Random_color(image_edges)
    image_output = overlay_random_colors_on_image(image, image_colored)
    image_with_contours = draw_contours_on_image(image, contours)
    image_with_contours = draw_centroids_on_image(image_with_contours, regions)
    image_output = draw_centroids_on_image(image_output, regions)
    
    # Wyświetlenie obrazu
    ax0 = axes0[i // width, i % width]
    ax0.imshow(image_with_contours)
    ax0.axis('off')

    ax1 = axes1[i // width, i % width]
    ax1.imshow(image_contrast)
    ax1.axis('off')

    ax2 = axes2[i // width, i % width]
    ax2.imshow(binary, cmap='gray')
    ax2.axis('off')

    ax3 = axes3[i // width, i % width]
    ax3.imshow(bw, cmap='gray')
    ax3.axis('off')

    ax4 = axes4[i // width, i % width]
    ax4.imshow(image_closed, cmap='gray')
    ax4.axis('off')

    ax5 = axes5[i // width, i % width]
    ax5.imshow(image_edges)
    ax5.axis('off')

    ax6 = axes6[i // width, i % width]
    ax6.imshow(image_output)
    ax6.axis('off')

# Zapis figur do PDF
figures = [fig0, fig1, fig2, fig3, fig4, fig5, fig6]
filenames = ["fig0.pdf", "fig1.pdf", "fig2.pdf", "fig3.pdf", "fig4.pdf", "fig5.pdf", "fig6.pdf"]

save_figures_to_pdf(figures, filenames)
