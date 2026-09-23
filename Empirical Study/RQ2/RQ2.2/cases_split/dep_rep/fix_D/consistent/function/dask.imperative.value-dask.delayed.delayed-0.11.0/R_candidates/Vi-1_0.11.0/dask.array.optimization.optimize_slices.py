def optimize_slices(dsk):
    """ Optimize slices

    1.  Fuse repeated slices, like x[5:][2:6] -> x[7:11]
    2.  Remove full slices, like         x[:] -> x

    See also:
        fuse_slice_dict
    """
    getters = (getarray, getitem)
    dsk = dsk.copy()
    for k, v in dsk.items():
        if type(v) is tuple:
            if v[0] in getters:
                try:
                    func, a, a_index = v
                    use_getarray = func is getarray
                except ValueError:  # has four elements, includes a lock
                    continue
                while type(a) is tuple and a[0] in getters:
                    try:
                        f2, b, b_index = a
                        use_getarray |= f2 is getarray
                    except ValueError:  # has four elements, includes a lock
                        break
                    if (type(a_index) is tuple) != (type(b_index) is tuple):
                        break
                    if ((type(a_index) is tuple) and
                            (len(a_index) != len(b_index)) and
                            any(i is None for i in b_index + a_index)):
                        break
                    try:
                        c_index = fuse_slice(b_index, a_index)
                    except NotImplementedError:
                        break
                    (a, a_index) = (b, c_index)
                if use_getarray:
                    dsk[k] = (getarray, a, a_index)
                elif (type(a_index) is slice and
                      not a_index.start and
                      a_index.stop is None and
                      a_index.step is None):
                    dsk[k] = a
                elif type(a_index) is tuple and all(type(s) is slice and
                                                    not s.start and
                                                    s.stop is None and
                                                    s.step is None
                                                    for s in a_index):
                    dsk[k] = a
                else:
                    dsk[k] = (getitem, a, a_index)
    return dsk
