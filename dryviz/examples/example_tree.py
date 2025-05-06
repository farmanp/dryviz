
from dryviz.core import dryviz

class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def add_child(self, node):
        self.children.append(node)

@dryviz
def build_sample_tree():
    root = TreeNode("A")
    b = TreeNode("B")
    c = TreeNode("C")
    d = TreeNode("D")
    e = TreeNode("E")
    f = TreeNode("F")
    g = TreeNode("G")

    root.add_child(b)
    root.add_child(c)

    b.add_child(d)
    b.add_child(e)

    c.add_child(f)
    c.add_child(g)
    
    # Demonstrate a slightly different tree structure (binary-like)
    # for the visualizer to handle via left/right attributes
    # Note: Our current TreeNode is generic, but we can create
    # a specific instance that the visualizer might pick up
    # if it had 'left' and 'right' attributes.
    # For now, this will be rendered via 'children'
    
    # Let's create another tree to show that
    simple_binary_root = TreeNode("Root")
    simple_binary_root.left = TreeNode("Left Child") # Visualizer might not see this as 'left' yet
    simple_binary_root.right = TreeNode("Right Child")# Visualizer might not see this as 'right' yet
    # To make the current visualizer see it, we'd need to add them to children
    # or modify the visualizer to check for .left and .right explicitly if .children is not present.
    # The current tree visualizer in visuals.py already checks for .left and .right.

    # Let's make a node that explicitly uses left/right for the visualizer
    class BinaryNode:
        def __init__(self, value, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right

    binary_root = BinaryNode("BinaryRoot")
    binary_root.left = BinaryNode("L")
    binary_root.right = BinaryNode("R")
    binary_root.left.left = BinaryNode("LL")
    
    processed_tree = root
    another_tree = binary_root
    return processed_tree, another_tree

if __name__ == "__main__":
    print("Visualizing tree construction:")
    final_tree, b_tree = build_sample_tree()
    print("--- Tree construction complete ---")
    print("Final Tree Structure (root):", final_tree.value)
    print("Binary Tree Structure (binary_root):", b_tree.value)
