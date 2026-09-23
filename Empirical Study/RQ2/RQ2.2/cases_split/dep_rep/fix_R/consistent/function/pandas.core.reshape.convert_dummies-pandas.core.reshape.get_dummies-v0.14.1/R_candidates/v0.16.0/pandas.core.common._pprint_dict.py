def _pprint_dict(seq, _nest_lvl=0, **kwds):
    """
    internal. pprinter for iterables. you should probably use pprint_thing()
    rather then calling this directly.
    """
    fmt = u("{%s}")
    pairs = []

    pfmt = u("%s: %s")

    nitems = get_option("max_seq_items") or len(seq)

    for k, v in list(seq.items())[:nitems]:
        pairs.append(pfmt % (pprint_thing(k, _nest_lvl + 1, **kwds),
                             pprint_thing(v, _nest_lvl + 1, **kwds)))

    if nitems < len(seq):
        return fmt % (", ".join(pairs) + ", ...")
    else:
        return fmt % ", ".join(pairs)
