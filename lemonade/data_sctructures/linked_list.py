from .node import Node

class LinkedList:
    def __init__(self):
        self._first: Node | None = None
        self._last: Node | None = None
        self._length: int = 0

    @property
    def first(self) -> Node | None:
        return self._first

    @property
    def last(self) -> Node | None:
        return self._last

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_empty(self) -> bool:
        return self._first is None

    def insert_at_end(self, data) -> None:
        new_node = Node(data=data)

        if self.is_empty:
            self._first = new_node
        else:
            self._last.next = new_node

        self._last = new_node
        self._length += 1

    def insert_at_beginning(self, data) -> None:
        new_node = Node(data=data)

        if self.is_empty:
            self._last = new_node
        else:
            new_node.next = self._first

        self._first = new_node
        self._length += 1

    def content(self) -> list:
        data = []
        current = self._first

        while current is not None:
            data.append(current.data)
            current = current.next

        return data

    def pop_first(self):
        if self.is_empty:
            raise Exception("Linked list is empty.")

        node = self._first

        self._first = self._first.next
        self._length -= 1

        if self.is_empty:
            self._last = None

        return node.data

    def pop_last(self):
        if self.is_empty:
            raise Exception("Linked list is empty.")

        if self._first == self._last:
            return self.pop_first()

        previous = None
        current = self._first

        while current.next is not None:
            previous = current
            current = current.next

        self._last = previous
        self._last.next = None
        self._length -= 1

        return current.data