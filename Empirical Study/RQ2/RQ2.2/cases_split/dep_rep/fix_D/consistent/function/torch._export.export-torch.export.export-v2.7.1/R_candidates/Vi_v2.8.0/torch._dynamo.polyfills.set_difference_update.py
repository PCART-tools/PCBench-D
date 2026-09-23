def set_difference_update(set1, *others):
    result = set1.difference(*others)
    set1.clear()
    set1.update(result)
