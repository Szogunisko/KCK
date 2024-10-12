import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D

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

# Create a figure with two subplots (one row, two columns)
fig, (ax1, box1) = plt.subplots(1, 2, figsize=(6.7, 4.7))

# Plot the first line chart (on the left)
line1, = ax1.plot(x11/1000, y1*100, label='1-Evol-RS', color='blue', marker='o', markevery=25)
ax1.plot(x21/1000, y2*100, label='1-Coev-RS', color='green', marker='v', markevery=25)
ax1.plot(x31/1000, y3*100, label='2-Coev-RS', color='red', marker='D', markevery=25)
ax1.plot(x41/1000, y4*100, label='1-Coev', color='black', marker='s', markevery=25)
ax1.plot(x51/1000, y5*100, label='2-Coev', color='magenta', marker='d', markevery=25)
ax1.set_xlim(0,500)
ax1.set_ylim(60,100)
plt.margins(x=0, y=0)
ax1.set_xlabel('Rozegranych gier (x1000)')
ax1.set_ylabel('Odsetek wygranych gier [%]')
ax1.grid(linestyle = '--')
ax1.legend(loc='lower right', handler_map={line1: HandlerLine2D(numpoints=2)})

#TUTEJ
ax2 = ax1.twiny()
ax2.set_xlim(0,200)
top_x = np.linspace(0, 200, 40)
ax2.set_xticks(np.arange(0, 201, 40))
ax2.set_xlabel('Pokolenie')


# Create the boxplot on the second subplot (on the right)
data_boxplot = [y1,y2,y3,y4,y5]
box1.boxplot(data_boxplot, notch=True, showmeans=True, patch_artist=False)

# Add labels and grid to the second plot
box1.set_xticklabels(['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev'])
box1.set_ylabel('Odsetek wygranych gier [%]')
box1.grid(True)
box1.set_title('Porównanie odsetku wygranych gier')

# Adjust layout and show the plots
plt.rc('font', family='serif', serif='Times New Roman')
plt.tight_layout()
plt.savefig('combined_plot.pdf')
plt.show()
