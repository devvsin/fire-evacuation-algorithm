from collections import deque
import math

def create_grid(n, m, exits):
    grid = [['Open' for _ in range(m)] for _ in range(n)]
    grid[1][1] = 'START'
    for exit_route in exits:
        for i, j in exit_route:
            grid[i][j] = 'Exit'
    return grid

def spread_fire(grid, fire_locations, exits, max_iterations):
    n, m = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    fire_growth = 1

    def is_valid_move(x, y):
        return 0 <= x < n and 0 <= y < m and grid[x][y] != 'Exit' and grid[x][y] != 'Fire'

    def bfs_shortest_distance(start, exit_route):
        visited = [[False for _ in range(m)] for _ in range(n)]
        visited[start[0]][start[1]] = True
        queue = deque([(start[0], start[1], 0)])  # (x, y, distance)
        while queue:
            x, y, distance = queue.popleft()
            if (x, y) in exit_route:
                return distance
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_valid_move(new_x, new_y) and not visited[new_x][new_y]:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, distance + 1))
        return math.inf

    shortest_distances = []
    for exit_route in exits:
        shortest_distances.append(bfs_shortest_distance((1, 1), exit_route))

    for t in range(max_iterations):
        new_fire_locations = []
        for i, j in fire_locations:
            for dx, dy in directions:
                x, y = i + dx, j + dy
                if is_valid_move(x, y):
                    new_fire_locations.append((x, y))

        for x, y in new_fire_locations:
            grid[x][y] = 'Fire'

        fire_locations = new_fire_locations

        # Check if all non-exit cells are on fire
        if all(grid[i][j] == 'Fire' or grid[i][j] == 'Exit' for i in range(n) for j in range(m)):
            break

        # Double the fire growth every iteration
        fire_growth *= 2

        # Print the grid after each iteration
        print(f"Grid after iteration {t + 1}, fire growth: {fire_growth}:")
        for row in grid:
            print(row)
        print()

        # Check if fire reaches any exit route and remove it from consideration
        for i, exit_route in enumerate(exits):
            if any(grid[x][y] == 'Fire' for x, y in exit_route):
                shortest_distances[i] = math.inf

        # Choose the exit route with the shortest distance that has not been reached by fire
        chosen_exit_index = min((i for i, d in enumerate(shortest_distances) if d != math.inf), key=lambda i: shortest_distances[i])

        print(f"Chosen exit route: {exits[chosen_exit_index]}")

    # Mark all cells as 'Fire' in the final grid
    if t == max_iterations - 1:
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 'Exit':
                    grid[i][j] = 'Fire'

    return grid, t + 1

n = 7
m = 7
exit_1=[(1,1),(2,1),(3,1),(4,0),(5,0)]
exit_2=[(1,1),(1,2),(2,3),(3,4),(3,5),(3,6)]
exit_3=[(1,1),(0,2),(0,3),(0,4),(0,5)]
exit_4=[(1,1),(1,2),(2,3),(2,4),(2,5),(1,5),(0,5)]

exits = [exit_1, exit_2, exit_3, exit_4]
grid = create_grid(n, m, exits)

# Take fire locations as input from the user
fire_locations = []
while True:
    location_str = input("Enter fire location (row,column) or 'done' to finish: ")
    if location_str.lower() == 'done':
        break
    row, col = map(int, location_str.split(','))
    fire_locations.append((row, col))

# Maximum number of iterations before terminating the loop
max_iterations = 20  # Adjusted for demonstration purposes

# Spread fire with a maximum number of iterations
grid_with_fire, t = spread_fire(grid, fire_locations, exits, max_iterations)

# Calculate the total time in seconds
total_time_seconds = t * 30  # Assuming each iteration takes 30 seconds

# Print the final grid and the time taken
for row in grid_with_fire:
    print(row)

print(f"Time taken for the entire grid to be engulfed in fire or reach maximum iterations: {total_time_seconds} seconds")
