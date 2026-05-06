import osmnx as ox
import matplotlib.pyplot as plt 
from matplotlib import animation
import networkx as nx
import heapq


# To download and save graph to .gramphml
# try:
#     place = ox.graph_from_place("Inwood, New York, USA") # Changed to smaller part of manhattan because all of manhattan isn't clearly visible, nodes are too dense
#     ox.save_graphml(place, "inwood.graphml") # Inwood is not too big not too small and part of manhattan

# except Exception as e: 
#     print(f"Something went wrong: {e}") 

# File load from local
try:
    place = ox.load_graphml("inwood.graphml")
    print(f"Graph loaded")
except Exception as e:
    print(f"Something went wrong: {e}")

fig, ax = ox.plot_graph(place, show=False, figsize=(12, 16), node_size=15, edge_linewidth=0.5, edge_color='white', bgcolor='black') # Get fig and ax to connect click event; stop automatic plotting with show
original_collections = set(ax.collections) # Save original
source = None
destination = None
gen = None

# Click interaction
def on_click(event):
    global source, destination, gen # Set globals

    # print(event.xdata, event.ydata) # Print coordinates

    # Coordinates
    x = event.xdata 
    y = event.ydata
    # node = ox.nearest_nodes(place, x,y) # Snap click to nearest node
    # print(f"Node: {node}") # Print node
    
    if source is None: # First click is source
        source = ox.nearest_nodes(place, x, y)
        ax.scatter(place.nodes[source]['x'], place.nodes[source]['y'], c='green', s=20, zorder=7) # Mark source
    elif destination is None: # Second is destination
        destination = ox.nearest_nodes(place, x, y)
        ax.scatter(place.nodes[destination]['x'], place.nodes[destination]['y'], c='blue', s=20, zorder=7) # Mark destination
        print(f"Source: {source} - Destination: {destination}")
        gen = dijkstra_generator(place, source, destination) # Trigger 
    else: # Third is reset
        source = None
        destination = None
        print("Reset")
        gen = None # Drop old process and reset node colors
        for collection in ax.collections[:]:
            if collection not in original_collections:
                collection.remove()
        for line in ax.lines[:]:
            line.remove()
        ax.figure.canvas.draw_idle()

# Dijkstra generator
def dijkstra_generator(graph, source, destination):

    distance = {node: float('inf') for node in graph.nodes} # Distance dictionary
    distance[source] = 0 # Set source distance to 0
    previous = {node: None for node in graph.nodes} # Previous dictionary to take care of edges 

    priority = [] # Priority queue
    heapq.heappush(priority, (0, source)) # Push source in

    visited = set() # Visited set

    while priority: # While we have nodes 
        current_distance, current_node = heapq.heappop(priority) # Pop current closest node and its distance

        if current_node == destination: # Check if we got to destination & track path if we did
            path = []
            node = destination
            while node is not None:
                path.append(node)
                node = previous[node]
            path.reverse()
            yield current_node, visited, [], previous  # regular yield
            yield current_node, visited, path, previous  # destination yield
            print(f"Destination reached at: {current_node}")
            return
    
        if current_node in visited: # If current was visited
            continue # Skip
        else: # If current wasn't visited
            visited.add(current_node) # Add current to visited
            yield current_node, visited, [], previous  # regular yield

            # Relaxation loop
            for neighbor in graph.successors(current_node): # Iterate through neighbors (graph.successors returns iterator)
                edge_weight = graph[current_node][neighbor][0]['length'] 
                new_distance = current_distance + edge_weight # Calculate distance to neighbor

                if new_distance < distance[neighbor]: # If distance to neighbor is less than the current minimum distance
                    distance[neighbor] = new_distance # Update current distance
                    previous[neighbor] = current_node # Record previous 
                    heapq.heappush(priority, (new_distance, neighbor)) # Push to queue

    print(f"No path found to destination") # No path found

# Animation of nodes 
def animate(frame):
    if gen is None:
        return
    
    try: 
        current_node, visited, path, previous = next(gen)
        xs = [place.nodes[n]['x'] for n in visited]
        ys = [place.nodes[n]['y'] for n in visited]
        ax.scatter(xs, ys, c='red', s=10, zorder=5) # Node coloring
        prev_node = previous[current_node]
        if prev_node is not None: # Explored paths drawing
            x_vals = [place.nodes[prev_node]['x'], place.nodes[current_node]['x']]
            y_vals = [place.nodes[prev_node]['y'], place.nodes[current_node]['y']]
            ax.plot(x_vals, y_vals, c='purple', linewidth=1, zorder=4)
        if path: # Path drawing
            xs = [place.nodes[n]['x'] for n in path]
            ys = [place.nodes[n]['y'] for n in path]
            ax.plot(xs, ys, c='yellow', linewidth=2, zorder=6)
    except StopIteration:
        return

fig.canvas.mpl_connect('button_press_event', on_click) # Click connection
ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False) # Connect animate to FuncAnimation
plt.show()
