"Q1"
doctors = input("Enter doctors: ").split()
shifts = input("Enter shifts: ").split()

def solve(assign, i):
    if i == len(doctors):
        print("\nFinal Schedule:")
        for d in doctors:
            print(d, "->", assign[d])
        return True

    d = doctors[i]

    for s in shifts:
        if s not in assign.values():

            if d == "D1" and s == "Night":
                continue
            if d == "D3" and s == "Morning":
                continue

            assign[d] = s

            if "D2" in assign and "D3" in assign:
                if shifts.index(assign["D2"]) >= shifts.index(assign["D3"]):
                    del assign[d]
                    continue

            if solve(assign, i + 1):
                return True

            del assign[d]

    return False

solve({}, 0)

"Q2"
from collections import deque

r, c = 5, 5

print("Enter the 5x5 grid (S, G, 0, X):")
grid = [input().split() for _ in range(r)]

for i in range(r):
    for j in range(c):
        if grid[i][j] == 'S':
            start = (i, j)
        if grid[i][j] == 'G':
            goal = (i, j)

move = [(-1,0),(1,0),(0,-1),(0,1)]
q = deque([(start, [start])])
visited = {start}

while q:
    (x, y), path = q.popleft()

    if (x, y) == goal:
        print("Path:", path)
        print("Cost:", len(path)-1)
        break

    for dx, dy in move:
        nx, ny = x + dx, y + dy

        if 0 <= nx < r and 0 <= ny < c:
            if grid[nx][ny] != 'X' and (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append(((nx, ny), path + [(nx, ny)]))

"Q3"
import heapq

r, c = 5, 5

print("Enter the 5x5 grid (S, G, 0, X, R):")
grid = [input().split() for _ in range(r)]

for i in range(r):
    for j in range(c):
        if grid[i][j] == 'S':
            start = (i, j)
        if grid[i][j] == 'G':
            goal = (i, j)

move = [(-1,0),(1,0),(0,-1),(0,1)]

pq = [(0, start)]
visited = set()

while pq:
    cost, (x, y) = heapq.heappop(pq)

    if (x, y) in visited:
        continue

    visited.add((x, y))

    if (x, y) == goal:
        print("Minimum Cost =", cost)
        break

    for dx, dy in move:
        nx, ny = x + dx, y + dy

        if 0 <= nx < r and 0 <= ny < c:
            if grid[nx][ny] != 'X' and (nx, ny) not in visited:
                extra = 2 if grid[nx][ny] == 'R' else 0
                heapq.heappush(pq, (cost + 1 + extra, (nx, ny)))
