import pandas as pd
import networkx as nx
import numpy as np
from networkx.algorithms.approximation import traveling_salesman_problem

from lib.config import config

class ShortestPath:
    def __init__(self):
        self.df = None
        self.ordered_points = None

    def load(self):
        # Step 1: Read the CSV file
        self.df = pd.read_csv(config.points_csv_file_path)

    def setup(self):
        # Step 2: Create a graph
        G = nx.Graph()

        # Add nodes to the graph
        for index, row in self.df.iterrows():
            G.add_node(index, pos=(row['lon_x'], row['lat_y']))

        # Add edges to the graph with Euclidean distance as weight
        for i in range(len(self.df)):
            for j in range(i + 1, len(self.df)):
                dist = np.sqrt((self.df.iloc[i]['lat_y'] - self.df.iloc[j]['lat_y']) ** 2 +
                            (self.df.iloc[i]['lon_x'] - self.df.iloc[j]['lon_x']) ** 2)
                G.add_edge(i, j, weight=dist)

        # Step 3: Solve the Traveling Salesman Problem to find the shortest path
        tsp_path = traveling_salesman_problem(G, cycle=True)

        # Get the ordered points and add a new column for the order index
        self.ordered_points = self.df.iloc[tsp_path].copy()
        self.ordered_points['order'] = range(len(tsp_path))        

    def to_csv(self):
        # Save the ordered points to a new CSV file with the same columns as the input CSV
        self.ordered_points.to_csv(config.shortest_path_csv_file_path, index=False)
