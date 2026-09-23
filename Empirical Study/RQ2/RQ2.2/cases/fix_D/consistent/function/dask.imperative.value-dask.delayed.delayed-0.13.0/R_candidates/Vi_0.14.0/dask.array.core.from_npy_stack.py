def from_npy_stack(dirname, mmap_mode='r'):
    """ Load dask array from stack of npy files

    See ``da.to_npy_stack`` for docstring

    Parameters
    ----------
    dirname: string
        Directory of .npy files
    mmap_mode: (None or 'r')
        Read data in memory map mode
    """
    with open(os.path.join(dirname, 'info'), 'rb') as f:
        info = pickle.load(f)

    dtype = info['dtype']
    chunks = info['chunks']
    axis = info['axis']

    name = 'from-npy-stack-%s' % dirname
    keys = list(product([name], *[range(len(c)) for c in chunks]))
    values = [(np.load, os.path.join(dirname, '%d.npy' % i), mmap_mode)
              for i in range(len(chunks[axis]))]
    dsk = dict(zip(keys, values))

    return Array(dsk, name, chunks, dtype)
