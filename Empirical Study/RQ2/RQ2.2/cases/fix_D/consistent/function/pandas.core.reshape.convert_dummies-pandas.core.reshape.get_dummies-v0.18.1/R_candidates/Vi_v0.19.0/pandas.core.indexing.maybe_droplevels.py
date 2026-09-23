def maybe_droplevels(index, key):
    # drop levels
    original_index = index
    if isinstance(key, tuple):
        for _ in key:
            try:
                index = index.droplevel(0)
            except:
                # we have dropped too much, so back out
                return original_index
    else:
        try:
            index = index.droplevel(0)
        except:
            pass

    return index
