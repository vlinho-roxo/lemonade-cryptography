from .linked_list import LinkedList

class Queue(LinkedList):
    def enqueue(self, data) -> None:
        self.insert_at_end(data)

    def dequeue(self):
        if self.is_empty:
            raise Exception("Queue is empty.")

        return self.pop_first()

    def first(self):
        if self.is_empty:
            raise Exception("Queue is empty.")

        return self._first.data

    def last(self):
        if self.is_empty:
            raise Exception("Queue is empty.")

        return self._last.data