# my own implementation of priority queue


class PriorityQueue(object):

    # initialization of queue - using array
    def __init__(self, size, predicate):
        self.max_size = size
        self.queue = list()
        self.actual_size = 0
        self.predicate = predicate

    # adding object at the end of the queue
    def enqueue(self, new_element):
        if self.is_full():
            raise FullQueueException(self.max_size)
        else:
            if self.actual_size == 0:
                self.queue.append(new_element)
                self.actual_size += 1
            else:
                for i in range(0, self.actual_size):
                    if self.predicate(new_element, self.queue[i]):
                        self.queue.insert(i, new_element)
                        self.actual_size += 1
                        return
                self.queue.append(new_element)
                self.actual_size += 1

    # removing object from the queue
    def dequeue(self):
        if self.is_empty():
            pass
            # raise EmnptyQeueuException()
        else:
            self.queue.pop(0)
            self.actual_size -= 1

    # checking first element in queue
    def first(self):
        if self.is_empty():
            pass
            # raise EmnptyQeueuException()
        else:
            return self.queue[0]

    # checking if queue is empty
    def is_empty(self):
        return self.actual_size == 0

    # checking if queue is full
    def is_full(self):
        return self.actual_size == self.max_size

    def print_queue(self):
        print("Queue actual size: {}".format(self.actual_size))
        for elem in self.queue:
            print(elem)


# exceptions classes

# may be called when adding object to queue
class FullQueueException(Exception):

    def __init__(self, size):
        super().__init__("Queue is full - only {} slots available".format(size))


# may be called when object is removed / first object in queue is checked
class EmnptyQeueuException(Exception):

    def __init__(self):
        super().__init__("Queue is empty - nothing inside")
