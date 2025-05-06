from dryviz.core import dryviz

@dryviz
def build_sample_graph():
    graph = {}
    print("Initial graph:", graph)

    # Add nodes and edges
    graph['A'] = ['B', 'C']
    print("Added A -> B, C:", graph)

    graph['B'] = ['A', 'D', 'E']
    print("Added B -> A, D, E:", graph)

    graph['C'] = ['A', 'F']
    print("Added C -> A, F:", graph)

    graph['D'] = ['B']
    print("Added D -> B:", graph)

    graph['E'] = ['B', 'F']
    print("Added E -> B, F:", graph)

    graph['F'] = ['C', 'E']
    print("Added F -> C, E:", graph)
    
    graph['G'] = [] # Node with no outgoing edges
    print("Added G (isolated):", graph)

    # Simulate removing an edge (e.g., A -> C)
    if 'C' in graph.get('A', []):
        graph['A'].remove('C')
    print("Removed A -> C:", graph)

    # Simulate removing a node (e.g., D and its incident edges)
    if 'D' in graph:
        del graph['D']
        # Also remove edges pointing to D from other nodes
        for node in graph:
            if 'D' in graph[node]:
                graph[node].remove('D')
    print("Removed node D and its edges:", graph)
    
    final_graph = graph
    return final_graph

if __name__ == "__main__":
    print("Visualizing graph construction and modification:")
    result_graph = build_sample_graph()
    print("--- Graph operations complete ---")
    print("Final graph structure:", result_graph)
