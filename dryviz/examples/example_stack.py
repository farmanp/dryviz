
from dryviz.core import dryviz

@dryviz
def manage_stack_operations():
    stack = []
    print("Initial stack:", stack)

    stack.append("apple")
    print("Pushed apple:", stack)

    stack.append("banana")
    print("Pushed banana:", stack)

    stack.append("cherry")
    print("Pushed cherry:", stack)

    popped_item = stack.pop()
    print(f"Popped {popped_item}:", stack)

    stack.append("date")
    print("Pushed date:", stack)

    popped_item_2 = stack.pop()
    print(f"Popped {popped_item_2}:", stack)
    
    popped_item_3 = stack.pop()
    print(f"Popped {popped_item_3}:", stack)

    # Final stack state
    final_stack = stack
    return final_stack

if __name__ == "__main__":
    print("Visualizing stack operations:")
    result_stack = manage_stack_operations()
    print("--- Stack operations complete ---")
    print("Final stack:", result_stack)
