import csv
import sys

driving_file = 'driving2.csv'
parks_file = 'parks.csv'
zones_file = 'zones.csv'

def get_args():
  if len(sys.argv) != 3:
    print("ERROR: Not enough or too many input arguments.")
    sys.exit(1)

  return sys.argv[1], int(sys.argv[2])

def read_driving(file_name):
  with open(file_name, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)

    data = {}

    for row in reader:
      state = row[0]

      data[state] = {
        headers[i]: int(row[i]) for i in range(1, len(row)) 
      }

  return data

def read_parks_zone_file(file_name):
  with open(file_name, 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    count = next(reader)

    data = {
      headers[i]: int(count[i]) for i in range(1, len(headers))
    }

  return data

def is_complete(csp, assignment, parks_visited):
  # All zone variables have a valid value assigned to it
  # Parks visited >= Number of parks
  for zone in csp['zones']:
    if zone not in assignment:
      return False
  
  return parks_visited >= csp['no_of_parks']

def select_unassigned_variable(csp, assignment):
  # Pick next zone variable
  for zone in csp['zones']:
    if zone not in assignment:
      return zone
  
  return None

def order_domain_values(csp, var):
  # Order all POSSIBLE domain values (next states) alphabetically
  return sorted(csp['domains'][var])

def is_consistent(csp, var, value, assignment, parks_visited):
  current_zone = var
  index = csp['zones'].index(current_zone)

  if index == 0:
    return True

  if index > 0:
    previous_zone = csp['zones'][index-1]
  else:
    previous_zone = None

  if previous_zone and previous_zone in assignment:
    previous_state = assignment[previous_zone]
    current_state = value

    road_distance = csp['distances'].get(previous_state, {}).get(current_state, -1)

    if road_distance == -1:
      return False
    
  current_parks_visited = parks_visited + csp['parks'].get(value, 0)

  if len(assignment) == len(csp['zones']) - 1:
    if current_parks_visited < csp['no_of_parks']:
      return False
  
  return True

def inference(csp, var, assignment):
  index = csp['zones'].index(var)

  if index >= len(csp['zones']) - 1:
    return {}

  next_zone = csp['zones'][index + 1]
  current_state = assignment[var]
  inferences = { next_zone : [] }

  for next_state in csp['domains'][next_zone]:
    distance = csp['distances'].get(current_state, {}).get(next_state, -1)

    if distance == -1:
      inferences[next_zone].append(next_state)

  for state in inferences[next_zone]:
    csp['domains'][next_zone].remove(state)

  return inferences

def add_inferences(csp, inferences):
  for zone, state_to_remove in inferences.items():
    for state in state_to_remove:
      if state in csp['domains'][zone]:
        csp['domains'][zone].remove(state)

def remove_inferences(csp, inferences):
  for zone, state_to_remove in inferences.items():
    for state in state_to_remove:
      if state not in csp['domains'][zone]:
        csp['domains'][zone].append(state)

def backtrack(csp, assignment, parks_visited=0):
  if is_complete(csp, assignment, parks_visited):
    return assignment
  
  var = select_unassigned_variable(csp, assignment)

  for value in order_domain_values(csp, var):
    if is_consistent(csp, var, value, assignment, parks_visited):
      assignment[var] = value
      updated_parks_visited = parks_visited + csp['parks'].get(value, 0)

      inferences = inference(csp, var, assignment)

      if inferences != 'failure':
        add_inferences(csp, inferences)

        result = backtrack(csp, assignment, updated_parks_visited)

        if result != 'failure':
          return result
        
        remove_inferences(csp, inferences)

      del assignment[var]
  
  return 'failure'

def backtrack_search(csp):
  return backtrack(csp, {})

def calculate_total_distance(solution, distances):
  total_distance = 0
  states = list(solution.values())

  for i in range(len(states) - 1):
    state_a = states[i]
    state_b = states[i + 1]
    distance = distances.get(state_a, {}).get(state_b, -1)

    if distance == -1:
        return -1
    
    total_distance += distance

  return total_distance

def main():
  # Command line arguments
  initial_state, no_of_parks = get_args()

  # Load CSV files
  distances = read_driving(driving_file)
  parks = read_parks_zone_file(parks_file)
  zones = read_parks_zone_file(zones_file)

  starting_zone = zones[initial_state]

  # Create CSP Dictionary
  csp = {
    'zones' : [ f"Z{z}" for z in range(starting_zone, 13) ],
    'domains' : { f"Z{z}": [] for z in range(starting_zone, 13) },
    'parks' : parks,
    'distances' : distances,
    'no_of_parks' : no_of_parks
  }

  # Append states to their zones
  for state, zone in zones.items():
    zone_key = f"Z{zone}"
    if zone_key in csp['domains']:
      csp['domains'][zone_key].append(state)  
    
  solution = backtrack_search(csp)

  last_name = 'Pacheco'
  first_name = 'Erik'
  student_id = 'A20459355'

  total_distance = calculate_total_distance(solution, distances)
  total_parks_visited = sum(parks[state] for state in solution.values())

  print(f"{last_name}, {first_name}, {student_id} solution:")
  print(f"Initial state: {initial_state}")
  print(f"Minimum number of parks: {no_of_parks}")

  if solution != "failure":
    print("Solution path:", solution)
    print("Number of states on the path:", len(solution))
    print("Path cost (total driving distance):", total_distance)
    print("Number of national parks visited:", total_parks_visited)
  else:
    print("Solution path: FAILURE: NO PATH FOUND")
    print("Number of states on a path: 0")
    print("Path cost: 0")
    print("Number of national parks visited: 0")

if __name__ == '__main__':
  main()