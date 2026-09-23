def _make_unique_name(seen: Set[str], name: str, min_version: int = 0):
    '''
    Make the name unique by appending a unique number to the name. Used for SSA.

    Args:
        seen (set): Set of names that have already been used (with respect to
            some context).
        name (string): The name to make unique
        min_version (number): Starting index. Is incremented continually until
            it can make the resulting name unique relative to 'seen'.

    Returns:
        x (string): A version of name that is not in seen.
    '''
    assert name is not None
    i = min_version
    x = '%s_%d' % (name, i) if i else name
    while x in seen:
        i += 1
        x = '%s_%d' % (name, i)
    seen.add(x)
    return x
