def unique(inarray):
    """Returns unique items in the FIRST dimension of the passed array. Only
    works on arrays NOT including string items (e.g., type 'O' or 'c').
    """
    inarray = asarray(inarray)
    uniques = np.array([inarray[0]])
    if len(uniques.shape) == 1:            # IF IT'S A 1D ARRAY
        for item in inarray[1:]:
            if np.add.reduce(np.equal(uniques,item).flat) == 0:
                try:
                    uniques = np.concatenate([uniques,np.array[np.newaxis,:]])
                except TypeError:
                    uniques = np.concatenate([uniques,np.array([item])])
    else:                                  # IT MUST BE A 2+D ARRAY
        if inarray.dtype.char != 'O':  # not an Object array
            for item in inarray[1:]:
                if not np.sum(np.alltrue(np.equal(uniques,item),1),axis=0):
                    try:
                        uniques = np.concatenate([uniques,item[np.newaxis,:]])
                    except TypeError:    # the item to add isn't a list
                        uniques = np.concatenate([uniques,np.array([item])])
                else:
                    pass  # this item is already in the uniques array
        else:   # must be an Object array, alltrue/equal functions don't work
            for item in inarray[1:]:
                newflag = 1
                for unq in uniques:  # NOTE: cmp --> 0=same, -1=<, 1=>
                    test = np.sum(abs(np.array(list(map(cmp,item,unq)))),axis=0)
                    if test == 0:   # if item identical to any 1 row in uniques
                        newflag = 0  # then not a novel item to add
                        break
                if newflag == 1:
                    try:
                        uniques = np.concatenate([uniques,item[np.newaxis,:]])
                    except TypeError:    # the item to add isn't a list
                        uniques = np.concatenate([uniques,np.array([item])])
    return uniques
