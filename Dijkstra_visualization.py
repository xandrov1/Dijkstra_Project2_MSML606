import osmnx as ox
import matplotlib.pyplot as plt 
import networkx as nx


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

# Click interaction
def on_click(event):
    print(event.xdata, event.ydata) # Print coordinates

fig.canvas.mpl_connect('button_press_event', on_click) # Click connection

plt.show()
