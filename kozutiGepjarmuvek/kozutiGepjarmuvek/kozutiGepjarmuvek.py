with open('atlageletkor.csv', encoding='ISO-8859-1') as file:
    lines = file.readlines()

vehicle_type = dict()
year_data = dict()
data = []

# Splitting, removing empty spaces, and formatting
data = [line.strip().split(';') for line in lines]
data = [[cell.strip() for cell in row] for row in data]

# Skip the first row
header = data[0]
data = data[1:]

# Extracting vehicle types and the first year (year is the key in year_data)
vehicle_type_keys = header[1:]
year_key = header[0]

for row_index, item in enumerate(data):
    if len(item) < len(vehicle_type_keys) + 1:
        continue  # Skip if there are not enough columns or if the row is empty

    current_year = item[0]
    vehicle_type_values = item[1:]
    vehicle_type_dict = dict(zip(vehicle_type_keys, vehicle_type_values))
    vehicle_type_dict[year_key] = current_year
    vehicle_type[current_year] = vehicle_type_dict
    year_data[current_year] = {'Values': vehicle_type_values, 'Position': row_index}

# Printing the results
print("Vehicle Type Dictionary:")
for key, value in vehicle_type.items():
    print(f"{year_key}: {value[year_key]} (Row {year_data[key]['Position']})")
    for sub_key, sub_value in value.items():
        if sub_key != year_key:
            print(f"{sub_key}: {sub_value}")

print("\nYear Data Dictionary:")
for key, value in year_data.items():
    print(f"{year_key}: {key}")
    print(f"Values: {value['Values']}")
    print(f"Position: {value['Position']}")
