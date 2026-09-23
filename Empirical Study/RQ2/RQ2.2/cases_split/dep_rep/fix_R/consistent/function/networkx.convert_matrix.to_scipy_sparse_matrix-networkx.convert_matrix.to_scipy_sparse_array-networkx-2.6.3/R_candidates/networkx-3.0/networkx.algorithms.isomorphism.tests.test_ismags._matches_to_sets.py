def _matches_to_sets(matches):
    """
    Helper function to facilitate comparing collections of dictionaries in
    which order does not matter.
    """
    return set(map(lambda m: frozenset(m.items()), matches))
