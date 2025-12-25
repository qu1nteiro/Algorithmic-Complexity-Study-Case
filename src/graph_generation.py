import itertools
import os
import shutil
import math
import networkx as nx
import random

student_number = 113816
random.seed(student_number)

n_min = 4
n_max = 30

densities = [0.125, 0.25, 0.50, 0.75]

coordinates_min = 1
coordinates_max = 500

Dist_min = 10

weight_min = 1
weight_max = 100

# OUTPUT DIRECTORY
base_data_folder = "data"
output_folder = os.path.join(base_data_folder, "generated_graphs")

os.makedirs(base_data_folder, exist_ok=True)

# Dir generated_graphs
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

print(f"*** Generating Graphs (Seed: {student_number}) ***")

for n in range(n_min, n_max +1):
    print(f"--- Generating Graph for n = {n} ---")
    graph_base = nx.Graph()
    positions = []

    for i in range(n):
        while True:
            x = random.randint(coordinates_min, coordinates_max)
            y = random.randint(coordinates_min, coordinates_max)
            new_position = (x, y)

            valid_position = True
            for previous_position in positions:
                dist = math.dist(new_position, previous_position)

                if dist < Dist_min:
                    valid_position = False
                    break

            if valid_position:
                positions.append(new_position)
                vertice_weight = random.randint(weight_min, weight_max)
                graph_base.add_node(i, pos = new_position, weight = vertice_weight)
                break

    all_nodes = list(graph_base.nodes())
    possible_edges = list(itertools.combinations(all_nodes,2))
    random.shuffle(possible_edges)
    E_max = (n * (n - 1)) / 2

    for p in densities:
        graph_final = graph_base.copy()
        edges_number = round(p * E_max)
        add_edges = possible_edges[:edges_number]
        graph_final.add_edges_from(add_edges)

        percentage_str = str(p*100).replace(".", ",")
        file_name = f"graph_n{n}_p{percentage_str}.gml"
        file_path = os.path.join(output_folder, file_name)

        nx.write_gml(graph_final, file_path)

    print(f" > File for n={n} (4 densities) saved in '{output_folder}/')")

print("*** Graphs Generation Complete ***")




