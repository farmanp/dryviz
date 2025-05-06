from rich.tree import Tree

def render_linked_list(head):
    """
    Build a Rich Tree visualization for a singly linked list.
    """
    def _build(node, tree):
        if node is None:
            tree.add("None")
            return
        subtree = tree.add(f"[{node.value}]")
        _build(node.next, subtree)

    root = Tree("LinkedList")
    _build(head, root)
    return root

def render_tree_node(node_data, tree_widget):
    """
    Recursively builds a Rich Tree for a generic tree node.
    Assumes node_data has a 'value' and 'children' (iterable) or 'left'/'right' attributes.
    """
    if node_data is None:
        tree_widget.add("None")
        return

    # Try to get a displayable value
    if hasattr(node_data, 'value'):
        display_value = node_data.value
    elif hasattr(node_data, 'key'):
        display_value = node_data.key
    elif isinstance(node_data, (int, str, float)):
        display_value = node_data
    else:
        display_value = str(node_data)[:30] # Fallback

    subtree = tree_widget.add(f"[{display_value}]")

    if hasattr(node_data, 'children') and node_data.children:
        for child in node_data.children:
            render_tree_node(child, subtree)
    elif hasattr(node_data, 'left') or hasattr(node_data, 'right'):
        if hasattr(node_data, 'left'):
            render_tree_node(node_data.left, subtree)
        if hasattr(node_data, 'right'):
            render_tree_node(node_data.right, subtree)

def render_tree(root_node, name="Tree"):
    """
    Build a Rich Tree visualization for a generic tree.
    """
    root_widget = Tree(name)
    render_tree_node(root_node, root_widget)
    return root_widget

def render_graph(graph_data, name="Graph"):
    """
    Build a Rich Tree visualization for a graph (adjacency list representation).
    Assumes graph_data is a dictionary where keys are nodes and values are lists of neighbors.
    """
    if not isinstance(graph_data, dict):
        return Tree(f"{name} (Unsupported format: expected dict)")

    tree = Tree(name)
    for node, neighbors in graph_data.items():
        node_subtree = tree.add(f"Node({node})")
        if neighbors:
            for neighbor in neighbors:
                node_subtree.add(f"-> {neighbor}")
        else:
            node_subtree.add(" (No outgoing edges)")
    return tree

def render_stack(stack_data, name="Stack"):
    """
    Build a Rich Tree visualization for a stack (list representation).
    Assumes stack_data is a list.
    """
    if not isinstance(stack_data, list):
        return Tree(f"{name} (Unsupported format: expected list)")

    tree = Tree(f"{name} (Top -> Bottom)")
    if not stack_data:
        tree.add(" (Empty)")
    else:
        for item in reversed(stack_data): # Display top of stack first
            tree.add(str(item))
    return tree

def render_dict(dict_data, name="Dictionary"):
    """
    Build a Rich Tree visualization for a dictionary.
    """
    if not isinstance(dict_data, dict):
        return Tree(f"{name} (Unsupported format: expected dict)")

    tree = Tree(name)
    if not dict_data:
        tree.add(" (Empty)")
    else:
        for key, value in dict_data.items():
            # Represent nested dictionaries or lists as sub-trees if simple, else just string
            if isinstance(value, dict):
                subtree = tree.add(f"[bold magenta]{key}[/]: dict")
                render_dict(value, subtree) # Recursive call for nested dicts
            elif isinstance(value, list):
                subtree = tree.add(f"[bold magenta]{key}[/]: list")
                # Basic list representation, could be expanded like render_stack if needed
                for i, item in enumerate(value):
                    subtree.add(f"[{i}]: {str(item)[:50]}") # Truncate long items
            else:
                tree.add(f"[bold magenta]{key}[/]: {str(value)[:100]}") # Truncate long values
    return tree