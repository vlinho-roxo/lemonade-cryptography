from __future__ import annotations

class Node:
    def __init__(self, data, next : Node = None):
        self._data = data
        self._next = next
        
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data) -> None:
        self._data = data
        
    @property
    def next(self) -> Node:
        return self._next
    
    @next.setter
    def next(self, next : Node) -> None:
        self._next = next