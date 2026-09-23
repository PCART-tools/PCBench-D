def set_intersection(set1, *others):
    if len(others) == 0:
        return set1.copy()

    intersection_set = set()
    for x in set1:
        for set2 in others:
            if x not in set2:
                break
        else:
            intersection_set.add(x)
    return intersection_set
