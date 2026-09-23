def tree_width(N, to_binary=False):
    """Generate tree width suitable for ``merge_sorted`` given N inputs

    The larger N is, the more tasks are reduced in a single task.

    In theory, this is designed so all tasks are of comparable effort.
    """
    if N < 32:
        group_size = 2
    else:
        group_size = int(math.log(N))
    num_groups = N // group_size
    if to_binary or num_groups < 16:
        return 2**int(math.log(N / group_size, 2))
    else:
        return num_groups
