from packages import *
import numpy as np
from sklearn.linear_model import LinearRegression

def nevjegy():
    ablak = tk.Toplevel() # Ablak incializálása a főablak (root) mellett
    ablak.title("Névjegy - KSH") # Felugró ablak címe
    felkover_font = tk.font.Font(weight="bold")
    dolt_font = tk.font.Font(slant="italic") # Dölt betűtípus tárolása
    felkover_szoveg = "A projekt készítői"
    nevek = "Szabó Brigitta Berta - PBJJXL - Projektvezető\nRéz Levente László - RTL7JM - Fejlesztő\nNemoda Márk Levente - BPBYJZ - Fejlesztő\nPethő Máté - JK8H85 - Fejlesztő\nPádár Patrik - GT6MXC - Fejlesztő"
    keszult = ('A Projekt a központi Statisztikai hivatal 24.1.1.26 "A személygépkocsi-állomány átlagos kora gyártmányok szerint" kimutatása alapján készült!')
    teljes_szoveg = f"{felkover_szoveg}\n\n{nevek}"

    szoveg_label = tk.Label(ablak, text=teljes_szoveg, font=felkover_font) # Szöveg megjelenítése félkövéren
    keszult_label = tk.Label(ablak, text=keszult, font=dolt_font) # Szöveg megjelenítése dölten
    keszult_label.pack(padx=20, pady=20) # Margók a keszult szöveghez
    szoveg_label.pack(padx=20, pady=20) # Margók a teljes_szoveg-hez

def evekre_bont(year, data_by_year):
    if year and year in data_by_year:
        data_for_year = data_by_year[year]

        # A Tkinter ablak létrehozása
        table_window = tk.Toplevel() # Ablak incializálása a főablak (root) mellett
        table_window.title(f'Adatok {year}-re/ra') # Felugró ablak címe
        table_window.geometry("430x720") # Felugró ablak mérete

        # Szöveges widget létrehozása
        text_widget = tk.Text(table_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill='both')

        # Adatok kiírása 2 oszlopban
        text_widget.insert(tk.END, f"{'Gyártó': <20}{'Életkor'}\n")
        text_widget.insert(tk.END, '─' * 30 + '\n')
        for manufacturer, value in data_for_year.items():
            text_widget.insert(tk.END, f"{manufacturer: <20}{value}\n")
        text_widget.insert(tk.END, '─' * 30 + '\n')
        # Adatok szerkesztésének tiltása
        text_widget.config(state=tk.DISABLED)
    else:
        print(f"\nNincs adat a(z) {year} évhez.")
        tk.messagebox.showerror(title=f"Nincs adat - {year}",  message=f"\nNincs adat a(z) {year} számára.")  # Kijelzem a hibát egy error ablakban ha nincs adat


def regresszio(x, y):
    # Adatokat konvertáljuk numerikus értékké
    x = np.array(x, dtype='float').reshape(-1, 1)
    y = np.array(y, dtype='float')
    model = LinearRegression().fit(x, y)   # Létrehozzuk a regressziós modellt
    y_pred = model.predict(x)     # Meghatározzuk előzetesen az x értékeket / értékeket
    return y_pred, model.coef_[0], model.intercept_   # Visszatérünk a meghatározott adattal

def osszatlag(data_by_year):
    average = tk.Tk()
    average.title("Összesített Átlag Diagram")

    # Adatok előkészítése
    years = list(data_by_year.keys())
    average_data = [float(data_by_year[year]['atlag'].replace(',', '.')) for year in years]

    # Matplotlib diagram létrehozása
    fig, ax = plt.subplots()

    # Adatok hozzáadása a diagramhoz
    ax.plot(years, average_data, label='Összesített Átlag', color="green")
    ax.scatter(years, average_data, color="green", marker='o')
    ax.legend()

    # Diagram címe és tengelynevek
    ax.set_title('Összesített Átlag életkor alakulása')
    ax.set_xlabel('Év')
    ax.set_xticks(years)
    ax.set_xticklabels([f"'{str(year)[-2:]}" for year in years])
    ax.set_ylabel('Átlag életkor')

    # Matplotlib diagram beágyazása a Tkinter ablakba
    canvas = FigureCanvasTkAgg(fig, master=average)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Navigációs eszköztár hozzáadása (opcionális)
    toolbar = NavigationToolbar2Tk(canvas, average)
    toolbar.update()
    canvas_widget.pack()
    average.mainloop()

def resetw(root):
    # Az ablak eredeti méretének beállítása
    root.geometry("800x600")  # ablak eredeti mérete
    root.eval('tk::PlaceWindow . center')  # Középrehelyezem az ablakot a képernyőhöz képest a méretet figyelembe véve