from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")

_RED = True
_BLACK = False

@dataclass(slots=True)
class _Node(Generic[K, V]):
    key: K
    value: V
    color: bool = _RED
    left: Optional[_Node[K, V]] = None
    right: Optional[_Node[K, V]] = None
    size: int = 1

class RedBlackTree(Generic[K, V]):
    def __int__(self, items: Optional[Iterable[tuple[K, V]]] = None) -> None:
        self._root: Optional[_Node[K, V]] = None
        if items is not None:
            for key, value in items:
                self.insert(key, value)
    
    def __len__(self) -> int:
        return self._size(self._root)
    
    def __contains__(self, key) -> bool:
        return self.contains(key)
    
    def __bool__(self) -> bool:
        return self._root is not None
    
    def clear(self) -> None:
        self._root = None

    def contains(self, key: K) -> bool:
        return self._get_node(key) is not None
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        node = self._get_node(key)
        return default if node is None else node.value
    
    def insert(self, key: K, value: V) -> None:
        self._root = self._insert(self._root, key, value)
        if self._root is not None:
            self._root.color = _BLACK

    def remove(self, key: K) -> None:
        if not self.contains(key):
            raise KeyError(f"Key not found: {key!r}")
        
        if self._root is not None and not self._is_red(self._root.left) and not self._is_red(self._root.right):
            self._root.color = _RED

        self._root = self._delete(self._root, key)
        if self._root is not None:
            self._root.color = _BLACK

    
        
        
