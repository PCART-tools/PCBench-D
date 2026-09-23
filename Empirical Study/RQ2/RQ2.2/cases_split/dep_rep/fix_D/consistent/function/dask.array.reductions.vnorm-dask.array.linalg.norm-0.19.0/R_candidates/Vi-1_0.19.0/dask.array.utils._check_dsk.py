def _check_dsk(dsk):
    """ Check that graph is well named and non-overlapping """
    if not isinstance(dsk, ShareDict):
        return

    assert all(isinstance(k, (tuple, str)) for k in dsk.dicts)
    freqs = frequencies(concat(dsk.dicts.values()))
    non_one = {k: v for k, v in freqs.items() if v != 1}
    assert not non_one, non_one
