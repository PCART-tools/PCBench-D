def is_list_of_ints(intlist):
    """ Return True if list is a list of ints. """
    if not isinstance(intlist, list):
        return False
    for i in intlist:
        if not isinstance(i, int):
            return False
    return True
