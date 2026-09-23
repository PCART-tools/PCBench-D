def set_symmetric_difference_update(set1, set2):
    result = set1.symmetric_difference(set2)
    set1.clear()
    set1.update(result)
