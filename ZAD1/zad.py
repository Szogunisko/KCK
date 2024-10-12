import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

# Dane dla 1-Evol-RS

with open('results/rsel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1)
x11 = data_array[:,1]
x12= data_array[:,0]
y1 = data_y

# Dane dla 1-Coev_RS
with open('results/cel-rs.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1)
x21 = data_array[:,1]
x22= data_array[:,0]
y2 = data_y
# Dane dla 2-Coev_RS
with open('results/2cel-rs.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1) 
x31 = data_array[:,1]
x32= data_array[:,0]
y3 = data_y
# Dane dla 1-Coev
with open('results/cel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1)
x41 = data_array[:,1]
x42= data_array[:,0]
y4 = data_y
# Dane dla 2-Coev
with open('results/2cel.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
data_array = np.array(data)
data_array = np.array(data_array[1:], dtype=float)
data_y = np.mean(data_array[:, 2:], axis=1)
x51 = data_array[:,1]
x52= data_array[:,0]
y5 = data_y # Przykładowe dane dla 1-Evol-RS

# Tworzenie wykresu

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.7, 5))  # 1 wiersz, 2 kolumny
ax1.plot(x11, y1, label='1-Evol-RS', color='blue', marker='o', markevery=25)
ax1.plot(x21, y2, label='1-Coev-RS', color='green', marker='v', markevery=25)
ax1.plot(x31, y3, label='2-Coev-RS', color='red', marker='D', markevery=25)
ax1.plot(x41, y4, label='1-Coev', color='black', marker='s', markevery=25)
ax1.plot(x51, y5, label='2-Coev', color='magenta', marker='d', markevery=25)
ax1.set_xlabel('Rozegranych gier')
ax1.set_ylabel('Odsetek wygranych gier')
ax1.grid(linestyle = '--')
ax1.legend(loc='lower right')



plt.savefig('myplot.pdf')
plt.show()
