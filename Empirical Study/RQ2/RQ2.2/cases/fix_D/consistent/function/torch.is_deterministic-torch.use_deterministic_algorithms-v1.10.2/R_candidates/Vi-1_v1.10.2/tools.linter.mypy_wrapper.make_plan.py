def make_plan(
    *,
    configs: Dict[str, Set[str]],
    files: List[str]
) -> Dict[str, List[str]]:
    """
    Return a dict from config names to the files to run them with.

    The keys of the returned dict are a subset of the keys of `configs`.
    The list of files in each value of returned dict should contain a
    nonempty subset of the given `files`, in the same order as `files`.
    """
    trie = make_trie(configs)
    plan = defaultdict(list)
    for filename in files:
        for config in lookup(trie, filename):
            plan[config].append(filename)
    return plan
