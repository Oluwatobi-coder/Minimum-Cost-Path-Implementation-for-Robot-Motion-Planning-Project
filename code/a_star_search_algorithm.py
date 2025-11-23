#!/usr/bin/env python3

# the command at the top ensures the code can be run on Linux or macOS using python3 interpreter

# importing the required modules
import csv # maniplation of csv files
import heapq  # heap queue implementation for the OPEN list
import os # interaction with the operating system
from collections import defaultdict # provision of default values for keys for the OPEN list




# specifying the start and goal nodes
start_node_id = 1
goal_node_id = 12


# function to load the node data from the nodes.csv file and returns 
# a dictionary mapping each node id to its heuristic cost
def load_nodes(filename):
    # initializing an empty dictionary
    heuristics = {}
    with open(filename, mode='r', encoding='utf-8') as f:
            # reading the column names and extracting each row of data
            reader = csv.reader(f)
            for row in reader:
                node_id = int(row[0])
                h_cost = float(row[3])
                heuristics[node_id] = h_cost
    return heuristics

# function to load the edge data from the edges from csv file into a list
def load_graph(filename):
    # using defaultdict to automatically initialize an empty list for new nodes
    graph = defaultdict(list)
    with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                id1 = int(row[0])
                id2 = int(row[1])
                cost = float(row[2])
                
                # adding edge in both directions since the graph is undirected
                graph[id1].append((id2, cost))
                graph[id2].append((id1, cost))
    return graph

# function implementing the A* search algorithm of the graph
def a_star_search(graph, heuristics, start_node, goal_node):

    # initializing OPEN list for storing the node id and total path cost (f_cost)
    # the node with the smallest f_cost is always at the top
    open_list = []
    
    # initializing the CLOSED set for storing node_ids that have been evaluated.
    closed_set = set()
    
    
    # initialize the dictionary for the past cost for each node
    # the past cost is set to infinity for all except the start node
    p_costs = defaultdict(lambda: float('inf'))
    p_costs[start_node] = 0
    
    # initializing the dictionary to store the search tree i.e child node to parent node, to reconstruct 
    # the path.
    parents = {}
    
    # adding the start node to the OPEN list i.e. f_cost = p_cost + h_cost
    start_f_cost = p_costs[start_node] + heuristics[start_node]
    heapq.heappush(open_list, (start_node, start_f_cost))

    # implementing the search loop
    while open_list:
        # extracting the node with the lowest f_cost from the OPEN list
        current_node, current_f_cost = heapq.heappop(open_list)
        
        # checking if the current node this is the goal, then the path is reconstructed and returned
        if current_node == goal_node:
            path = []
            node = goal_node
            while node is not None:
                path.append(node)
                node = parents.get(node)  # getting the parent node, defaults to None if not found
            return path[::-1]  # reversing the list to get the path from start to goal

        # skipping current node if already evalueted
        if current_node in closed_set:
            continue
            
        # adding the current node to the CLOSED as it is being evaluated
        closed_set.add(current_node)
        
        # exploring the neighbor nodes
        for neighbor_node, edge_cost in graph.get(current_node, []):
            
            # skipping the neighbor node if found in the CLOSED set, since the best path to it had been 
            # found already
            if neighbor_node in closed_set:
                continue
                
            # Calculate the speculative cost to reach the neighbor node through the current node 
            # i.e. past_cost + edge_cost
            speculative_cost = p_costs[current_node] + edge_cost
            
            # checking if this is a better path (lower p_cost) compared to the previously found one
            if speculative_cost < p_costs[neighbor_node]:
                # recording the improved cost i.e. lower cost
                p_costs[neighbor_node] = speculative_cost
                parents[neighbor_node] = current_node
                
                # calculating the neighbor node's total path cost i.e. f_cost
                f_cost = speculative_cost + heuristics[neighbor_node]
                
                # adding the neighbor node to the OPEN list
                heapq.heappush(open_list, (neighbor_node, f_cost))

    # returning None if the loop finishes without finding the goal node i.e. no path exists
    return None

# function to save the final path to the path.csv file
def save_path_to_csv(path, filename):
    try:
        # formatting the path as a comma-separated string
        path_str = ",".join(map(str, path))
        
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(path_str + "\n")
        print(f"Successfully saved path to {filename}")
        
    except IOError as e:
        print(f"Error saving path file: {e}")
        
# defining the main function that calls the other functions of the script i.e runs the A* search and stores 
# the minimum-cost path to the path.csv file
def main():
    print("Starting A* search...")
    
    # loading the nodes and the edges data from files
    heuristics = load_nodes('results/nodes.csv')
    graph = load_graph('results/edges.csv')

    # displaying info to console
    print(f"Loaded {len(heuristics)} nodes and graph data.")
    print(f"Finding path from {start_node_id} to {goal_node_id}...")
    
    # running the A* Search algorithm
    path = a_star_search(graph, heuristics, start_node_id, goal_node_id)
    
    # handling the result
    if path:
        print(f"Path found: {path}")
        save_path_to_csv(path, os.path.join('results', 'path.csv'))
    else:
        print(f"No path found from {start_node_id} to {goal_node_id}.")
        save_path_to_csv([1], os.path.join('results', 'path.csv'))

# executing the main() function
if __name__ == "__main__":
    main()