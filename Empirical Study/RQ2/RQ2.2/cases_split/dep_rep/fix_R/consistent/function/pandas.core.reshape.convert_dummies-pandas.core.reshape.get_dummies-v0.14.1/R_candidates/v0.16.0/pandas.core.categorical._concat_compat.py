def _concat_compat(to_concat, axis=0):
    """
    provide concatenation of an object/categorical array of arrays each of which is a single dtype

    Parameters
    ----------
    to_concat : array of arrays
    axis : axis to provide concatenation

    Returns
    -------
    a single array, preserving the combined dtypes
    """

    def convert_categorical(x):
        # coerce to object dtype
        if is_categorical_dtype(x.dtype):
            return x.get_values()
        return x.ravel()

    typs = get_dtype_kinds(to_concat)
    if not len(typs-set(['object','category'])):

        # we only can deal with object & category types
        pass

    else:

        # convert to object type and perform a regular concat
        from pandas.core.common import _concat_compat
        return _concat_compat([ np.array(x,copy=False).astype('object') for x in to_concat ],axis=axis)

    # we could have object blocks and categorical's here
    # if we only have a single cateogoricals then combine everything
    # else its a non-compat categorical
    categoricals = [ x for x in to_concat if is_categorical_dtype(x.dtype) ]
    objects = [ x for x in to_concat if is_object_dtype(x.dtype) ]

    # validate the categories
    categories = None
    for x in categoricals:
        if categories is None:
            categories = x.categories
        if not categories.equals(x.categories):
            raise ValueError("incompatible categories in categorical concat")

    # concat them
    return Categorical(np.concatenate([ convert_categorical(x) for x in to_concat ],axis=axis), categories=categories)
