def _get_level_lengths(levels, sentinel=''):
    from itertools import groupby

    def _make_grouper():
        record = {'count': 0}

        def grouper(x):
            if x != sentinel:
                record['count'] += 1
            return record['count']
        return grouper

    result = []
    for lev in levels:
        i = 0
        f = _make_grouper()
        recs = {}
        for key, gpr in groupby(lev, f):
            values = list(gpr)
            recs[i] = len(values)
            i += len(values)

        result.append(recs)

    return result
