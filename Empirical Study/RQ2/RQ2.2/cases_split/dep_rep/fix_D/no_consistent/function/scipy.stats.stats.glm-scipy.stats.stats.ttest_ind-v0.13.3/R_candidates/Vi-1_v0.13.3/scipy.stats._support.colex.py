def colex(a, indices, axis=1):
    """\nExtracts specified indices (a list) from passed array, along passed
    axis (column extraction is default).  BEWARE: A 1D array is presumed to be a
    column-array (and that the whole array will be returned as a column).

    Returns: the columns of a specified by indices\n"""

    if type(indices) not in [ListType,TupleType,np.ndarray]:
        indices = [indices]
    if len(np.shape(a)) == 1:
        cols = np.resize(a,[a.shape[0],1])
    else:
        cols = np.take(a,indices,axis)
    return cols
