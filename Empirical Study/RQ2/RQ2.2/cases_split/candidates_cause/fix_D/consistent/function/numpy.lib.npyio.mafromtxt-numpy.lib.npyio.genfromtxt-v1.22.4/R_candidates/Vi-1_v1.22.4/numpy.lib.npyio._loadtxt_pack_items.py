def _loadtxt_pack_items(packing, items):
    """Pack items into nested lists based on re-packing info."""
    if packing is None:
        return items[0]
    elif packing is tuple:
        return tuple(items)
    elif packing is list:
        return list(items)
    else:
        start = 0
        ret = []
        for length, subpacking in packing:
            ret.append(
                _loadtxt_pack_items(subpacking, items[start:start+length]))
            start += length
        return tuple(ret)
