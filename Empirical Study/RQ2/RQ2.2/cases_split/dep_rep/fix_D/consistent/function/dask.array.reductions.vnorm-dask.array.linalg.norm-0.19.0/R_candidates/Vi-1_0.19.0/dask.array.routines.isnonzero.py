def isnonzero(a):
    try:
        np.zeros(tuple(), dtype=a.dtype).astype(bool)
    except ValueError:
        ######################################################
        # Handle special cases where conversion to bool does #
        # not work correctly.                                #
        #                                                    #
        # xref: https://github.com/numpy/numpy/issues/9479   #
        ######################################################
        return a.map_blocks(_isnonzero_vec, dtype=bool)
    else:
        return a.astype(bool)
