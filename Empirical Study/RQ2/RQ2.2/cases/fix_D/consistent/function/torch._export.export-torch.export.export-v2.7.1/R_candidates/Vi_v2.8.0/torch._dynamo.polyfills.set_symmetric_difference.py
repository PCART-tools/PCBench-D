def set_symmetric_difference(set1, set2):
    symmetric_difference_set = set()
    for x in set1:
        if x not in set2:
            symmetric_difference_set.add(x)
    for x in set2:
        if x not in set1:
            symmetric_difference_set.add(x)
    return symmetric_difference_set
