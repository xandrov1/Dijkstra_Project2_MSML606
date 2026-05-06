import osmnx as ox
import matplotlib.pyplot as plt 
import networkx as nx
import heapq


# To download and save graph to .gramphml
# try:
#     place = ox.graph_from_place("Manhattan , New York, USA")
#     ox.save_graphml(place, "manhattan.graphml")

# except Exception as e: 
#     print(f"omething went wrong: {e}") 

# File load from local
try:
    place = ox.load_graphml("manhattan.graphml")
    print(f"Graph loaded")
except Exception as e:
    print(f"Something went wrong: {e}")

fig, ax = ox.plot_graph(place, show= False) # Get fig and ax to connect click event; stop automatic plotting with show
source = None
destination = None

# Click interaction
def on_click(event):
    global source, destination # Set globals

    # print(event.xdata, event.ydata) # Print coordinates

    # Coordinates
    x = event.xdata 
    y = event.ydata
    # node = ox.nearest_nodes(place, x,y) # Snap click to nearest node
    # print(f"Node: {node}") # Print node
    
    if source is None: # First click is source
        source = ox.nearest_nodes(place, x, y)
    elif destination is None: # Second is destination
        destination = ox.nearest_nodes(place, x, y)
        print(f"Source: {source} - Destination: {destination}")
    else: # Third is reset
        source = None
        destination = None
        print("Reset")

# Dijkstra 
def dijkstra_generator(graph, source, destination):

    distance = {node: float('inf') for node in graph.nodes} # Distance dictionary
    distance[source] = 0 # Set source distance to 0

    priority = [] # Priority queue
    heapq.heappush(priority, (0, source)) # Push source in

    visited = set() # Visited set

    while priority: # While we have nodes 
        current_distance, current_node = heapq.heappop(priority) # Pop current closest node and its distance

        if current_node == destination: # Check if we got to destination
            print(f"Destination reached at: {current_node}")
            return
    
        if current_node in visited: # If current was visited
            continue # Skip
        else: # If current wasn't visited
            visited.add(current_node) # Add current to visited
            yield current_node, visited # Yield to relax

            # Relaxation loop
            for neighbor in graph.successors(current_node): # Iterate through neighbors (graph.successors returns iterator)
                edge_weight = graph[current_node][neighbor][0]['length'] 
                new_distance = current_distance + edge_weight # Calculate distance to neighbor

                if new_distance < distance[neighbor]: # If distance to neighbor is less than the current minimum distance
                    distance[neighbor] = new_distance # Update current distance
                    heapq.heappush(priority, (new_distance, neighbor)) # Push to queue

        
            

fig.canvas.mpl_connect('button_press_event', on_click) # Click connection

plt.show()
