def set_intersection_update(set1, *others):
    result = set1.intersection(*others)
    set1.clear()
    set1.update(result)
