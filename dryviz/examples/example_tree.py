"""
This example demonstrates operations on a binary tree data structure.
It covers:
1.  **Node Definition**: How a tree node is structured (value, left child, right child).
2.  **Tree Insertion**: How nodes are added to maintain binary search tree properties.
3.  **Tree Traversal**: In-order traversal to display the tree's elements.
4.  **Visualization**: The `@dryviz` decorator is used on the `insert` and `inorder_traversal` methods
    of the `Node` class to visualize tree construction and traversal.

Key operations shown:
- Creating an empty tree (root is None).
- Inserting elements: 50, 30, 20, 40, 70, 60, 80.
- Performing an in-order traversal to print the sorted elements.
"""
from dryviz.core import dryviz

class Node:
    """Represents a node in a binary tree."""
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        # Initial print for node creation can be tricky with @dryviz on methods.
        # We'll focus on prints within insert and traversal for clarity of operation.

    @dryviz
    def insert(self, key):
        """Inserts a new key into the binary tree rooted at this node."""
        print(f"Attempting to insert {key} into the subtree rooted at {self.val}.")
        if self.val:
            if key < self.val:
                if self.left is None:
                    self.left = Node(key)
                    print(f"Inserted {key} as the left child of {self.val}.")
                else:
                    print(f"{key} < {self.val}, moving to the left subtree of {self.val}.")
                    self.left.insert(key)
            elif key > self.val:
                if self.right is None:
                    self.right = Node(key)
                    print(f"Inserted {key} as the right child of {self.val}.")
                else:
                    print(f"{key} > {self.val}, moving to the right subtree of {self.val}.")
                    self.right.insert(key)
            else:
                print(f"Key {key} is already in the tree (value of current node {self.val}).")
        else:
            # This case should ideally not be hit if the root is initialized correctly.
            self.val = key
            print(f"Initialized tree with root {key} (current node was empty).")

    @dryviz
    def inorder_traversal(self, current_node):
        """Performs an in-order traversal of the tree and collects node values."""
        res = []
        if current_node:
            # Traverse left subtree
            if current_node.left:
                print(f"Traversing left subtree of {current_node.val}.")
            res = self.inorder_traversal(current_node.left)
            
            # Visit root node
            print(f"Visiting node {current_node.val}.")
            res.append(current_node.val)
            
            # Traverse right subtree
            if current_node.right:
                print(f"Traversing right subtree of {current_node.val}.")
            res = res + self.inorder_traversal(current_node.right)
        return res

if __name__ == "__main__":
    print("--- Welcome to the Dryviz Binary Tree Operations Tutorial ---")
    print("This example demonstrates how a binary search tree is built and traversed.")
    print("The @dryviz decorator on Node methods will help visualize these operations.")

    # Step 1: Create the root of the tree
    print("\nStep 1: Creating the root node with value 50.")
    root = Node(50)
    # Dryviz will capture the state after this initial node creation if the class itself is decorated,
    # or after the first decorated method call.

    # Step 2: Insert more nodes
    # The insert method is decorated, so each insertion will be visualized.
    print("\nStep 2: Inserting nodes 30, 20, 40, 70, 60, 80.")
    nodes_to_insert = [30, 20, 40, 70, 60, 80]
    for node_val in nodes_to_insert:
        print(f"\n--- Inserting {node_val} ---")
        root.insert(node_val)

    print("\nAll nodes inserted. Current tree structure (conceptual based on insertions):")
    # A simple print of the root value, actual structure is in Dryviz visualization
    print(f"Root of the tree is: {root.val}") 

    # Step 3: Perform in-order traversal
    # The inorder_traversal method is decorated.
    print("\nStep 3: Performing in-order traversal.")
    print("In-order traversal visits nodes in ascending order for a BST.")
    traversed_nodes = root.inorder_traversal(root)
    
    print("\n--- Binary Tree Operations Visualization Complete ---")
    print("The visualization (if enabled by Dryviz) should have shown:")
    print("1. Each node insertion and how it finds its place in the BST.")
    print("2. The process of in-order traversal (left-root-right).")
    print("Final in-order traversal result:", traversed_nodes)
    print("Experiment by inserting different values or trying other traversal methods!")
