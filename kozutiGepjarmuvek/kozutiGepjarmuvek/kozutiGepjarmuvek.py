myFile = open('uzemanyagfogyasztas.csv')
myLine = myFile.readlines()
myFile.close() 

vehicType = dict()
year = dict()
x = []

# Split, üres helyek kitörlése, és inté alakítás
x = [line.strip().split(';') for line in myLine]
x = [[int(cell.replace(' ', '')) if cell.strip().replace(' ', '').isnumeric() else cell for cell in row] for row in x]

#elsõ sor skip
x = x[1:]

# Minen a második sorból (kulcs a vehicType) és az elsõ év(kulcs az year)
vehicTypeKeys = x[0]
yearKey = vehicTypeKeys.pop(0)

for item in x:
    if len(item) < len(vehicTypeKeys):
        continue  # Ha nincs elég sor, vagy üres a sor skip

    year_value = item[0]
    vehicType_values = item[1:]
    vehicType_dict = dict(zip(vehicTypeKeys, vehicType_values))
    vehicType[year_value] = vehicType_dict
    year[year_value] = vehicType_values

# kiiratás (valamiért hozzáad egy + egyet
print("vehicType Dictionary:")
for key, value in vehicType.items():
    print(f"{yearKey}: {key}")
    for sub_key, sub_value in value.items():
        print(f"{sub_key}: {sub_value}")

print("\nyear Dictionary:")
for key, value in year.items():
    print(f"{yearKey}: {key}")
    print(f"Values: {value}")
