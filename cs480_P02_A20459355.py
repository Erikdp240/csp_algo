import csv
import sys as s

def bac

def open_csv(file_name):
  data = {}

  with open(file_name, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
      if file_name == 'driving.csv':
        data[row[0]] = list(map(int, row[1:]))
      else: 
        data[row[0]] = int(row[1])

  return data

def get_args():
  if len(s.argv) != 3:
    print('Error: Not enough or too many input arguments.')
    s.exit(1)

  state = s.argv[1]
  park = s.argv[2]

  return state, park

def main():
  intitial, no_of_parks = get_args()

  driving_data = open_csv('driving2.csv')
  parks_data = open_csv('parks.csv')
  zone_data = open_csv('zones.csv')

  zone_variables = {}

  for state, zone in zone_data.items():
    if zone not in zone_variables:
      zone_variables[zone] = []
    zone_variables[zone].append(state)

if __name__ == '__main__':
  main()