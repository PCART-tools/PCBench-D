def merge_dicts(*dicts):
    return {x: d[x] for d in dicts for x in d}
