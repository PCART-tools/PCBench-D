def set_union(set1, *others):
    # frozenset also uses this function
    union_set = set(set1.copy())
    for set2 in others:
        set_update(union_set, set2)
    return type(set1)(union_set)
