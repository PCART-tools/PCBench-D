def tree_groups(N, num_groups):
    """Split an integer N into evenly sized and spaced groups.

    >>> tree_groups(16, 6)
    [3, 2, 3, 3, 2, 3]
    """
    # Bresenham, you so smooth!
    group_size = N // num_groups
    dx = num_groups
    dy = N - group_size * num_groups
    D = 2 * dy - dx
    rv = []
    for _ in range(num_groups):
        if D < 0:
            rv.append(group_size)
        else:
            rv.append(group_size + 1)
            D -= 2 * dx
        D += 2 * dy
    return rv
