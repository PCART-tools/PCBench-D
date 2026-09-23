def lookup(trie: Trie, filename: str) -> Set[str]:
    """
    Return the configs in `trie` that include a prefix of `filename`.

    A path is included by a config if any of its ancestors are included
    by the wildcard-expanded version of that config's `files`. Thus,
    this function follows `filename`'s path down the `trie` and
    accumulates all the configs it finds along the way.
    """
    configs = set()
    inner = trie
    for segment in split_path(filename):
        inner = inner.get(segment, {})
        configs |= inner.get(None, set())
    return configs
