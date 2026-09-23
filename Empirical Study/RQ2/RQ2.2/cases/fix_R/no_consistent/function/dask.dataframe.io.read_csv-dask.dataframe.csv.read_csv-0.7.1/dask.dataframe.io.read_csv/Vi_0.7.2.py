

@wraps(pd.read_csv)
def read_csv(fn, *args, **kwargs):
    if 'nrows' in kwargs:  # Just create single partition
        df = read_csv(fn, *args, **dissoc(kwargs, 'nrows'))
        return df.head(kwargs['nrows'], compute=False)

    chunkbytes = kwargs.pop('chunkbytes', 2**25)  # 50 MB
    index = kwargs.pop('index', None)
    kwargs = kwargs.copy()

    kwargs = fill_kwargs(fn, args, kwargs)

    # Handle glob strings
    if '*' in fn:
        from .multi import concat
        return concat([read_csv(f, *args, **kwargs) for f in sorted(glob(fn))])

    token = tokenize(os.path.getmtime(fn), args, kwargs)
    name = 'read-csv-%s-%s' % (fn, token)
    bom = get_bom(fn)

    columns = kwargs.pop('columns')
    header = kwargs.pop('header')

    # Chunk sizes and numbers
    total_bytes = file_size(fn, kwargs['compression'])
    nchunks = int(ceil(total_bytes / chunkbytes))
    divisions = [None] * (nchunks + 1)

    first_kwargs = merge(kwargs, dict(header=header, compression=None))
    rest_kwargs = merge(kwargs, dict(header=None, compression=None))

    # Create dask graph
    dsk = dict(((name, i), (_read_csv, fn, i, chunkbytes,
                                       kwargs['compression'], rest_kwargs,
                                       bom))
               for i in range(1, nchunks))

    dsk[(name, 0)] = (_read_csv, fn, 0, chunkbytes, kwargs['compression'],
                                 first_kwargs, b'')

    result = DataFrame(dsk, name, columns, divisions)

    if index:
        result = result.set_index(index)

    return result
