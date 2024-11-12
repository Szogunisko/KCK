from skimage import io, color, measure, morphology
from matplotlib import pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from skimage.filters.edges import convolve
from skimage import img_as_ubyte
from skimage.segmentation import find_boundaries

# Funkcja progowania, zamknięcia i wykrywania krawędzi w pionie i poziomie
def thresh_with_closing_and_edge_detection(image, t):
    # Konwersja do skali szarości
    image = rgb2gray(image) * 255
    image = image.astype(np.uint8)
    
    # Binaryzacja
    binary = np.where(image > t, 0, 255).astype(np.uint8)
    
    # Operacja zamknięcia
    selem = morphology.disk(5)
    closed_image = morphology.closing(binary, selem)
    
    # Filtr Sobela dla krawędzi pionowych i poziomych
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])
    
    # Konwolucja w kierunku poziomym i pionowym
    edges_x = convolve(closed_image, sobel_x)
    edges_y = convolve(closed_image, sobel_y)
    
    # Łączenie krawędzi
    edges = np.sqrt(edges_x**2 + edges_y**2)
    edges = (edges - edges.min()) / (edges.max() - edges.min()) * 255
    edges = edges.astype(np.uint8)
    
    # Etykietowanie samolotów
    labeled_image = measure.label(edges > 0, connectivity=2)
    
    # Znajdowanie konturów każdego samolotu
    boundaries = find_boundaries(labeled_image, mode='outer')
    
    return boundaries, labeled_image

# Funkcja do generowania losowych kolorów dla każdego obiektu
def apply_random_colors(boundaries, labeled_image):
    # Przygotowanie pustego obrazu RGB
    color_image = np.zeros((*boundaries.shape, 3), dtype=np.uint8)
    
    # Przypisywanie losowych kolorów każdemu obiektowi
    for label in np.unique(labeled_image):
        if label == 0:
            continue  # pomiń tło
        mask = labeled_image == label
        color = np.random.randint(0, 255, size=3)  # losowy kolor RGB
        color_image[mask] = color
    
    return color_image

# Parametry wyświetlania
height = 4
width = 5
fig, axes = plt.subplots(height, width, figsize=(15, 10))

start_nr = 1
end_nr = start_nr + height * width
for i, nr in enumerate(range(start_nr, end_nr, 1)):
    # Wczytaj obraz
    filename = "samolot"
    if nr < 10:
        filename += "0"
    filename += str(nr) + ".jpg"
    image = io.imread("./Lab4_images/" + filename)
    
    # Przetwarzanie z progowaniem, zamknięciem i wykrywaniem krawędzi
    boundaries, labeled_image = thresh_with_closing_and_edge_detection(image, 120)
    
    # Zastosuj losowe kolory do każdego obiektu
    color_image = apply_random_colors(boundaries, labeled_image)
    
    # Wyświetlenie obrazu
    axes[i // width, i % width].imshow(color_image)
    axes[i // width, i % width].axis('off')

plt.tight_layout()
plt.show()
