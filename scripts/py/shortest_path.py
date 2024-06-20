import pandas as pd
import networkx as nx
import numpy as np
from networkx.algorithms.approximation import traveling_salesman_problem

# Step 1: Read the CSV file
df = pd.read_csv('./data/20240529_sblz1z2_p1_waypoints.csv')

# Step 2: Create a graph
G = nx.Graph()

# Add nodes to the graph
for index, row in df.iterrows():
    G.add_node(index, pos=(row['latitude'], row['longitude']))

# Add edges to the graph with Euclidean distance as weight
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        dist = np.sqrt((df.iloc[i]['latitude'] - df.iloc[j]['latitude']) ** 2 +
                       (df.iloc[i]['longitude'] - df.iloc[j]['longitude']) ** 2)
        G.add_edge(i, j, weight=dist)

# Step 3: Solve the Traveling Salesman Problem to find the shortest path
tsp_path = traveling_salesman_problem(G, cycle=True)

# Get the ordered points
ordered_points = df.iloc[tsp_path]

# Save the ordered points to a new CSV file with the same columns as the input CSV
ordered_points.to_csv('./data/20240529_sblz1z2_p1_waypoints_shortest_path.csv', index=False)
