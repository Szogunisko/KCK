import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb, rgb_to_hsv

# Tworzenie niestandardowego gradientu koloru: Zielony -> Żółty -> Czerwony
colors = [(0, (0, 1, 0)), (0.5, (1, 1, 0)), (1, (1, 0, 0))]
custom_cmap = LinearSegmentedColormap.from_list("CustomGradient", colors)

# Wczytaj dane z pliku DEM
file_path = 'big.dem.txt'  # Zastąp własną ścieżką do pliku
with open(file_path, 'r') as file:
    # Pierwsza linia pliku zawiera szerokość, wysokość i odległość
    w, h, distance = map(float, file.readline().strip().split())
    w, h = int(w), int(h)  # Przekształcenie szerokości i wysokości na int
    # Wczytaj wartości wysokości jako tablicę 2D
    height_map = np.array([list(map(float, file.readline().strip().split())) for _ in range(h)])

# Definiowanie wektora światła
light_vector = np.array([-1, -1, 1])
light_vector = light_vector / np.linalg.norm(light_vector)

# Obliczanie gradientów wysokości w kierunkach x i y
dx, dy = np.gradient(height_map)

# Tworzenie wektorów normalnych dla każdego punktu
normals = np.dstack((-dx, -dy, np.ones_like(height_map) * distance))
normals /= np.linalg.norm(normals, axis=2, keepdims=True)  # Normalizacja normalnych

# Obliczenie współczynnika cienia (cosinus kąta między światłem a normalnymi)
cos_angle = np.clip(np.sum(normals * light_vector, axis=2), 0, 1)  # Obcięcie do zakresu [0, 1]
shade_factor = ((cos_angle - cos_angle.min()) / (cos_angle.max() - cos_angle.min())) ** 0.6

# Stosowanie niestandardowego gradientu do mapy wysokości
colored_height_map = custom_cmap((height_map - height_map.min()) / (height_map.max() - height_map.min()))

# Konwersja RGB do HSV w celu manipulacji kolorami
hsv_map = rgb_to_hsv(colored_height_map[:, :, :3])

# Zwiększenie saturacji i zastosowanie współczynnika cienia do jasności
hsv_map[:, :, 1] *= np.clip(hsv_map[:, :, 1] ** 2, 0, 1)  # Zwiększenie saturacji
hsv_map[:, :, 2] *= np.clip(shade_factor * 1.25, 0, 1)  # Zastosowanie cienia i zwiększenie jasności

# Konwersja mapy z powrotem do RGB po zmianach w HSV
shaded_map = hsv_to_rgb(hsv_map)

# Wyświetlanie wyniku
plt.figure(figsize=(10, 8))
plt.imshow(shaded_map)
plt.title("Mapa wysokości terenu z intensywnym kolorowaniem i cieniowaniem")
plt.xlabel("Szerokość (w punktach)")
plt.ylabel("Wysokość (w punktach)")
plt.show()
