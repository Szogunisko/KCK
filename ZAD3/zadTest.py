from skimage import io, color, measure, morphology, exposure, filters
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from skimage.color import rgb2gray
from skimage.filters.edges import convolve
from skimage import img_as_ubyte
from skimage.segmentation import find_boundaries

# Funkcja progowania, zamknięcia i filtracji medianowej
def thresh_with_closing_and_median_filter(image, t, disk_size=5):
    # Konwersja do skali szarości
    image = rgb2gray(image) * 255
    image = image.astype(np.uint8)
    
    # Zastosowanie filtra medianowego do wygładzenia obrazu
    image_filtered = filters.median(image, morphology.disk(disk_size))
    
    # Binaryzacja po filtracji medianowej
    binary = np.where(image_filtered > t, 0, 255).astype(np.uint8)
    
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
        color = np.random.randint(100, 256, size=3)
        color_image[mask] = color
    
    return color_image

# Lista pomijanych numerów zdjęć
skip_images = {6, 18, 19}

# Parametry wyświetlania
height = 3
width = 7

# Otwórz plik PDF do zapisu
with PdfPages("wynik_samoloty.pdf") as pdf:
    fig, axes = plt.subplots(height, width, figsize=(16, 12))

    start_nr = 0
    end_nr = start_nr + height * width
    for i, nr in enumerate(range(start_nr, end_nr, 1)):
        # Pomijanie wybranych obrazów
        if nr in skip_images:
            continue

        # Wczytaj obraz
        filename = "samolot"
        if nr < 10:
            filename += "0"
        filename += str(nr) + ".jpg"
        image = io.imread("./Lab4_images/" + filename)
        intensityP = 5
        intensityK = 28
        pp, pk = np.percentile(image, (intensityP, intensityK))
        image = exposure.rescale_intensity(image, in_range=(pp, pk))
        
        # Przetwarzanie z progowaniem, zamknięciem i medianą
        boundaries, labeled_image = thresh_with_closing_and_median_filter(image, 126, disk_size=3)
        
        # Zastosuj losowe kolory do każdego obiektu
        color_image = apply_random_colors(boundaries, labeled_image)
        
        # Wyświetlenie obrazu
        ax = axes[i // width, i % width]
        ax.imshow(color_image)
        ax.axis('off')

    # Dopasowanie układu figur
    plt.tight_layout()
    # Dodaj całą figurę do pliku PDF
    pdf.savefig(fig)
    plt.close(fig)
