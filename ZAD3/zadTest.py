import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters, feature, measure, morphology

# Wczytaj obraz
filename = 'samolot01.jpg'  # Upewnij się, że ścieżka do obrazu jest poprawna
image = io.imread("./Lab4_images/" + filename)

# Konwertuj obraz do skali szarości
gray_image = color.rgb2gray(image)

# Użyj filtra Canny'ego do wykrycia krawędzi
edges = feature.canny(gray_image, sigma=2.0)

# Opcjonalnie, można wykonać operację morfologiczną, aby poprawić wynik (zamykanie)
edges = morphology.binary_closing(edges, morphology.disk(3))

# Znajdź kontury na podstawie krawędzi
contours = measure.find_contours(edges, level=0.8)

# Wyświetl oryginalny obraz oraz obraz z nałożonymi konturami
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(image)
ax[0].set_title('Oryginalny obraz')
ax[0].axis('off')

# Wyświetl obraz z konturami
ax[1].imshow(gray_image, cmap='gray')
for contour in contours:
    ax[1].plot(contour[:, 1], contour[:, 0], linewidth=0.8, color='red')
ax[1].set_title('Kontury samolotów')
ax[1].axis('off')

plt.show()
