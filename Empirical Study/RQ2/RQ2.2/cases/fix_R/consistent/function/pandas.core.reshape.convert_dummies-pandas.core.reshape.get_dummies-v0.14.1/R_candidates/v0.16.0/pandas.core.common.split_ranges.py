def split_ranges(mask):
    """ Generates tuples of ranges which cover all True value in mask

    >>> list(split_ranges([1,0,0,1,0]))
    [(0, 1), (3, 4)]
    """
    ranges = [(0, len(mask))]

    for pos, val in enumerate(mask):
        if not val:  # this pos should be ommited, split off the prefix range
            r = ranges.pop()
            if pos > r[0]:  # yield non-zero range
                yield (r[0], pos)
            if pos + 1 < len(mask):  # save the rest for processing
                ranges.append((pos + 1, len(mask)))
    if ranges:
        yield ranges[-1]
