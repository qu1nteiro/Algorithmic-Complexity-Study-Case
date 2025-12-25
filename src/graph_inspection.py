import networkx as nx
import os
import matplotlib.pyplot as plt

output_folder = "data/generated_graphs"
file_to_inspect = "graph_n25_p75,0.gml"

complete_path = os.path.join(output_folder, file_to_inspect)

print(f"--- Reading file: {file_to_inspect} ---")

if not os.path.exists(complete_path):
    print(f"ERROR: File '{complete_path}' not found.")
    print("Verify if the name 'file_to_inspect' is correct")
else:
    G = nx.read_gml(complete_path)

    print(f"Graph type: {type(G)}")
    print(f"Nº of vertices (n): {G.number_of_nodes()}")
    print(f"Nº of edges (m): {G.number_of_edges()}")

    print("\n--- vertices (with it's attributes) ---")
    for no in G.nodes(data=True):
        print(f"  Vertice: {no}")

    print("\n--- edges (list of pars) ---")
    print(list(G.edges()))

    print("\n--- Generating Visualization---")

    positions = nx.get_node_attributes(G, 'pos')

    labels_nodes = nx.get_node_attributes(G, 'weight')

    plt.figure(figsize=(10, 8))

    nx.draw(G,
            positions,
            labels= labels_nodes,
            with_labels=True,
            node_color='lightgreen',
            node_size=600,
            font_size=10,
            font_color='black'
            )

    plt.title(f"Visualization of {file_to_inspect}")
    plt.xlabel("Coordinate X")
    plt.ylabel("Coordinate Y")
    plt.grid(True)

    plt.savefig("graph_n25_p75.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("--- Inspection Concluded ---")