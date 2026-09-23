def make_trie(configs: Dict[str, Set[str]]) -> Trie:
    """
    Return a trie from path prefixes to their `mypy` configs.

    Specifically, each layer of the trie represents a segment of a POSIX
    path relative to the root of this repo. If you follow a path down
    the trie and reach a `None` key, that `None` maps to the (nonempty)
    set of keys in `configs` which explicitly include that path.
    """
    trie: Trie = {}
    for ini, files in configs.items():
        for f in files:
            inner = trie
            for segment in split_path(f):
                inner = inner.setdefault(segment, {})
            inner.setdefault(None, set()).add(ini)
    return trie
