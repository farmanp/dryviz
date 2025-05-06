from rich.tree import Tree

# --- Visualizer Registry ---
VISUALIZER_REGISTRY = []

def register_visualizer(condition_func, visualizer_func, priority=0):
    """
    Registers a new visualizer strategy.
    Visualizers with higher priority are checked first.
    """
    VISUALIZER_REGISTRY.append({'condition': condition_func, 'visualizer': visualizer_func, 'priority': priority})

# --- Condition Functions ---

def _is_linked_list_node(data):
    """Checks if data could be the head of a linked list."""
    if isinstance(data, (dict, list, tuple, set, str, int, float, bool)) or data is None:
        return False
    has_val_attr = hasattr(data, 'value') or hasattr(data, 'val') or hasattr(data, 'data')
    if not (has_val_attr and hasattr(data, 'next')):
        return False
    # Ensure it's not also a tree node with other children attributes
    if hasattr(data, 'children') or hasattr(data, 'left') or hasattr(data, 'right'):
        return False
    return True

def _is_tree_node(data):
    """Checks if data could be a tree node (and not better handled as a linked list)."""
    if isinstance(data, (dict, list, tuple, set, str, int, float, bool)) or data is None:
        return False
    has_val_attr = hasattr(data, 'value') or hasattr(data, 'val') or hasattr(data, 'key')
    has_children_attrs = hasattr(data, 'children') or hasattr(data, 'left') or hasattr(data, 'right')
    if not (has_val_attr and has_children_attrs):
        return False
    # If it also has 'next' but no other tree children, it might be a linked list handled by _is_linked_list_node
    if hasattr(data, 'next') and not (hasattr(data, 'children') or (hasattr(data, 'left') and data.left) or (hasattr(data, 'right') and data.right)):
        # This check helps differentiate if _is_linked_list_node is specific enough.
        # Given the priority system, if _is_linked_list_node is higher priority, this might not be strictly needed here.
        pass # Let priority decide if it also matches linked list structure
    return True

def _is_graph_dict(data):
    """Checks if data is a dictionary representing a graph (adjacency list)."""
    if not isinstance(data, dict) or not data:
        return False
    for _node, neighbors in data.items():
        if not isinstance(neighbors, (dict, list, set, tuple)):
            return False # Neighbors should be a collection
    return True

def _is_stack_list(data):
    """Checks if data is a list (could be a stack)."""
    return isinstance(data, list)

def _is_dictionary(data):
    """Checks if data is a dictionary."""
    return isinstance(data, dict)

# --- Internal Visualizer Implementations ---

def _build_rich_tree_for_linked_list_node(node, tree_widget):
    if node is None:
        tree_widget.add("None")
        return
    
    display_val = "Unknown"
    if hasattr(node, 'data'):
        display_val = node.data
    elif hasattr(node, 'value'):
        display_val = node.value
    elif hasattr(node, 'val'):
        display_val = node.val
        
    subtree = tree_widget.add(f"[{display_val}]")
    if hasattr(node, 'next'):
        _build_rich_tree_for_linked_list_node(node.next, subtree)

def _visualize_linked_list_internal(head, name):
    root_widget = Tree(name)
    _build_rich_tree_for_linked_list_node(head, root_widget)
    return root_widget

def _build_rich_tree_for_generic_node(node_data, tree_widget):
    if node_data is None:
        tree_widget.add("None")
        return

    display_value = "Unknown"
    if hasattr(node_data, 'value'):
        display_value = node_data.value
    elif hasattr(node_data, 'val'):
        display_value = node_data.val
    elif hasattr(node_data, 'key'):
        display_value = node_data.key
    elif isinstance(node_data, (int, str, float, bool)):
        display_value = node_data
    else:
        display_value = str(node_data)[:30]

    subtree = tree_widget.add(f"[{display_value}]")

    if hasattr(node_data, 'children') and node_data.children:
        for child in node_data.children:
            _build_rich_tree_for_generic_node(child, subtree)
    elif hasattr(node_data, 'left') or hasattr(node_data, 'right'): # Binary tree nodes
        if hasattr(node_data, 'left'):
            _build_rich_tree_for_generic_node(node_data.left, subtree)
        else: # Add a placeholder if only right child exists for structure
            subtree.add("left: None")
            
        if hasattr(node_data, 'right'):
            _build_rich_tree_for_generic_node(node_data.right, subtree)
        else: # Add a placeholder if only left child exists
            subtree.add("right: None")


def _visualize_tree_internal(root_node_data, name):
    root_widget = Tree(name)
    _build_rich_tree_for_generic_node(root_node_data, root_widget)
    return root_widget

def _visualize_graph_internal(graph_data, name):
    tree = Tree(name)
    if not graph_data:
        tree.add("(Empty Graph)")
        return tree
    for node, neighbors in graph_data.items():
        node_subtree = tree.add(f"Node({node})")
        if isinstance(neighbors, dict): 
            if neighbors:
                for neighbor, weight in neighbors.items():
                    node_subtree.add(f"-> {neighbor} (weight: {weight})")
            else:
                node_subtree.add(" (No outgoing edges)")
        elif isinstance(neighbors, (list, set, tuple)):
            if neighbors:
                for neighbor in neighbors:
                    node_subtree.add(f"-> {neighbor}")
            else:
                node_subtree.add(" (No outgoing edges)")
        else:
            node_subtree.add(f"(Neighbors: {str(neighbors)[:50]})")
    return tree

def _visualize_stack_internal(stack_data, name):
    tree = Tree(f"{name} (Top -> Bottom)")
    if not stack_data:
        tree.add(" (Empty)")
    else:
        for item in reversed(stack_data): # Display top of stack first
            tree.add(str(item))
    return tree

def _visualize_dictionary_internal(dict_data, name):
    tree = Tree(name)
    if not dict_data:
        tree.add(" (Empty)")
    else:
        for key, value in dict_data.items():
            key_str = f"[bold magenta]{str(key)}[/]"
            if isinstance(value, dict):
                # Create a new node for the key, then add the visualization of the nested dictionary.
                # The name for the nested visualization can be simple like "dict" or more descriptive.
                nested_vis_name = "dict" 
                dict_subtree_node = tree.add(f"{key_str}:")
                nested_dict_vis = generate_visualization(value, name=nested_vis_name)
                dict_subtree_node.add(nested_dict_vis)
            elif isinstance(value, list):
                nested_vis_name = "list"
                list_node = tree.add(f"{key_str}:")
                nested_list_vis = generate_visualization(value, name=nested_vis_name)
                list_node.add(nested_list_vis)
            else:
                tree.add(f"{key_str}: {str(value)[:100]}") # Truncate long values
    return tree

# --- Main Visualization Dispatcher ---
def generate_visualization(data, name="Data"):
    """
    Generates a Rich Tree visualization for the given data using registered visualizers.
    """
    # Sort by priority (descending) for stable dispatch order
    # This sort should ideally happen once after all registrations.
    # For now, sorting here ensures it's always correctly ordered before dispatch.
    # A more performant approach would be to sort once at module load time.
    sorted_registry = sorted(VISUALIZER_REGISTRY, key=lambda x: x['priority'], reverse=True)

    for item in sorted_registry:
        if item['condition'](data):
            return item['visualizer'](data, name)

    # Fallback for unsupported types or if no visualizer matched
    fallback_tree = Tree(f"{name} (Type: {type(data).__name__})")
    try:
        fallback_tree.add(str(data)[:200]) # Basic string representation, truncated
    except (TypeError, ValueError, AttributeError, OverflowError, RecursionError) as e: # More specific exceptions
        fallback_tree.add(f"<Error converting to string: {e}>")
    return fallback_tree

# --- Register Visualizers (Order by priority) ---
# Higher priority means checked earlier.
register_visualizer(_is_linked_list_node, _visualize_linked_list_internal, priority=30)
register_visualizer(_is_tree_node, _visualize_tree_internal, priority=20)
register_visualizer(_is_graph_dict, _visualize_graph_internal, priority=15)
register_visualizer(_is_dictionary, _visualize_dictionary_internal, priority=10) 
register_visualizer(_is_stack_list, _visualize_stack_internal, priority=5) 

# Sort registry once after all registrations
VISUALIZER_REGISTRY.sort(key=lambda x: x['priority'], reverse=True)


# --- Public API Functions (as used by core.py or examples) ---

def render_linked_list(head):
    """Build a Rich Tree visualization for a singly linked list."""
    return generate_visualization(head, name="LinkedList")

# render_tree_node was an internal helper, its logic is now in _build_rich_tree_for_generic_node.
# It is removed from the public API as it's not used by core.py or examples.

def render_tree(root_node, name="Tree"):
    """Build a Rich Tree visualization for a generic tree."""
    return generate_visualization(root_node, name=name)

def render_graph(graph_data, name="Graph"):
    """
    Build a Rich Tree visualization for a graph (adjacency list representation).
    Assumes graph_data is a dictionary where keys are nodes and values are lists/dicts of neighbors.
    """
    if not isinstance(graph_data, dict): # Retain explicit type check for public API
        return Tree(f"{name} (Unsupported format: expected dict)")
    return generate_visualization(graph_data, name=name)

def render_stack(stack_data, name="Stack"):
    """
    Build a Rich Tree visualization for a stack (list representation).
    Assumes stack_data is a list.
    """
    if not isinstance(stack_data, list): # Retain explicit type check
        return Tree(f"{name} (Unsupported format: expected list)")
    return generate_visualization(stack_data, name=name)

def render_dict(dict_data, name="Dictionary"):
    """
    Build a Rich Tree visualization for a dictionary.
    """
    if not isinstance(dict_data, dict): # Retain explicit type check
        return Tree(f"{name} (Unsupported format: expected dict)")
    return generate_visualization(dict_data, name=name)