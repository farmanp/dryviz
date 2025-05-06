"""
Demonstrates basic stack operations using a Python list.
This function shows the following stack operations:
1. Creating an empty stack
2. Pushing elements onto the stack (apple, banana, cherry, date)
3. Popping elements from the stack
4. Tracking the stack state after each operation
The function prints the state of the stack after each operation and returns
the final stack state after all operations are completed.
Returns:
    list: The final state of the stack after all push and pop operations
"""

from dryviz.core import dryviz

@dryviz

def manage_stack_operations():
    # Step 1: Create an empty stack. A Python list can be used as a stack.
    stack = []
    print("Step 1: Created an empty stack. Current stack:", stack)

    # Step 2: Push 'apple' onto the stack.
    # The append() method adds an element to the end of the list (top of the stack).
    stack.append("apple")
    print("Step 2: Pushed 'apple' onto the stack. Current stack:", stack)

    # Step 3: Push 'banana' onto the stack.
    stack.append("banana")
    print("Step 3: Pushed 'banana' onto the stack. Current stack:", stack)

    # Step 4: Push 'cherry' onto the stack.
    stack.append("cherry")
    print("Step 4: Pushed 'cherry' onto the stack. Current stack:", stack)

    # Step 5: Pop an element from the stack.
    # The pop() method removes and returns the last element of the list (top of the stack).
    popped_item = stack.pop()
    print(f"Step 5: Popped '{popped_item}' from the stack. Current stack:", stack)

    # Step 6: Push 'date' onto the stack.
    stack.append("date")
    print("Step 6: Pushed 'date' onto the stack. Current stack:", stack)

    # Step 7: Pop another element from the stack.
    popped_item_2 = stack.pop()
    print(f"Step 7: Popped '{popped_item_2}' from the stack. Current stack:", stack)
    
    # Step 8: Pop one more element from the stack.
    popped_item_3 = stack.pop()
    print(f"Step 8: Popped '{popped_item_3}' from the stack. Current stack:", stack)

    # Final stack state
    # The stack now contains the remaining elements after all operations.
    final_stack = stack
    print("All stack operations are complete.")
    return final_stack

if __name__ == "__main__":
    print("--- Welcome to the Dryviz Stack Operations Tutorial ---")
    print("This example demonstrates how a stack works using a Python list.")
    print("The @dryviz decorator will help visualize these operations.")
    
    result_stack = manage_stack_operations()
    
    print("--- Stack Operations Visualization Complete ---")
    print("The visualization (if enabled by Dryviz) should have shown each step.")
    print("Final state of the stack:", result_stack)
    print("Feel free to modify this example to experiment further!")
