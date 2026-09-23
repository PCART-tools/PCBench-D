def set_difference(set1, set2):
    difference_set = set()
    for x in set1:
        if x not in set2:
            difference_set.add(x)
    return difference_set
