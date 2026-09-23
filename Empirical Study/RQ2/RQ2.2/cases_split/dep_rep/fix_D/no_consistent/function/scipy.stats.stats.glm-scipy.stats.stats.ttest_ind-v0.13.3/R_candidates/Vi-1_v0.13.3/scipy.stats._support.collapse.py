def collapse(a, keepcols, collapsecols, stderr=0, ns=0, cfcn=None):
    """Averages data in collapsecol, keeping all unique items in keepcols
    (using unique, which keeps unique LISTS of column numbers), retaining
    the unique sets of values in keepcols, the mean for each.  If the sterr or
    N of the mean are desired, set either or both parameters to 1.

    Returns: unique 'conditions' specified by the contents of columns specified
    by keepcols, abutted with the mean(s,axis=0) of column(s) specified by
    collapsecols

    Examples
    --------

    import numpy as np
    from scipy import stats

    xx = np.array([[ 0.,  0.,  1.],
           [ 1.,  1.,  1.],
           [ 2.,  2.,  1.],
           [ 0.,  3.,  1.],
           [ 1.,  4.,  1.],
           [ 2.,  5.,  1.],
           [ 0.,  6.,  1.],
           [ 1.,  7.,  1.],
           [ 2.,  8.,  1.],
           [ 0.,  9.,  1.]])

    >>> stats._support.collapse(xx, (0), (1,2), stderr=0, ns=0, cfcn=None)
    array([[ 0. ,  4.5,  1. ],
           [ 0. ,  4.5,  1. ],
           [ 1. ,  4. ,  1. ],
           [ 1. ,  4. ,  1. ],
           [ 2. ,  5. ,  1. ],
           [ 2. ,  5. ,  1. ]])
    >>> stats._support.collapse(xx, (0), (1,2), stderr=1, ns=1, cfcn=None)
    array([[ 0.        ,  4.5       ,  1.93649167,  4.        ,  1.        ,
             0.        ,  4.        ],
           [ 0.        ,  4.5       ,  1.93649167,  4.        ,  1.        ,
             0.        ,  4.        ],
           [ 1.        ,  4.        ,  1.73205081,  3.        ,  1.        ,
             0.        ,  3.        ],
           [ 1.        ,  4.        ,  1.73205081,  3.        ,  1.        ,
             0.        ,  3.        ],
           [ 2.        ,  5.        ,  1.73205081,  3.        ,  1.        ,
             0.        ,  3.        ],
           [ 2.        ,  5.        ,  1.73205081,  3.        ,  1.        ,
             0.        ,  3.        ]])

    """
    if cfcn is None:
        cfcn = lambda x: np.mean(x, axis=0)
    a = asarray(a)
    if keepcols == []:
        avgcol = colex(a,collapsecols)
        means = cfcn(avgcol)
        return means
    else:
        if type(keepcols) not in [ListType,TupleType,np.ndarray]:
            keepcols = [keepcols]
        values = colex(a,keepcols)   # so that "item" can be appended (below)
        uniques = unique(values).tolist()  # get a LIST, so .sort keeps rows intact
        uniques.sort()
        newlist = []
        for item in uniques:
            if type(item) not in [ListType,TupleType,np.ndarray]:
                item = [item]
            tmprows = linexand(a,keepcols,item)
            for col in collapsecols:
                avgcol = colex(tmprows,col)
                item.append(cfcn(avgcol))
                if stderr:
                    if len(avgcol) > 1:
                        item.append(compute_stderr(avgcol))
                    else:
                        item.append('N/A')
                if ns:
                    item.append(len(avgcol))
                newlist.append(item)
        try:
            new_a = np.array(newlist)
        except TypeError:
            new_a = np.array(newlist,'O')
        return new_a
