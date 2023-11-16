import tkinter.messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import simpledialog
from gui_opt import *

# Megnyitom a filet olvasásra
with open("atlageletkor.csv", encoding='ISO-8859-1') as file:
    # Kiolvastatom az összes sort
    lines = file.readlines()
    root = tk.Tk()
    # Ablak méretének beállítása
    root.geometry("800x600")
    #Középrehelyezem az ablakot a képernyőhöz képest a méretet figyelembe véve
    root.eval('tk::PlaceWindow . center')


# Külön választom a megnevezéseket és az adatokat
header = lines[0].strip().split(';')
data_lines = lines[1:]

# Az adatok ellenőrzése, és a vesszők kicserélése pontokra
data = [line.strip().split(';') for line in data_lines]
data = [[cell.replace(',', '.') if cell != '' else '0' for cell in row] for row in data]

# Az "Összesen" sor indexének meghatározása
osszesen_index = [i for i, row in enumerate(data) if row[0] == 'Összesen'][0]

# Minden év adata
for i in range(1, len(header)):
    year = header[i]
    for j in range(1, len(data)):
        if data[j][i] == '':
            data[j][i] = data[osszesen_index][i]

# Évek és minden év adatainak kinyerése
years = header[1:]
allByYear = [row[0] for row in data[1:]]  # Feltételezve, hogy az első oszlop a gyártóneveket tartalmazza

# Létrehozok egy szótárat az adatok tárolásához minden év esetén
data_by_year = {}

# Lista az összes autónak
all_cars = []

# Végigiterálok az éveken, és tárolom az adatokat a szótárban
for year in years:
    # Megkeresem az év indexét a fejlécben
    year_index = header.index(year)

    # Létrehozok egy szótárat az aktuális év adataihoz
    data_for_year = {manufacturer: row[year_index] for manufacturer, row in zip(allByYear, data[1:])}

    # Hozzáadom az "atlag" kulcsot az első adatsorhoz
    data_for_year['atlag'] = data[0][year_index]

    # Eltávolítom a '0': '0' bejegyzést
    data_for_year = {k: v for k, v in data_for_year.items() if k != '0'}

    # Tárolom az adatokat az aktuális évhez a szótárban
    data_by_year[year] = data_for_year

    # Hozzáadom az autókat az összes autó listához
    all_cars.extend(data_for_year.keys())

# Szűröm a duplikátumokat és eltávolítom az üres értékeket
all_cars = list(set(filter(None, all_cars)))
print(all_cars)

# Kiírom az adatokat minden év esetén
for year, data_for_year in data_by_year.items():
    print(f"\nAdatok {year}-re/ra:")
    print(data_for_year)
# Bekérem felhasználótól a gyártót

manufacturer_input = simpledialog.askstring("Gyártó neve", "Adja meg a gyártó nevét az adatok megjelenítéséhez:", parent=root) #Létrehozom az adatbekérő ablakot
years = list(data_by_year.keys())
average_data = [float(data_by_year[year]['atlag'].replace(',', '.')) for year in years]

if manufacturer_input in allByYear:
    print(f"\nAdatok a(z) {manufacturer_input} számára:")
    #for year, data_for_year in data_by_year.items():
    # print(f"{year}: {data_for_year[manufacturer_input]}")
       # manufacturer_data = [float(data_by_year[year][manufacturer_input].replace(',', '.')) for year in years]
    # A Tkinter ablak létrehozása
    root.title(f'{manufacturer_input} átlag életkor alakulása évenként')
    print(f"A grafikon létrehozása a(z) {manufacturer_input} típushoz sikeresen megtörtént")

    # Menüsáv létrehozása
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    options_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fájl", menu=file_menu)
    menubar.add_cascade(label="Művelet", menu=options_menu)
    show_data_submenu = tk.Menu(options_menu, tearoff=0)

    # Kilépés menüpont hozzáadása
    file_menu.add_command(label="Névjegy", command=nevjegy)
    file_menu.add_command(label="Kilépés", command=root.destroy)
    options_menu.add_cascade(label="Adatok megjelenítése évekre lebontva", menu=show_data_submenu)
    # Az évekhez tartozó menüpontok hozzáadása a show_data_submenu részhez
    for year in years:
        show_data_submenu.add_command(label=year, command=lambda y=year: show_data_for_year(y, data_by_year))
    # Matplotlib diagram létrehozása
    fig, ax = plt.subplots()

    # Adatok előkészítése
    manufacturer_data = [float(data_by_year[year][manufacturer_input].replace(',', '.')) for year in years]
    ax.plot(years, average_data, label='Átlag')
    ax.plot(years, manufacturer_data, label=manufacturer_input)

    # Jelmagyarázat hozzáadása
    or_patch = mpatches.Patch(color='orange', label='Évek szerinti adat')
    bl_patch = mpatches.Patch(color='blue', label='Átlag')
    ax.legend(handles=[or_patch, bl_patch])

    # Diagram címe és tengelynevek
    ax.set_title(f'{manufacturer_input} átlag életkor alakulása évenként')
    ax.set_xlabel('Év')
    ax.set_xticks(years)
    ax.set_xticklabels([f"'{str(year)[-2:]}" for year in years])
    ax.set_ylabel('Életkor')

    # Matplotlib diagram beágyazása a Tkinter ablakba
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # Navigációs eszköztár hozzáadása
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas_widget.pack()
    # Tkinter főciklus indítása
    tk.mainloop()
else:
    print(f"\nNincs adat a(z) {manufacturer_input} számára.") # Konzolban is kiírja a hibát
    tkinter.messagebox.showerror(title=f"Nincs adat - {manufacturer_input}", message=f"\nNincs adat a(z) {manufacturer_input} számára.") # Kijelzem a hibát egy error ablakban ha nincs adat
