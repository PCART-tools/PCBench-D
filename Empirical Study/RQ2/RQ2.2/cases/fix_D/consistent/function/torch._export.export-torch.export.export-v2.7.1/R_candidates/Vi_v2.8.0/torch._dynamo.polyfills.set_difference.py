def set_difference(set1, *others):
    if len(others) == 0:
        return set1.copy()

    if not all(isinstance(s, Iterable) for s in others):
        raise TypeError(f"set.difference expected an iterable, got {type(others)}")

    difference_set = set()
    for x in set1:
        for set2 in others:
            if x in set2:
                break
        else:
            difference_set.add(x)
    return difference_set
