def optimize_slices(dsk):
    """ Optimize slices

    1.  Fuse repeated slices, like x[5:][2:6] -> x[7:11]
    2.  Remove full slices, like         x[:] -> x

    See also:
        fuse_slice_dict
    """
    fancy_ind_types = (list, np.ndarray)
    getters = (getarray_nofancy, getarray, getitem)
    dsk = dsk.copy()
    for k, v in dsk.items():
        if type(v) is tuple and v[0] in getters and len(v) == 3:
            f, a, a_index = v
            getter = f
            while type(a) is tuple and a[0] in getters and len(a) == 3:
                f2, b, b_index = a
                if (type(a_index) is tuple) != (type(b_index) is tuple):
                    break
                if type(a_index) is tuple:
                    indices = b_index + a_index
                    if (len(a_index) != len(b_index) and
                            any(i is None for i in indices)):
                        break
                    if (f2 is getarray_nofancy and
                            any(isinstance(i, fancy_ind_types) for i in indices)):
                        break
                elif (f2 is getarray_nofancy and
                        (type(a_index) in fancy_ind_types or
                         type(b_index) in fancy_ind_types)):
                    break
                try:
                    c_index = fuse_slice(b_index, a_index)
                    # rely on fact that nested gets never decrease in
                    # strictness e.g. `(getarray, (getitem, ...))` never
                    # happens
                    getter = f2
                except NotImplementedError:
                    break
                a, a_index = b, c_index
            if getter is not getitem:
                dsk[k] = (getter, a, a_index)
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
