import heapq

graph = {
    'A': {'B': 4, 'J': 3},
    'B': {'D': 5},
    'C': {'F': 3, 'J': 2},
    'D': {'H': 4, 'F': 2},
    'E': {'H': 3},
    'F': {'D': 2, 'C': 3},
    'G': {'E': 3},
    'I': {'G': 2, 'J': 4},
    'J': {'C': 2, 'I': 4},
    'H': {}
}

heuristic = {
    'A': 10,
    'B': 8,
    'C': 7,
    'D': 4,
    'E': 2,
    'F': 5,
    'G': 3,
    'H': 0,
    'I': 4,
    'J': 6
}

def a_star(start, goal):

    queue = [(heuristic[start], 0, start, [start])]
    visited = set()

    while queue:

        f, g, current, path = heapq.heappop(queue)

        if current == goal:
            return path, g

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph[current].items():

            if neighbor not in visited:

                new_g = g + cost
                new_f = new_g + heuristic[neighbor]

                heapq.heappush(
                    queue,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return None

path, cost = a_star('A', 'H')

print("Shortest Path:", " → ".join(path))
print("Total Cost:", cost)