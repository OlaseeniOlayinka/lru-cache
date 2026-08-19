import unittest

from lru_cache import LRUCache


class LRUCacheTests(unittest.TestCase):
    def test_get_returns_none_for_missing_key(self):
        cache = LRUCache(2)

        self.assertIsNone(cache.get("missing"))
        self.assertEqual(len(cache), 0)

    def test_get_promotes_entry_to_most_recently_used(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)

        self.assertEqual(cache.get("a"), 1)
        cache.put("c", 3)

        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_put_updates_and_promotes_existing_entry(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)

        self.assertEqual(len(cache), 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 10)
        self.assertIsNone(cache.get("b"))

    def test_evicts_least_recently_used_entry(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_supports_capacity_one_and_none_values(self):
        cache = LRUCache(1)
        cache.put("a", None)

        self.assertIsNone(cache.get("a"))
        self.assertEqual(len(cache), 1)
        cache.put("b", False)
        self.assertEqual(len(cache), 1)
        self.assertIsNone(cache.get("a"))
        self.assertFalse(cache.get("b"))

    def test_rejects_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-1)
        with self.assertRaises(TypeError):
            LRUCache(1.5)
        with self.assertRaises(TypeError):
            LRUCache(True)

    def test_dictionary_and_list_have_matching_entries(self):
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")

        list_keys = []
        node = cache._head.next
        while node is not cache._tail:
            list_keys.append(node.key)
            self.assertIs(cache._nodes[node.key], node)
            self.assertIs(node.next.prev, node)
            node = node.next

        self.assertEqual(set(list_keys), set(cache._nodes))
        self.assertEqual(len(list_keys), len(cache))
        self.assertIs(cache._head.next.prev, cache._head)
        self.assertIs(cache._tail.prev.next, cache._tail)


if __name__ == "__main__":
    unittest.main()