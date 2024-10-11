#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import csv

# Dane dla 1-Evol-RS
with open('results/rsel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
y1 = data_y

# Dane dla 1-Coev_RS
with open('results/cel-rs.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
y2 = data_y

# Dane dla 2-Coev_RS
with open('results/2cel-rs.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
y3 = data_y

# Dane dla 1-Coev
with open('results/cel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
y4 = data_y

# Dane dla 2-Coev
with open('results/2cel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
y5 = data_y # Przykładowe dane dla 1-Evol-RS

# X obojętnie bo wszedzie sa te same 0-500tys
x1 = data_array[:,1]
x2= data_array[:,0]
x_dolna = x1  # Rozegrane gry



# Tworzenie wykresu
fig, ax1 = plt.subplots()
# Wykres dla 1-Evol-RS
ax1.plot(x_dolna, y1, 'b-o', label='1-Evol-RS', markersize=5)
# Wykres dla 1-Coev-RS
ax1.plot(x_dolna, y2, 'g-v', label='1-Coev-RS', markersize=5)
# Wykres dla 2-Coev-RS
ax1.plot(x_dolna, y3, 'r-D', label='2-Coev-RS', markersize=5)
# Wykres dla 1-Coev
ax1.plot(x_dolna, y4, 'k-s', label='1-Coev', markersize=5)
# Wykres dla 2-Coev
ax1.plot(x_dolna, y5, 'm-d', label='2-Coev', markersize=5)

# Oś X dolna
ax1.set_xlabel('Rozegranych gier')
ax1.set_ylabel('Odsetek wygranych gier')

# Siatka
ax1.grid(True)

# Legenda
ax1.legend(loc='best')
plt.show()
