import networkx as nx
import os
import itertools
import time

def subset_verifier(graph, subset):
    if not subset:
        return graph.number_of_nodes() == 0

    dominated_nodes = set()

    dominated_nodes.update(subset)

    for node in subset:
        dominated_nodes.update(graph.neighbors(node))
    return len(dominated_nodes) == graph.number_of_nodes()

def weight_calculation(graph, subset):
    total_weight = 0
    for node in subset:
        total_weight += graph.nodes[node]['weight']
    return total_weight

def exhaustive_search(graph):
    all_nodes = list(graph.nodes())
    n = graph.number_of_nodes()

    best_weight = float('inf')
    best_subset = None

    tested_configs = 0

    print(f"  Initializing exhaustive search for n={n}. (Testing 2^{n} = {2 ** n} combinations)")

    for k in range(n + 1):

        for subset in itertools.combinations(all_nodes, k):

            tested_configs += 1

            if subset_verifier(graph,subset):

                weight_at_moment = weight_calculation(graph, subset)

                if weight_at_moment < best_weight:
                    best_weight = weight_at_moment
                    best_subset = subset

    return best_subset, best_weight, tested_configs

graphs_folder = "generated_graphs"
file = "graph_n20_p50,0.gml"

graph_path = os.path.join(graphs_folder, file)

if os.path.exists(graph_path):
    print(f"--- Loading graph: {graph_path} ---")
    G = nx.read_gml(graph_path)

    G = nx.convert_node_labels_to_integers(G, first_label=0)

    print("Calling exhaustive search...")

    start_time = time.time()

    optimal_subset, optimal_weight, number_of_tests = exhaustive_search(G)

    end_time = time.time()
    print(f" Execution Time: {end_time - start_time:.4f} seconds")

    print("\n--- Exhaustive search results ---")
    print(f"GraFico: {file}")
    print(f"Tested configurations: {number_of_tests}")
    print(f"Best set: {optimal_subset}")
    print(f"Best weight: {optimal_weight}")

else:
    print(f"ERROr: File not found. Verify name: {graph_path}")