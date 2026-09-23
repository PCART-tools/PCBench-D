def set_isdisjoint(set1, set2):
    for x in set1:
        if x in set2:
            return False
    return True
