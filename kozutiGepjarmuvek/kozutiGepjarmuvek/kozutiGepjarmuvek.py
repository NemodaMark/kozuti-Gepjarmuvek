# Megnyitom a filet olvasásra
with open("atlageletkor.csv", encoding='ISO-8859-1') as file:
    # Kiolvastatom az összes sort
    lines = file.readlines()

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

# Kiírom az adatokat minden év esetén
for year, data_for_year in data_by_year.items():
    print(f"\nAdatok {year}-re/ra:")
    print(data_for_year)
