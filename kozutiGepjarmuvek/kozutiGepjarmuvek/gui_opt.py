import tkinter as tk
from tkinter import font

def nevjegy():
    ablak = tk.Toplevel()
    ablak.title("Névjegy - KSH")

    félkövér_font = font.Font(weight="bold")

    félkövér_szoveg = "A projekt készítői."
    nevek = "Szabó Brigitta Berta\nRéz Levente László\nNemoda Márk Levente\nPethő Máté\nPádár Patrik"

    teljes_szoveg = f"{félkövér_szoveg}\n\n{nevek}"

    szoveg_label = tk.Label(ablak, text=teljes_szoveg, font=félkövér_font)
    szoveg_label.pack(padx=20, pady=20)
