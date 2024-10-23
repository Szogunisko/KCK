import numpy as np
import matplotlib.pyplot as plt
import csv

#Ustawienei czcionki
plt.rc('font', family='serif', serif='Times New Roman')

#funkcja do wczytywania danych z plików csv
def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = np.array(data)
    data = np.array(data[1:], dtype=float)
    x = data[:,1]
    y = np.mean(data[:, 2:], axis=1)
    return x, y, data

# Wczytanie danych z plików csv
x1, y1, data_rsel = read_csv('results/rsel.csv') # Dane dla 1-Evol_RS
x2, y2, data_cel_rs = read_csv('results/cel-rs.csv') # Dane dla 1-Coev_RS
x3, y3, data_2cel_rs = read_csv('results/2cel-rs.csv') # Dane dla 2-Coev_RS
x4, y4 , data_cel= read_csv('results/cel.csv') # Dane dla 1-Coev
x5, y5, data_2cel = read_csv('results/2cel.csv') # Dane dla 2-Coev

# Stworzenie pola z dwoma wykresami: jeden wiersz, dwie kolumny, szerokosc i wysokosc w calach
fig, (ax1, box1) = plt.subplots(1, 2, figsize=(6.7, 5))

# Pierwszy wykres liniowy z markerami
ax1.plot(x1/1000, y1*100, label='1-Evol-RS', color='blue', marker='o', markevery=25, markeredgecolor = 'black', markeredgewidth=0.5,alpha=0.8,linewidth=0.75)
ax1.plot(x2/1000, y2*100, label='1-Coev-RS', color='green', marker='v', markevery=25, markeredgecolor = 'black', markeredgewidth=0.5,alpha=0.8,linewidth=0.75)
ax1.plot(x3/1000, y3*100, label='2-Coev-RS', color='red', marker='D', markevery=25, markeredgecolor = 'black', markeredgewidth=0.5,alpha=0.8,linewidth=0.75)
ax1.plot(x4/1000, y4*100, label='1-Coev', color='black', marker='s', markevery=25, markeredgecolor = 'black', markeredgewidth=0.5,alpha=0.8,linewidth=0.75)
ax1.plot(x5/1000, y5*100, label='2-Coev', color='magenta', marker='d', markevery=25, markeredgecolor = 'black', markeredgewidth=0.5,alpha=0.8,linewidth=0.75)
ax1.set_xlim(0,500)
ax1.set_ylim(60,100)
ax1.tick_params(axis='x', direction='in', length=3)
ax1.tick_params(axis='y', direction='in', length=3)
#ustawienie znacznikow y po dwóch stronach
ax1.yaxis.set_ticks_position('both')
ax1.set_xlabel('Rozegranych gier (×1000)')
ax1.set_ylabel('Odsetek wygranych gier [%]')
ax1.grid(linestyle = '--', linewidth=0.25, dashes=(7, 14))
ax1.legend(loc='lower right', numpoints=2)

ax2 = ax1.twiny()
ax2.set_xlim(0,200)
#usuniecie zewnetrznych znacznikow
ax2.tick_params(axis='x', direction='in', length=3)
ax2.tick_params(axis='y', direction='in', length=3)
top_x = np.linspace(0, 200, 40)
ax2.set_xticks(np.arange(0, 201, 40))
ax2.set_xlabel('Pokolenie')


# Dane do boxplota
boxplot_data = [
    data_rsel[-1, 2:]*100,   
    data_cel_rs[-1, 2:]*100, 
    data_2cel_rs[-1, 2:]*100,
    data_cel[-1, 2:]*100,    
    data_2cel[-1, 2:]*100   
]

# Ustawienia wykresu pudełkowego
box1.boxplot(boxplot_data, showmeans=True,patch_artist=True,
            notch=True, 
            showfliers=True,
            boxprops=dict(linewidth=1, edgecolor='blue',facecolor='none', color='blue', zorder=-1),
            whiskerprops=dict(linewidth=1, color='blue', linestyle='--', dashes=(5,6)),
            medianprops=dict(color='red', zorder=7),
            flierprops=dict(marker='+', markeredgecolor='blue', markersize=5),
            meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='blue', markersize=5, zorder=-2),
)

#Notch -> wyciecie
#Fliers -> wartosci odstajace
#Whisker -> wąsy
#Mediana ->mediana
#Mean -> średnia

# Ustawienia osi wykresu pudełkowego
box1.set_xticklabels(['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev'], rotation=20)
box1.set_ylim(60, 100)
box1.tick_params(axis='x', direction='in', length=3)
box1.tick_params(axis='y', direction='in', length=3)
box1.xaxis.set_ticks_position('both')
box1.yaxis.tick_right()
box1.grid(linestyle = '--', linewidth=0.25, dashes=(7, 14))


#ZAPIS DO PDF i Dopasowanie
plt.tight_layout()
plt.savefig('wykres.pdf')
plt.show()
