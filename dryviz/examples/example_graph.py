"""
This example demonstrates how to create and manipulate a graph data structure.
It showcases the following operations:
1.  **Initialization**: Creating an empty graph.
2.  **Adding Nodes**: Incorporating 'A', 'B', 'C', 'D', and 'E' into the graph.
3.  **Adding Edges**: Establishing connections between nodes, such as 'A' to 'B' with a weight of 1.
4.  **Graph State**: Displaying the graph's structure after each significant operation.

The `@dryviz` decorator is used to visualize these changes, offering a clear view of the graph's evolution.
"""
from dryviz.core import dryviz

@dryviz
def manage_graph_operations():
    """
    Manages and demonstrates operations on a graph.

    This function initializes a graph, adds nodes and edges, and prints the
    state of the graph at each step to illustrate how graph operations work.
    The @dryviz decorator helps in visualizing these steps.

    Returns:
        dict: The final state of the graph after all operations.
    """
    # Step 1: Initialize an empty graph.
    # A graph is represented as a dictionary where keys are nodes and
    # values are dictionaries of neighbors with their corresponding edge weights.
    graph = {}
    print("Step 1: Initialized an empty graph. Current graph:", graph)

    # Step 2: Add nodes to the graph.
    # We'll add nodes 'A', 'B', 'C', 'D', and 'E'.
    # Initially, these nodes have no edges.
    nodes = ['A', 'B', 'C', 'D', 'E']
    for node in nodes:
        if node not in graph:
            graph[node] = {}
    print(f"Step 2: Added nodes {', '.join(nodes)}. Current graph:", graph)

    # Step 3: Add edges to the graph.
    # Edges are directed and have weights.
    # For example, ('A', 'B', 1) means an edge from 'A' to 'B' with weight 1.

    # Add edge A -> B with weight 1
    graph['A']['B'] = 1
    print("Step 3a: Added edge A -> B with weight 1. Current graph:", graph)

    # Add edge A -> C with weight 4
    graph['A']['C'] = 4
    print("Step 3b: Added edge A -> C with weight 4. Current graph:", graph)

    # Add edge B -> C with weight 2
    graph['B']['C'] = 2
    print("Step 3c: Added edge B -> C with weight 2. Current graph:", graph)

    # Add edge B -> D with weight 5
    graph['B']['D'] = 5
    print("Step 3d: Added edge B -> D with weight 5. Current graph:", graph)

    # Add edge C -> E with weight 3
    graph['C']['E'] = 3
    print("Step 3e: Added edge C -> E with weight 3. Current graph:", graph)

    # Add edge D -> E with weight 1
    graph['D']['E'] = 1
    print("Step 3f: Added edge D -> E with weight 1. Current graph:", graph)

    print("All graph operations are complete.")
    return graph

if __name__ == "__main__":
    print("--- Welcome to the Dryviz Graph Operations Tutorial ---")
    print("This example demonstrates how a graph is built and modified.")
    print("We'll add nodes and weighted edges, visualizing each step with @dryviz.")

    final_graph = manage_graph_operations()

    print("--- Graph Operations Visualization Complete ---")
    print("The visualization (if enabled by Dryviz) should have shown the graph's evolution.")
    print("Final state of the graph:", final_graph)
    print("You can experiment by adding more nodes or edges, or by changing weights.")
