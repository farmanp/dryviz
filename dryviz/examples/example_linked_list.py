"""
This example demonstrates operations on a singly linked list.
It covers:
1.  **Node Definition**: How a node in the linked list is structured (value and next pointer).
2.  **Linked List Class**: Basic operations like append, prepend, delete, and display.
3.  **Instantiation**: Creating a linked list.
4.  **Appending Nodes**: Adding 10, 20, and 30 to the end of the list.
5.  **Prepending Nodes**: Adding 5 to the beginning of the list.
6.  **Deleting Nodes**: Removing 20 from the list.
7.  **Displaying List**: Showing the list's contents after each major operation.

The `@dryviz` decorator is applied to the `LinkedList` class methods to visualize these operations.
"""
from dryviz.core import dryviz

class Node:
    """Represents a node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

@dryviz
class LinkedList:
    """A class to represent and manipulate a singly linked list."""
    def __init__(self):
        """Initializes an empty linked list."""
        self.head = None
        print("Step 1: Initialized an empty linked list.")

    def append(self, data):
        """Appends a new node with the given data to the end of the list."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            print(f"Appended node {data} (list was empty). List: {self._display_list_internals()})")
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        print(f"Appended node {data}. List: {self._display_list_internals()})")

    def prepend(self, data):
        """Prepends a new node with the given data to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        print(f"Prepended node {data}. List: {self._display_list_internals()})")

    def delete(self, key):
        """Deletes the first occurrence of a node with the given key."""
        current_node = self.head
        if current_node and current_node.data == key:
            self.head = current_node.next
            print(f"Deleted node {key} (it was the head). List: {self._display_list_internals()})")
            return
        prev_node = None
        while current_node and current_node.data != key:
            prev_node = current_node
            current_node = current_node.next
        if current_node is None:
            print(f"Node {key} not found for deletion. List: {self._display_list_internals()})")
            return
        prev_node.next = current_node.next
        print(f"Deleted node {key}. List: {self._display_list_internals()})")

    def _display_list_internals(self):
        """Helper method to get a string representation of the list for printing."""
        elements = []
        current_node = self.head
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        return " -> ".join(elements) if elements else "Empty"

    def display(self):
        """Prints the current state of the linked list."""
        # This method is primarily for the user to call explicitly if they want a final view.
        # The tutorial prints are handled within each operation for clarity.
        print(f"Current list state: {self._display_list_internals()}")

if __name__ == "__main__":
    print("--- Welcome to the Dryviz Linked List Operations Tutorial ---")
    print("This example demonstrates common linked list operations.")
    print("The @dryviz decorator on the LinkedList class will help visualize these.")

    # Create a linked list
    ll = LinkedList() # Step 1 print occurs here

    # Append nodes
    print("\nStep 2: Appending nodes 10, 20, 30")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.display() # Shows state after appends

    # Prepend a node
    print("\nStep 3: Prepending node 5")
    ll.prepend(5)
    ll.display() # Shows state after prepend

    # Delete a node
    print("\nStep 4: Deleting node 20")
    ll.delete(20)
    ll.display() # Shows state after delete

    # Attempt to delete a non-existent node
    print("\nStep 5: Attempting to delete non-existent node 100")
    ll.delete(100)
    ll.display() # Shows state after attempting to delete non-existent node

    print("\n--- Linked List Operations Visualization Complete ---")
    print("The visualization (if enabled by Dryviz) should have shown each operation.")
    print("Final state of the linked list:")
    ll.display()
    print("Explore further by adding more operations or modifying existing ones!")