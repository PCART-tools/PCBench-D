def optimize_slices(dsk):
    """ Optimize slices

    1.  Fuse repeated slices, like x[5:][2:6] -> x[7:11]
    2.  Remove full slices, like         x[:] -> x

    See also:
        fuse_slice_dict
    """
    fancy_ind_types = (list, np.ndarray)
    dsk = dsk.copy()
    for k, v in dsk.items():
        if type(v) is tuple and v[0] in GETTERS and len(v) in (3, 5):
            if len(v) == 3:
                get, a, a_index = v
                # getter defaults to asarray=True, getitem is semantically False
                a_asarray = get is not getitem
                a_lock = None
            else:
                get, a, a_index, a_asarray, a_lock = v
            while type(a) is tuple and a[0] in GETTERS and len(a) in (3, 5):
                if len(a) == 3:
                    f2, b, b_index = a
                    b_asarray = f2 is not getitem
                    b_lock = None
                else:
                    f2, b, b_index, b_asarray, b_lock = a

                if a_lock and a_lock is not b_lock:
                    break
                if (type(a_index) is tuple) != (type(b_index) is tuple):
                    break
                if type(a_index) is tuple:
                    indices = b_index + a_index
                    if (len(a_index) != len(b_index) and
                            any(i is None for i in indices)):
                        break
                    if (f2 is getter_nofancy and
                            any(isinstance(i, fancy_ind_types) for i in indices)):
                        break
                elif (f2 is getter_nofancy and
                        (type(a_index) in fancy_ind_types or
                         type(b_index) in fancy_ind_types)):
                    break
                try:
                    c_index = fuse_slice(b_index, a_index)
                    # rely on fact that nested gets never decrease in
                    # strictness e.g. `(getter_nofancy, (getter, ...))` never
                    # happens
                    get = getter if f2 is getter_inline else f2
                except NotImplementedError:
                    break
                a, a_index, a_lock = b, c_index, b_lock
                a_asarray |= b_asarray

            # Skip the get call if not from from_array and nothing to do
            if (get not in GETNOREMOVE and
                ((type(a_index) is slice and not a_index.start and
                  a_index.stop is None and a_index.step is None) or
                 (type(a_index) is tuple and
                  all(type(s) is slice and not s.start and s.stop is None and
                      s.step is None for s in a_index)))):
                dsk[k] = a
            elif get is getitem or (a_asarray and not a_lock):
                # default settings are fine, drop the extra parameters Since we
                # always fallback to inner `get` functions, `get is getitem`
                # can only occur if all gets are getitem, meaning all
                # parameters must be getitem defaults.
                dsk[k] = (get, a, a_index)
            else:
                dsk[k] = (get, a, a_index, a_asarray, a_lock)

    return dsk
