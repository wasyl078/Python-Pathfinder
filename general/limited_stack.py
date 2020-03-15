# imports
from typing import Any, List


# | used for enemy's AI, now abandoned | this is stack with max size
class LimitedUniqueStack(object):
    # constructor - initialize variables
    def __init__(self, max_size):
        self.actual_size = 0
        self.max_size = max_size
        self.stack: List[Any] = list()

    # peak on top element
    def top(self) -> Any:
        return self.stack[0]

    # returns top element and removes it from stack
    def pop(self) -> Any:
        if not self.is_empty():
            self.actual_size -= 1
            poped_element = self.stack.pop(0)
            return poped_element

    # put new element on stack's top, if stack is full - element on bottom is removed
    def push(self, new_element):
        if new_element not in self.stack:
            if self.is_full():
                self.stack.pop()
            else:
                self.actual_size += 1
            self.stack.insert(0, new_element)

    # checks if stack is empty
    def is_empty(self) -> bool:
        if self.max_size == 0:
            return True
        else:
            return self.actual_size == 0

    # checks if stack is full
    def is_full(self) -> bool:
        if self.max_size == 0:
            return False
        else:
            return self.actual_size == self.max_size

    # prints stack's elements
    def print_stack(self):
        print("Size: {}".format(self.actual_size))
        for elem in self.stack:
            print(elem)
