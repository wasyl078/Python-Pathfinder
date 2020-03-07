class LimitedUniqueStack(object):
    def __init__(self, max_size):
        self.actual_size = 0
        self.max_size = max_size
        self.stack = list()

    def top(self):
        return self.stack[0]

    def pop(self):
        if not self.is_empty():
            self.actual_size -= 1
            poped_element = self.stack.pop(0)
            return poped_element

    def push(self, new_element):
        if new_element not in self.stack:
            if self.is_full():
                self.stack.pop()
            else:
                self.actual_size += 1
            self.stack.insert(0, new_element)

    def is_empty(self):
        return self.actual_size == 0

    def is_full(self):
        return self.actual_size == self.max_size

    def print_stack(self):
        print("Size: {}".format(self.actual_size))
        for elem in self.stack:
            print(elem)
