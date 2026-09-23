def to_hdf5(filename, *args, **kwargs):
    """ Store arrays in HDF5 file

    This saves several dask arrays into several datapaths in an HDF5 file.
    It creates the necessary datasets and handles clean file opening/closing.

    >>> da.to_hdf5('myfile.hdf5', '/x', x)  # doctest: +SKIP

    or

    >>> da.to_hdf5('myfile.hdf5', {'/x': x, '/y': y})  # doctest: +SKIP

    Optionally provide arguments as though to ``h5py.File.create_dataset``

    >>> da.to_hdf5('myfile.hdf5', '/x', x, compression='lzf', shuffle=True)  # doctest: +SKIP

    This can also be used as a method on a single Array

    >>> x.to_hdf5('myfile.hdf5', '/x')  # doctest: +SKIP

    See Also
    --------
    da.store
    h5py.File.create_dataset
    """
    if len(args) == 1 and isinstance(args[0], dict):
        data = args[0]
    elif (len(args) == 2 and
          isinstance(args[0], str) and
          isinstance(args[1], Array)):
        data = {args[0]: args[1]}
    else:
        raise ValueError("Please provide {'/data/path': array} dictionary")

    chunks = kwargs.pop('chunks', True)

    import h5py
    with h5py.File(filename) as f:
        dsets = [f.require_dataset(dp, shape=x.shape, dtype=x.dtype,
                                   chunks=tuple([c[0] for c in x.chunks])
                                   if chunks is True else chunks, **kwargs)
                 for dp, x in data.items()]
        store(list(data.values()), dsets)
