"""A fixed-capacity least-recently-used cache."""


class LinkedNode:
    """A node in the cache's doubly linked list."""

    def __init__(self, key, value, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


class LRUCache:
    """Store up to ``capacity`` key/value pairs with O(1) access and updates."""

    def __init__(self, capacity):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be a positive integer")
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self._nodes = {}
        self._head = LinkedNode(None, None)
        self._tail = LinkedNode(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self):
        return len(self._nodes)

    def get(self, key):
        node = self._nodes.get(key)
        if node is None:
            return None

        self._move_to_front(node)
        return node.value

    def put(self, key, value):
        node = self._nodes.get(key)
        if node is not None:
            self._remove_node(node)
            node.value = value
        else:
            node = LinkedNode(key, value)
            self._nodes[key] = node

        self._add_to_front(node)

        if len(self._nodes) > self.capacity:
            least_recently_used = self._tail.prev
            self._remove_node(least_recently_used)
            del self._nodes[least_recently_used.key]

    def _add_to_front(self, node):
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)