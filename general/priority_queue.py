# my own implementation of priority queue
class PriorityQueue(object):

    # initialization of queue - by using list
    def __init__(self, order_function):
        self.queue = list()
        self.actual_size = 0
        self.order_function = order_function

    # adding object at the end of the queue
    def enqueue(self, new_element):
        if self.is_empty():
            self.queue.append(new_element)
        else:
            for index in range(0, self.actual_size):
                if self.order_function(new_element, self.queue[index]):
                    self.queue.insert(index, new_element)
                    self.actual_size += 1
                    return
            self.queue.append(new_element)
        self.actual_size += 1

    # removing object from the queue
    def dequeue(self):
        if not self.is_empty():
            self.queue.pop(0)
            self.actual_size -= 1

    # checking first element in queue
    def first(self):
        if not self.is_empty():
            return self.queue[0]

    # checking if queue is empty
    def is_empty(self):
        return self.actual_size == 0

    # printing to console each queue eleement
    def print_queue(self):
        print("Queue actual size: {}, \nElements: ".format(self.actual_size))
        for elem in self.queue:
            print("-> {}".format(elem))
