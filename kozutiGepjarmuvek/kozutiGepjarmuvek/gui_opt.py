import tkinter as tk
from tkinter import font
import tkinter.simpledialog as simpledialog


def nevjegy():
    ablak = tk.Toplevel()
    ablak.title("Névjegy - KSH")

    félkövér_font = font.Font(weight="bold")
    dolt_font = font.Font(slant="italic")


    félkövér_szoveg = "A projekt készítői"
    nevek = "Szabó Brigitta Berta - NeptKód - Projektvezető\nRéz Levente László - RTL7JM - Fejlesztő\nNemoda Márk Levente - BPBYJZ - Fejlesztő\nPethő Máté - NeptKód - Fejlesztő\nPádár Patrik - NeptKód - Fejlesztő"
    keszult = ('A Projekt a központi Statisztikai hivatal 24.1.1.26 "A személygépkocsi-állomány átlagos kora gyártmányok szerint" kimutatása alapján készült!')
    teljes_szoveg = f"{félkövér_szoveg}\n\n{nevek}"

    szoveg_label = tk.Label(ablak, text=teljes_szoveg, font=félkövér_font)
    keszult_label = tk.Label(ablak, text=keszult, font=dolt_font)
    keszult_label.pack(padx=20, pady=20)
    szoveg_label.pack(padx=20, pady=20)

def show_data_for_year(year, data_by_year):
    if year and year in data_by_year:
        data_for_year = data_by_year[year]

        # A Tkinter ablak létrehozása
        table_window = tk.Toplevel()
        table_window.title(f'Adatok {year}-re/ra')
        table_window.geometry("840x760")

        # Szöveges widget létrehozása
        text_widget = tk.Text(table_window, wrap=tk.WORD)
        text_widget.pack(expand=True, fill='both')

        # Adatok táblázatos formátumban
        text_widget.insert(tk.END, f"{'Gyártó': <20}{'Életkor'}\n")
        text_widget.insert(tk.END, '-' * 30 + '\n')
        for manufacturer, value in data_for_year.items():
            text_widget.insert(tk.END, f"{manufacturer: <20}{value}\n")

        # Tilos a szerkesztés
        text_widget.config(state=tk.DISABLED)
    else:
        print(f"\nNincs adat a(z) {year} évhez.")

