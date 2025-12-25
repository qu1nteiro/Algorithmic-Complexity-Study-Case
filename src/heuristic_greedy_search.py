import networkx as nx
import os
import time


# --- 1. HELPER FUNCTIONS ---

def calculate_weight(graph, subset):
    """Calculates the sum of weights of the nodes in the subset."""
    total = 0
    for node in subset:
        total += graph.nodes[node]['weight']
    return total


def is_dominating(graph, subset):
    """
    Check: Verifies if the chosen subset actually covers the whole graph.
    """
    if not subset:
        return False

    covered = set(subset)
    for node in subset:
        covered.update(graph.neighbors(node))

    return len(covered) == len(graph.nodes())


# --- 2. GREEDY HEURISTIC ALGORITHM ---

def find_dominating_set_greedy(graph):
    """
    Greedy Algorithm:
    Iteratively picks the node with the best 'cost-benefit' ratio
    """
    greedy_set = set()
    nodes_to_cover = set(graph.nodes())
    ops_count = 0

    while nodes_to_cover:
        best_node = None
        best_ratio = -1.0

        # Only consider nodes that are NOT yet in our solution set
        candidates = set(graph.nodes()) - greedy_set

        for node in candidates:
            weight = graph.nodes[node]['weight']

            # Prevent division by zero if weight is 0
            if weight <= 0: weight = 0.0001

            # Calculate how many new nodes this candidate covers
            neighbors = set(graph.neighbors(node)) | {node}
            newly_covered = len(neighbors.intersection(nodes_to_cover))

            # Calculate Efficiency Ratio
            if newly_covered > 0:
                ratio = newly_covered / weight
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_node = node

        # Fallback: If no node improves coverage (e.g., disconnected components)
        # pick the cheapest remaining node needed to cover the rest.
        if best_node is None:
            if not nodes_to_cover: break
            best_node = min(nodes_to_cover, key=lambda n: graph.nodes[n]['weight'])

        # Add the best node to solution
        greedy_set.add(best_node)
        ops_count += 1

        # Remove covered nodes from the "To Do" list
        covered_now = set(graph.neighbors(best_node)) | {best_node}
        nodes_to_cover.difference_update(covered_now)

    final_weight = calculate_weight(graph, greedy_set)
    return greedy_set, final_weight, ops_count


# --- 3. MAIN EXECUTION ---

graphs_folder = "data/generated_graphs"
file_to_inspect = "graph_n25_p75,0.gml"
graph_path = os.path.join(graphs_folder, file_to_inspect)

if os.path.exists(graph_path):
    print(f"\n=== LOADING GRAPH: {file_to_inspect} ===")

    # Load Graph
    G = nx.read_gml(graph_path)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    print(f"Graph Info: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")

    # Run Greedy Heuristic
    print("\n>> Running Greedy Heuristic...")
    start_time = time.time()

    greedy_subset, greedy_weight, operations = find_dominating_set_greedy(G)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Check validity
    valid = is_dominating(G, greedy_subset)
    valid_str = "YES" if valid else "NO"

    # --- PRINT RESULTS ---
    print("-" * 40)
    print("      GREEDY HEURISTIC RESULTS      ")
    print("-" * 40)
    print(f"Execution Time  : {elapsed_time:.6f} seconds")
    print(f"Operations      : {operations} steps")
    print(f"Total Weight    : {greedy_weight}")
    print(f"Set Size        : {len(greedy_subset)} nodes")
    print(f"Valid Solution? : {valid_str}")
    print("-" * 40)
    print(f"Selected Nodes  : {sorted(list(greedy_subset))}")
    print("=" * 40)

else:
    print(f"ERROR: File not found at {graph_path}")