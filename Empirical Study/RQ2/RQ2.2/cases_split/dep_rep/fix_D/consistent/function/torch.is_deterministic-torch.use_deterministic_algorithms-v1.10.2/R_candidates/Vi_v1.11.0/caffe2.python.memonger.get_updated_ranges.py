def get_updated_ranges(ranges, max_live=None):
    ''' Set LiveRange.defined = -1 if it is None
        Set LiveRange.used = max_live if it is None
        Set LiveRanee.size = 1 if it is None
    '''

    def _get_max_live(ranges):
        max_live = max(x[1].used for x in ranges if x[1].used) + 1
        return max_live

    def _update_range(x, max_live, size):
        cx = x
        if x[1].defined is None:
            cx = (cx[0], cx[1]._replace(defined=-1))
        if x[1].used is None:
            cx = (cx[0], cx[1]._replace(used=max_live))
        if x[1].size is None:
            cx = (cx[0], cx[1]._replace(size=size))
        return cx

    if max_live is None:
        max_live = _get_max_live(ranges)
    ranges = [_update_range(x, max_live, 1) for x in ranges]

    return ranges
