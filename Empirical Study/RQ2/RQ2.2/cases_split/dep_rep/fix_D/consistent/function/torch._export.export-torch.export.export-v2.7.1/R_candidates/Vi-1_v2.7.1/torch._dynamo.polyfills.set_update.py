def set_update(set1, set2):
    for x in set2:
        if x not in set1:
            set1.add(x)
    return set1
