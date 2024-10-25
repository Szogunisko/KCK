import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb, rgb_to_hsv

# Tworzenie niestandardowego gradientu
colors = [(0, (0, 1, 0)), (0.5, (1, 1, 0)), (1, (1, 0, 0))]
custom_cmap = LinearSegmentedColormap.from_list("CustomGradient", colors)

# Wczytaj dane z pliku
file_path = 'big.dem.txt'  # Zastąp własną ścieżką do pliku
with open(file_path, 'r') as file:
    w, h, distance = map(float, file.readline().strip().split())
    w, h = int(w), int(h)
    height_map = []
    for _ in range(h):
        row = list(map(float, file.readline().strip().split()))
        height_map.append(row)
    height_map = np.array(height_map)

# Definiowanie stałego wektora światła
light_vector = np.array([-1, -1, 1])
light_vector = light_vector / np.linalg.norm(light_vector)

# Obliczanie gradientów wysokości w kierunku x i y
dx, dy = np.gradient(height_map)

# Obliczenie wektora normalnego dla każdego punktu
dz = distance / 100.0
normals = np.dstack((-dx, -dy, np.ones_like(height_map) * dz))
norms = np.linalg.norm(normals, axis=2)
normals /= norms[:, :, np.newaxis]

# Obliczenie kąta między wektorem światła a normalnym
cos_angle = np.einsum('ijk,k->ij', normals, light_vector)
shade_factor = ((cos_angle - cos_angle.min()) / (cos_angle.max() - cos_angle.min())) ** 0.6

# Stosowanie gradientu HSV
colored_height_map = custom_cmap((height_map - height_map.min()) / (height_map.max() - height_map.min()))
hsv_map = rgb_to_hsv(colored_height_map[:, :, :3])

# Dostosowanie saturacji (S) i jasności (V)
hsv_map[:, :, 1] = np.clip(hsv_map[:, :, 1]*1.5, 0, 1)  # Zwiększenie saturacji o 50%
hsv_map[:, :, 2] *= (shade_factor*1.3)  # Zwiększenie jasności o 30%

# Konwersja z powrotem do RGB
shaded_map = hsv_to_rgb(hsv_map)

# Wyświetlanie wyniku
plt.figure(figsize=(10, 8))
plt.imshow(shaded_map, interpolation='nearest')
plt.colorbar(label="Wysokość (m)")
plt.title("Mapa wysokości terenu z intensywnym kolorowaniem i cieniowaniem")
plt.xlabel("Szerokość (w punktach)")
plt.ylabel("Wysokość (h punktach)")
plt.show()
