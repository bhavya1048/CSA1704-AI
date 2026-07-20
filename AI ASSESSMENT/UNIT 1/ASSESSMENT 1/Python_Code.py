"Q1"
j1 = int(input("Enter capacity of Jug 1: "))
j2 = int(input("Enter capacity of Jug 2: "))
target = int(input("Enter target amount: "))

a = 0
b = 0

while b != target:
    if a == 0:
        a = j1
    elif b == j2:
        b = 0
    else:
        t = min(a, j2 - b)
        a -= t
        b += t

    print("Jug1 =", a, "Jug2 =", b)

print("Target Reached!")
"Q2"
class MarsRover:
    def __init__(self):
        self.percepts = [
            "Camera Images",
            "Soil Samples",
            "Rock Composition",
            "Temperature",
            "Atmospheric Pressure",
            "Obstacle Detection",
            "Battery Status"
        ]

        self.environment = {
            "Observability": "Partially Observable",
            "Nature": "Dynamic",
            "Episodes": "Sequential",
            "State": "Continuous",
            "Agents": "Single Agent"
        }

        self.actions = [
            "Move Forward",
            "Turn Left",
            "Turn Right",
            "Collect Sample",
            "Analyze Sample",
            "Capture Image",
            "Avoid Obstacle",
            "Transmit Data",
            "Recharge Battery"
        ]

        self.performance = [
            "Accurate Sample Collection",
            "Safe Navigation",
            "Efficient Battery Usage",
            "Successful Data Transmission"
        ]

        self.architecture = "Model-Based Goal-Based Agent"

    def display(self):
        print("\n========== MARS ROVER INTELLIGENT AGENT ==========\n")

        print("Percepts")
        for i, p in enumerate(self.percepts, 1):
            print(f"{i}. {p}")

        print("\nOperating Environment")
        for key, value in self.environment.items():
            print(f"{key}: {value}")

        print("\nActions")
        for i, action in enumerate(self.actions, 1):
            print(f"{i}. {action}")

        print("\nPerformance Measures")
        for i, measure in enumerate(self.performance, 1):
            print(f"{i}. {measure}")

        print("\nSuitable Agent Architecture")
        print(self.architecture)


rover = MarsRover()
rover.display()
"Q3"
N = 8
board = [-1] * N

def safe(row, col):
    for i in range(col):
        if board[i] == row or abs(board[i] - row) == abs(i - col):
            return False
    return True

def solve(col):
    if col == N:
        return True
    for row in range(N):
        if safe(row, col):
            board[col] = row
            if solve(col + 1):
                return True
    return False

if solve(0):
    for i in range(N):
        print("Q" if board[i] >= 0 else ".", end=" ")
    print("\nQueen Positions:", board)

"Q4"
pickup = input("Enter Pickup Location: ")
destination = input("Enter Destination: ")
cab = input("Enter Cab Type (Mini/Micro/Sedan/Prime): ")

print("\nBooking Details")
print("Pickup:", pickup)
print("Destination:", destination)
print("Cab Type:", cab)
print("Status: Cab Booked Successfully")
"Q5"
from queue import PriorityQueue

graph = {
    'S': [('A', 2), ('B', 5)],
    'A': [('C', 4), ('D', 7)],
    'B': [('D', 2)],
    'C': [('G', 3)],
    'D': [('G', 1)],
    'G': []
}

pq = PriorityQueue()
pq.put((0, 'S', ['S']))
visited = set()

while not pq.empty():
    cost, node, path = pq.get()

    if node == 'G':
        print("Least Cost Path:", " -> ".join(path))
        print("Total Cost:", cost)
        break

    if node not in visited:
        visited.add(node)
        for next_node, weight in graph[node]:
            pq.put((cost + weight, next_node, path + [next_node]))



