def sum_normals(stats: Iterable[Stat]) -> Stat:
    """
    Returns a stat corresponding to the sum of the given stats.

    Assumes that the center and spread for each of the given stats are
    mean and stdev, respectively.
    """
    l = list(stats)
    spread: Optional[float]
    if any(stat['spread'] is not None for stat in l):
        spread = math.sqrt(sum((stat['spread'] or 0)**2 for stat in l))
    else:
        spread = None
    return {
        'center': sum(stat['center'] for stat in l),
        'spread': spread,
    }
