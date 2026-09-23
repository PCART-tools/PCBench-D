def _get_count(assignments):
    ''' Return number of blobs in assignments '''
    if assignments:
        return sum([len(x) for x in assignments])
    return 0
