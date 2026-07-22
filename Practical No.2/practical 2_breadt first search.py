import matplotlib.pyplot as plt

graph = {

    'Andheri Railway Colony': {
        'Andheri Station': 1.2,
        'WEH Metro': 1.5
    },

    'WEH Metro': {
        'Santacruz': 2.0
    },

    'Andheri Station': {
        'Santacruz': 2.3
    },

    'Santacruz': {
        'Khar Road': 2.1
    },

    'Khar Road': {
        'Bandra Station': 2.0
    },

    'Bandra Station': {
        'Bandstand Promenade': 1.8
    },

    'Bandstand Promenade': {}
}


heuristics = {

    'Andheri Railway Colony': 9.1,
    'Andheri Station': 7.8,
    'WEH Metro': 7.9,
    'Santacruz': 5.5,
    'Khar Road': 3.3,
    'Bandra Station': 1.8,
    'Bandstand Promenade': 0
}


coords = {

    'Andheri Railway Colony': (6, 0),

    'WEH Metro': (8, 2),

    'Andheri Station': (4, 2),

    'Santacruz': (6, 5),

    'Khar Road': (6, 8),

    'Bandra Station': (6, 11),

    'Bandstand Promenade': (6, 14)
}


def rbfs_search(start, goal):

    success, path, cost, _ = rbfs(
        start,
        goal,
        g=0,
        f_limit=float('inf'),
        path=[start]
    )

    return path, cost


def rbfs(node, goal, g, f_limit, path):

    if node == goal:
        return True, path, g, g

    neighbors = graph[node]

    if not neighbors:
        return False, [], 0, float('inf')

    successors = []

    for neighbor, distance in neighbors.items():

        if neighbor not in path:

            next_g = g + distance

            next_f = max(
                next_g + heuristics[neighbor],
                g + heuristics[node]
            )

            successors.append(
                [next_f, neighbor, next_g]
            )

    if not successors:
        return False, [], 0, float('inf')

    while True:

        successors.sort(key=lambda x: x[0])

        best = successors[0]

        if best[0] > f_limit:
            return False, [], 0, best[0]

        if len(successors) > 1:
            alternative = successors[1][0]
        else:
            alternative = float('inf')

        success, result_path, total_g, returned_f = rbfs(

            best[1],
            goal,
            best[2],
            min(f_limit, alternative),
            path + [best[1]]

        )

        best[0] = returned_f

        if success:
            return True, result_path, total_g, returned_f


path, total_dist = rbfs_search(
    'Andheri Railway Colony',
    'Bandstand Promenade'
)

print('Optimal RBFS Path:')
print(' -> '.join(path))
print(f'\nTotal Road Distance: {total_dist:.1f} km')


plt.figure(figsize=(10, 8))

for node, neighbors in graph.items():

    x1, y1 = coords[node]

    for neighbor, dist in neighbors.items():

        x2, y2 = coords[neighbor]

        is_path = (
            node in path and
            neighbor in path and
            path.index(neighbor) == path.index(node) + 1
        )

        if is_path:
            color = '#2ecc71'
            width = 3
        else:
            color = '#bdc3c7'
            width = 1.5

        plt.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=width,
            zorder=1
        )

        plt.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            f'{dist} km',
            color='red',
            fontsize=8,
            ha='center'
        )

for node, (x, y) in coords.items():

    if node in path:
        color = '#f1c40f'
    else:
        color = '#3498db'

    plt.scatter(
        x,
        y,
        color=color,
        s=900,
        zorder=2
    )

    plt.text(
        x,
        y,
        f'{node}\nh={heuristics[node]}',
        ha='center',
        va='center',
        color='white',
        fontsize=8,
        fontweight='bold'
    )

plt.title(
    f'RBFS Routing Map: Andheri Railway Colony to Bandstand Promenade\n'
    f'(Optimal Distance = {total_dist:.1f} km)',
    fontsize=13,
    fontweight='bold'
)

plt.axis('off')
plt.tight_layout()
plt.show()