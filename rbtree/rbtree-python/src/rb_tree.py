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

    def min_item(self) -> tuple[K, V]:
        if self._root is None:
            raise ValueError("Tree is empty")
        node = self._min_node(self._root)
        return node.key, node.value
        
    def max_item(self) -> tuple[K, V]:
        if self._root is None:
            raise ValueError("Tree is empty")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key, node.value
    
    def inorder_items(self) -> list[tuple[K, V]]:
        result: list[tuple[K, V]] = []
        self.collect_inorder(self._root, result)
        return result
    
    def keys(self) -> list[K]:
        return [key for key, _ in self._inorder_items()]

    def values(self) -> list[V]:
        return [value for _, value in self._inorder_items()]

    def items(self) -> Iterator[tuple[K, V]]:
        yield from self._iter_inorder(self._root)

    def validate(self) -> bool:
        if self._root is None:
            return True
        
        assert not self._is_red(self._root), "Root must be black"
        self._validate_bst(self._root, None, None)
        black_height = self._validate_invariants(self._root)
        assert black_height >= 1
        self._validate_sizes(self._root)
        return True
    
    @staticmethod
    def _is_red(node: Optional[_Node[K, V]]) -> bool:
        return node is not None and node.color == _RED
    
    @staticmethod
    def _size(node: Optional[_Node[K, V]]) -> int:
        return 0 if node is None else node.size
    
    def _get_node(self, key: K) -> Optional[_Node[K, V]]:
        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None
    
    def _rotate_left(self, h: _Node[K, V]) -> _Node[K, V]:
        assert h.right is not None
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = _RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x
    
    def _rotate_right(self, h: _Node[K, V]) -> _Node[K, V]:
        assert h.left is not None
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = _RED
        x.size = 1 + self._size(h.left) + self._size(h.right)
        return x 

    def _flip_colors(self, h: _Node[K, V]) -> None:
        h.color = not h.color
        if h.left is not None:
            h.left.color = not h.left.color
        if h.right is not None:
            h.right.color = not h.right.color
        
    def _fix_up(self, h: _Node[K, V]) -> _Node[K, V]:
        if self._is_red(h.right):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return h
    
    def _move_red_left(self, h: _Node[K, V]) -> _Node[K, V]:
        self._flip_colos(h)
        if h.left is not None and self._is_red(h.right.left):
            h.right = self._rotate_right(h.right)
            h = self._rotate_left(h)
            self._flip_colors(h)
        return h
    
    def _move_red_right(self, h: _Node[K, V]) -> _Node[K, V]:
        self._flip_colors(h)
        if h.left is not None and self._is_red(h.left.left):
            h = self._rotate_right(h)
            self._flip_colors(h)
        return h 
    
    def _insert(self, h: Optional[_Node[K, V]], key: K, value: V) -> _Node[K, V]:
        if h is None:
            return _Node(key=key, value=value, color=_RED)
        
        if key < h.key:
            h.left = self._insert(h.left, key, value)
        elif key > h.key:
            h.right = self._insert(h.right, key, value)
        else:
            h.value = value

        if self._is_red(h.right) and not self._is_red(h.left):
            h = self._rotate_left(h)
        if self._is_red(h.left) and self._is_red(h.left.left):
            h = self._rotate_right(h)
        if self._is_red(h.left) and self._is_red(h.right):
            self._flip_colors(h)

        h.size = 1 + self._size(h.left) + self._size(h.right)
        return h

