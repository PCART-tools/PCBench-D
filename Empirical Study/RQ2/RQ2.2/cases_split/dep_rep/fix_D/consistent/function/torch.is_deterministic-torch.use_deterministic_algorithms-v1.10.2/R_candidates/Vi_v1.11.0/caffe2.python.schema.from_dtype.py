def from_dtype(dtype, _outer_shape=()):
    """Constructs a Caffe2 schema from the given numpy's dtype.

    Numpy supports scalar, array-like and structured datatypes, as long as
    all the shapes are fixed. This function breaks down the given dtype into
    a Caffe2 schema containing `Struct` and `Scalar` types.

    Fields containing byte offsets are not currently supported.
    """
    if not isinstance(dtype, np.dtype):
        # wrap into a ndtype
        shape = _outer_shape
        dtype = np.dtype((dtype, _outer_shape))
    else:
        # concatenate shapes if necessary
        shape = _outer_shape + dtype.shape
        if shape != dtype.shape:
            dtype = np.dtype((dtype.base, shape))

    if not dtype.fields:
        return Scalar(dtype)

    struct_fields = []
    for name, (fdtype, offset) in dtype.fields:
        assert offset == 0, ('Fields with byte offsets are not supported.')
        struct_fields += (name, from_dtype(fdtype, _outer_shape=shape))
    return Struct(*struct_fields)
