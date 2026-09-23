def _get_max_size(assignment):
    if not assignment:
        return 0
    ret = max([x[1].size for x in assignment])
    ret = 0 if ret is None else ret
    return ret
