def format_plan(plan):
    """
    >>> format_plan([((10, 10, 10), (15, 15)), ((30,), (10, 10, 10))])
    [(3*[10], 2*[15]), ([30], 3*[10])]
    """
    return [format_chunks(c) for c in plan]
