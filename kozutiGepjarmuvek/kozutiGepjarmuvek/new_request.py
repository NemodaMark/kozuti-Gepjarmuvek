from packages import *

# Új lekérés indítása
def newkeres(root):
    root.destroy() # Törlöm a korábbi adatokat a képernyőről
    with open("atlageletkor.csv", encoding='ISO-8859-1') as file:
        # Kiolvastatom az összes sort
        lines = file.readlines()
        root = tk.Tk()
        root.geometry("800x600")  # Ablak méretének fixálása
        #  root.iconbitmap(default='appicon.ico') # Program ikon beállítása
        root.eval(
            'tk::PlaceWindow . center')  # Középrehelyezem az ablakot a képernyőhöz képest a méretet figyelembe véve

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
  #  print(all_cars)

    # Kiírom az adatokat minden év esetén
    #for year, data_for_year in data_by_year.items():
    #    print(f"\nAdatok {year}-re/ra:")
    #    print(data_for_year)
    # Bekérem felhasználótól a gyártót

    manufacturer_input = simpledialog.askstring("Gyártó neve", "Adja meg a gyártó nevét az adatok megjelenítéséhez:",
                                                parent=root)  # Létrehozom az adatbekérő ablakot
    years = list(data_by_year.keys())
    average_data = [float(data_by_year[year]['atlag'].replace(',', '.')) for year in years]

    if manufacturer_input in allByYear:
     #   print(f"\nAdatok a(z) {manufacturer_input} számára:")
        # for year, data_for_year in data_by_year.items():
        # print(f"{year}: {data_for_year[manufacturer_input]}")
        # manufacturer_data = [float(data_by_year[year][manufacturer_input].replace(',', '.')) for year in years]
        # A Tkinter ablak létrehozása
        root.title(f'{manufacturer_input} átlag életkor alakulása évenként')  # Az ablak címe
       # print(
        #    f"A grafikon létrehozása a(z) {manufacturer_input} típushoz sikeresen megtörtént")  # Konzolban jelzem a generálás sikerességét

        # Menüsáv létrehozása
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)  # Fájl menü incializálása
        options_menu = tk.Menu(menubar, tearoff=0)  # Művelet menü incializálása
        version_menu = tk.Menu(menubar, tearoff=0)  # Verzió menü incializálása
        window_menu = tk.Menu(menubar, tearoff=0)  # Ablak menü hozzáadása
        menubar.add_cascade(label="Fájl", menu=file_menu)  # Fájl menü megjelenítése
        menubar.add_cascade(label="Ablak", menu=window_menu)
        menubar.add_cascade(label="Művelet", menu=options_menu)  # Művelet menü megjelenítése
        menubar.add_cascade(label="Ver. 1.22",
                            menu=version_menu)  # Verzió menü megjelenítése (Ezzel iratjuk ki verziószámot)
        show_data_submenu = tk.Menu(options_menu, tearoff=0)  # Almenü létrehozása a művelet fülön belül
        # Menüpontok hozzáadása a fejléchez
        window_menu.add_command(label="Visszaállítás", command=lambda: resetw(root))
        file_menu.add_command(label="Projektről", command=projektrol)
        file_menu.add_command(label="Névjegy", command=nevjegy)
        file_menu.add_command(label="Kilépés", command=root.destroy)
        # Almenük beépítése
        options_menu.add_command(label="Új lekérés", command=lambda: newkeres(root))
        options_menu.add_command(label="Összesített Átlagdiagram", command=lambda: osszatlag(data_by_year))
        options_menu.add_cascade(label="Adatok megjelenítése évekre lebontva", menu=show_data_submenu)
        # Az évekhez tartozó menüpontok hozzáadása a show_data_submenu részhez
        for year in years:
            show_data_submenu.add_command(label=year, command=lambda y=year: evekre_bont(y, data_by_year))
        fig, ax = plt.subplots()  # Matplotlib diagram létrehozása

        # Adatok előkészítése
        manufacturer_data = [float(data_by_year[year][manufacturer_input].replace(',', '.')) for year in years]
        ax.plot(years, average_data, label='Átlag')
        ax.plot(years, manufacturer_data, label=manufacturer_input)
        ax.scatter(years, manufacturer_data, color="orange", marker='o', label="Pontdiagram")
        y_pred, slope, intercept = regresszio(years, manufacturer_data)
        ax.plot(years, y_pred, color='red', linestyle='--', label='Lineáris regresszió')
        # Jelmagyarázat hozzáadása
        or_patch = mpatches.Patch(color='orange',
                                  label='Évek szerinti adat')  # Narancssárga (Évi bontású) jelmagyarázat
        bl_patch = mpatches.Patch(color='blue', label='Átlag')  # Kék (Átlag) jelmagyarázat
        red_patch = mpatches.Patch(color='red', label='Regressziós görbe')  # Piros (Regressziós) jelmagyarázat
        ax.legend(handles=[or_patch, bl_patch, red_patch])

        # Diagram címe és tengelynevek
        ax.set_title(f'{manufacturer_input} átlag életkor alakulása évenként')
        ax.set_xlabel('Év')
        ax.set_xticks(years)  # X-tengelyen évek jelennek meg
        ax.set_xticklabels([f"'{str(year)[-2:]}" for year in
                            years])  # Levágjuk az évszám utolsó két karakterét, és az elején hozzáfűzünk egy aposztrófot
        ax.set_ylabel('Életkor')

        canvas = FigureCanvasTkAgg(fig, master=root)  # diagram beágyazása a főablakba
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Navigációs eszköztár hozzáadása
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas_widget.pack()
        # Tkinter főciklus indítása
        mplcursors.cursor(hover=True)
        tk.mainloop()
    else:
      #  print(f"\nNincs adat a(z) {manufacturer_input} számára.")  # Konzolban is kiírja a hibát
        tkinter.messagebox.showerror(title=f"Nincs adat - {manufacturer_input}",
                                     message=f"\nNincs adat a(z) {manufacturer_input} számára.")  # Kijelzem a hibát egy error ablakban ha nincs adat
        root.destroy()