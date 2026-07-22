import heapq
import matplotlib.pyplot as plt
import networkx as nx


graph = {

    'Andheri Railway Colony': {
        'Andheri Station': 1.2,
        'WEH Metro': 1.5
    },

    'Andheri Station': {
        'Santacruz': 2.3
    },

    'WEH Metro': {
        'Santacruz': 2.0
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

node_positions = {

    'Andheri Railway Colony': (6, 0),

    'Andheri Station': (4, 2),

    'WEH Metro': (8, 2),

    'Santacruz': (6, 5),

    'Khar Road': (6, 8),

    'Bandra Station': (6, 11),

    'Bandstand Promenade': (6, 14)

}


def a_star_search(graph, heuristics, start, goal):

    priority_queue = [(heuristics[start], start, [start], 0)]

    visited = set()

    while priority_queue:

        f_score, current, path, g_score = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path, g_score

        for neighbor, edge_weight in graph[current].items():

            if neighbor not in visited:

                next_g = g_score + edge_weight
                next_f = next_g + heuristics[neighbor]

                heapq.heappush(
                    priority_queue,
                    (next_f, neighbor, path + [neighbor], next_g)
                )

    return None, float('inf')



optimal_path, total_distance = a_star_search(

    graph,
    heuristics,
    'Andheri Railway Colony',
    'Bandstand Promenade'

)

print("Optimal Path Discovered:")
print(" -> ".join(optimal_path))
print(f"\nTotal Road Distance: {total_distance:.1f} km")



G = nx.DiGraph()

for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

plt.figure(figsize=(11, 9))

path_edges = list(zip(optimal_path, optimal_path[1:]))

normal_edges = [
    edge for edge in G.edges()
    if edge not in path_edges
]


nx.draw_networkx_nodes(
    G,
    node_positions,
    node_size=2500,
    node_color='lightblue'
)

nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=normal_edges,
    width=1.5,
    edge_color='gray',
    arrows=True
)

nx.draw_networkx_edges(
    G,
    node_positions,
    edgelist=path_edges,
    width=3.5,
    edge_color='darkorange',
    arrows=True
)

node_labels = {
    node: f"{node}\nh(n)={heuristics[node]}"
    for node in G.nodes()
}

nx.draw_networkx_labels(
    G,
    node_positions,
    labels=node_labels,
    font_size=8,
    font_weight='bold'
)

edge_labels = nx.get_edge_attributes(G, 'weight')

formatted_edge_labels = {
    edge: f"{weight} km"
    for edge, weight in edge_labels.items()
}

nx.draw_networkx_edge_labels(
    G,
    node_positions,
    edge_labels=formatted_edge_labels,
    font_color='red'
)

plt.title(
    "A* Routing Map: Andheri Railway Colony to Bandstand Promenade\n"
    "(Highlighted Orange Path = Optimal Route)",
    fontsize=14
)

plt.axis('off')
plt.tight_layout()
plt.show()