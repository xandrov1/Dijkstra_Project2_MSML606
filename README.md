# Dijkstra's Algorithm Visualization for Manhattan's Road Network

***AI USAGE STATEMENT: GENERATIVE AI WAS NOT USED IN THE MAKING OF THIS REPORT OR CODE***

Our program for MSML606's extra credit project 2 is an interactive visualization of Dijkstra's shortest-path algorithm running on a real road network. Click two points on the map to watch the algorithm explore the network in real time, then see the shortest path highlighted once the destination is reached.

> **Authors:** Alessandro Vivaldi & Andrew Liu

---

## Requirements

- Python 3.8+
- [OSMnx](https://osmnx.readthedocs.io/)
- [NetworkX](https://networkx.org/)
- [Matplotlib](https://matplotlib.org/)

Install dependencies with:

```bash
pip install osmnx networkx matplotlib
```

---

## Setup

**1. Download the road network graph**

When you run the program for the first time, the first step is to download and save the Inwood road network. Uncomment the download block near the top of `Dijkstra_visualization.py`:

```python
place = ox.graph_from_place("Inwood, New York, USA")
ox.save_graphml(place, "inwood.graphml")
```

After that, run the script once to generate `inwood.graphml`, then re-comment that block. Every run after will be able to load from the local file.

**2. Run the visualization**

```bash
python Dijkstra_visualization.py
```

---

## How The Program Works

Our Python script displays a real road network of the Inwood neighborhood in Manhattan (sourced from OpenStreetMap via OSMnx). At each road intersection, there is a dedicated node, while at each road segment, there is a weighted edge. Each edge represents the road's actual length in meters.

When the user clicks on a destination from the map, the following happens:

1. Starting from the source node, Dijkstra's algorithm works by maintaining a min-heap priority queue of unvisited nodes. Each of these nodes are put in order by its current known shortest distance.
2. During each step of the process, the algorithm first pops the closest unvisited node, then relaxes its neighbors, and then updates distances if a new shortest path is discovered.
3. Since the algorithm is implemented as a Python generator, it can animate each step it takes on a live map.
4. Once the algorithm reaches the desired destination, the shortest path is remade by backtracking through a `previous` dictionary and is then rendered in yellow.

Additionally, the shortest path will always be optimal since all edge weights must be non-negative as they are based on real-life road lengths.

---

## Information on our Algorithm

Dijkstra's algorithm is a greedy algorithm for weighted graphs. Its use case in our program is as follows:

- Uses Python's `heapq` module as a min-heap priority queue for O(log n) node extraction.
- Tracks a `previous` dictionary for path reconstruction.
- Uses `graph.successors()` for neighbor traversal on a directed graph.
- Guaranteed optimal for non-negative edge weights (road lengths in meters).

We chose Inwood over using the entire city because Manhattan's full road network is far too dense to visualize clearly. Inwood provided us with a better representation of the area while being a legible subset.

**One-way street handling:** The graph is directed, and `graph.successors()` only returns neighbors reachable via outgoing directed edges. In turn, the algorithm naturally respects one-way streets, meaning that it will never traverse a road in the wrong direction. Additionally, edge directions are not labeled in the visualization to avoid severe node density, but they are present throughout the traversal stage.

**When no path exists:** If the priority queue has been emptied before reaching the destination, the algorithm prints `"No path found to destination"` and the generator ends. This usually happens when the destination node is unreachable from the source, following directed edges.
