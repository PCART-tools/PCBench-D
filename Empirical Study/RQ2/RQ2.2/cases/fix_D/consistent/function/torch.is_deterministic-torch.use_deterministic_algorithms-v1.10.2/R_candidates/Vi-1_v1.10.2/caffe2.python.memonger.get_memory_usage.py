def get_memory_usage(assignments):
    ret = 0
    for cur in assignments:
        ret += _get_max_size(cur)
    return ret
