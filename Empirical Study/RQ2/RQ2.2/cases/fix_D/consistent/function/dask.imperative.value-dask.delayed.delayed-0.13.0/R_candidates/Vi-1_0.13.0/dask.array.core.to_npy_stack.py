def to_npy_stack(dirname, x, axis=0):
    """ Write dask array to a stack of .npy files

    This partitions the dask.array along one axis and stores each block along
    that axis as a single .npy file in the specified directory

    Examples
    --------

    >>> x = da.ones((5, 10, 10), chunks=(2, 4, 4))  # doctest: +SKIP
    >>> da.to_npy_stack('data/', x, axis=0)  # doctest: +SKIP

        $ tree data/
        data/
        |-- 0.npy
        |-- 1.npy
        |-- 2.npy
        |-- info

    The ``.npy`` files store numpy arrays for ``x[0:2], x[2:4], and x[4:5]``
    respectively, as is specified by the chunk size along the zeroth axis.  The
    info file stores the dtype, chunks, and axis information of the array.

    You can load these stacks with the ``da.from_npy_stack`` function.

    >>> y = da.from_npy_stack('data/')  # doctest: +SKIP

    See Also
    --------
    from_npy_stack
    """

    chunks = tuple((c if i == axis else (sum(c),))
                   for i, c in enumerate(x.chunks))
    xx = x.rechunk(chunks)

    if not os.path.exists(dirname):
        os.path.mkdir(dirname)

    meta = {'chunks': chunks, 'dtype': x.dtype, 'axis': axis}

    with open(os.path.join(dirname, 'info'), 'wb') as f:
        pickle.dump(meta, f)

    name = 'to-npy-stack-' + str(uuid.uuid1())
    dsk = dict(((name, i), (np.save, os.path.join(dirname, '%d.npy' % i), key))
               for i, key in enumerate(core.flatten(xx._keys())))

    Array._get(merge(dsk, xx.dask), list(dsk))
