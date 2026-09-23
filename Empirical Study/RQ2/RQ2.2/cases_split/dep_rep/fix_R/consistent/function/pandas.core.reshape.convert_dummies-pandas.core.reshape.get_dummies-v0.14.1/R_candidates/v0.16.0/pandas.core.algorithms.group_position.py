def group_position(*args):
    """
    Get group position
    """
    from collections import defaultdict
    table = defaultdict(int)

    result = []
    for tup in zip(*args):
        result.append(table[tup])
        table[tup] += 1

    return result
