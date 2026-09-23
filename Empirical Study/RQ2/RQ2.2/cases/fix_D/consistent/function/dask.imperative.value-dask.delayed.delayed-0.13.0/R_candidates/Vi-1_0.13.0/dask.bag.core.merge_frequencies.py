def merge_frequencies(seqs):
    first, rest = seqs[0], seqs[1:]
    if not rest:
        return first
    out = defaultdict(int)
    out.update(first)
    for d in rest:
        for k, v in iteritems(d):
            out[k] += v
    return out
