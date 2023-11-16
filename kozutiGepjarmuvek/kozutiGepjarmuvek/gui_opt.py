import tkinter as tk
from tkinter import font
import tkinter.simpledialog as simpledialog


def nevjegy():
    ablak = tk.Toplevel() # Ablak incializálása a főablak (root) mellett
    ablak.title("Névjegy - KSH") # Felugró ablak címe

    félkövér_font = font.Font(weight="bold") # Félkövér betűtípus tárolása
    dolt_font = font.Font(slant="italic") # Dölt betűtípus tárolása


    félkövér_szoveg = "A projekt készítői"
    nevek = "Szabó Brigitta Berta - NeptKód - Projektvezető\nRéz Levente László - RTL7JM - Fejlesztő\nNemoda Márk Levente - BPBYJZ - Fejlesztő\nPethő Máté - NeptKód - Fejlesztő\nPádár Patrik - NeptKód - Fejlesztő"
    keszult = ('A Projekt a központi Statisztikai hivatal 24.1.1.26 "A személygépkocsi-állomány átlagos kora gyártmányok szerint" kimutatása alapján készült!')
    teljes_szoveg = f"{félkövér_szoveg}\n\n{nevek}"

    szoveg_label = tk.Label(ablak, text=teljes_szoveg, font=félkövér_font) # Szöveg megjelenítése félkövéren
    keszult_label = tk.Label(ablak, text=keszult, font=dolt_font) # Szöveg megjelenítése dölten
    keszult_label.pack(padx=20, pady=20) # Margók a keszult szöveghez
    szoveg_label.pack(padx=20, pady=20) # Margók a teljes_szoveg-hez

def show_data_for_year(year, data_by_year):
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


