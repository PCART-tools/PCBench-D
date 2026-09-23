def child_max(dependencies, dependents, scores):
    """ Maximum-ish of scores of children

    This takes a dictionary of scores per key and returns a new set of scores
    per key that is the maximum of the scores of all children of that node plus
    its own score.  In some sense this ranks each node by the maximum
    importance of their children plus their own value.

    This is generally fed the result from ``ndependents``

    Examples
    --------

    >>> dsk = {'a': 1, 'b': 2, 'c': (inc, 'a'), 'd': (add, 'b', 'c')}
    >>> scores = {'a': 3, 'b': 2, 'c': 2, 'd': 1}
    >>> dependencies, dependents = get_deps(dsk)

    >>> sorted(child_max(dependencies, dependents, scores).items())
    [('a', 3), ('b', 2), ('c', 5), ('d', 6)]
    """
    result = dict()
    num_needed = dict((k, len(v)) for k, v in dependencies.items())
    current = set(k for k, v in num_needed.items() if v == 0)
    while current:
        key = current.pop()
        score = scores[key]
        children = dependencies[key]
        if children:
            score += max(result[child] for child in children)
        result[key] = score
        for parent in dependents[key]:
            num_needed[parent] -= 1
            if num_needed[parent] == 0:
                current.add(parent)
    return result
