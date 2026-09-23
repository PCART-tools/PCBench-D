def set_intersection(set1, set2):
    intersection_set = set()
    for x in set1:
        if x in set2:
            intersection_set.add(x)
    return intersection_set
