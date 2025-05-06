from dryviz.core import dryviz

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

@dryviz
def example_list():
    head = Node(10, Node(20, Node(30)))
    print("Example complete!")

if __name__ == "__main__":
    example_list()