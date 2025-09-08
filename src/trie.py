import heapq

class TrieNode:
    def __init__(self):
        self.children = {}        # char -> TrieNode
        self.is_word = False
        self.freq = 0             # valid only if is_word=True

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, freq: int = 1):
        """Insert a word into the trie with given frequency."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True
        node.freq = freq

    def search(self, word: str) -> bool:
        """Check if word exists in the trie."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_word

    def _collect(self, node, prefix, results):
        """Recursive DFS to collect words starting from given node."""
        if node.is_word:
            results.append((prefix, node.freq))
        for ch, child in node.children.items():
            self._collect(child, prefix + ch, results)

    def starts_with(self, prefix: str, limit=None):
        """Return words starting with prefix, ranked by frequency."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        results = []
        self._collect(node, prefix, results)

        # Sort by frequency, highest first
        if limit:
            return heapq.nlargest(limit, results, key=lambda x: x[1])
        return sorted(results, key=lambda x: -x[1])
