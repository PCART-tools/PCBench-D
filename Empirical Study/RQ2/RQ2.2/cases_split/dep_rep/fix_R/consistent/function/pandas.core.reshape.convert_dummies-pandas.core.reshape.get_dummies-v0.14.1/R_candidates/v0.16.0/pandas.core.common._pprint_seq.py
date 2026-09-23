def _pprint_seq(seq, _nest_lvl=0, **kwds):
    """
    internal. pprinter for iterables. you should probably use pprint_thing()
    rather then calling this directly.

    bounds length of printed sequence, depending on options
    """
    if isinstance(seq, set):
        fmt = u("set([%s])")
    else:
        fmt = u("[%s]") if hasattr(seq, '__setitem__') else u("(%s)")

    nitems = get_option("max_seq_items") or len(seq)

    s = iter(seq)
    r = []
    for i in range(min(nitems, len(seq))):  # handle sets, no slicing
        r.append(pprint_thing(next(s), _nest_lvl + 1, **kwds))
    body = ", ".join(r)

    if nitems < len(seq):
        body += ", ..."
    elif isinstance(seq, tuple) and len(seq) == 1:
        body += ','

    return fmt % body
