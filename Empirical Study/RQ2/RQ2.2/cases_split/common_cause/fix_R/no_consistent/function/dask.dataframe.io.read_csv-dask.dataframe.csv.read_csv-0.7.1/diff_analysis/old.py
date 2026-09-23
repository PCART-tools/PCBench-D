

@wraps(pd.read_csv)
def read_csv(fn, *args, **kwargs):
    chunkbytes = kwargs.pop('chunkbytes', 2**25)  # 50 MB
    categorize = kwargs.pop('categorize', None)
    index = kwargs.pop('index', None)
    if index and categorize == None:
        categorize = True

    kwargs = fill_kwargs(fn, args, kwargs)

    # Handle glob strings
    if '*' in fn:
        return concat([read_csv(f, *args, **kwargs) for f in sorted(glob(fn))])

    token = tokenize(os.path.getmtime(fn), args, kwargs)
    name = 'read-csv-%s-%s' % (fn, token)

    columns = kwargs.pop('columns')
    header = kwargs.pop('header')

    if 'nrows' in kwargs:  # Just create single partition
        dsk = {(name, 0): (apply, pd.read_csv, (fn,),
                                  assoc(kwargs, 'header', header))}
        result = DataFrame(dsk, name, columns, [None, None])

    else:
        # Chunk sizes and numbers
        total_bytes = file_size(fn, kwargs['compression'])
        nchunks = int(ceil(total_bytes / chunkbytes))
        divisions = [None] * (nchunks + 1)

        first_kwargs = merge(kwargs, dict(header=header, compression=None))
        rest_kwargs = merge(kwargs, dict(header=None, compression=None))

        # Create dask graph
        dsk = dict(((name, i), (_read_csv, fn, i, chunkbytes,
                                           kwargs['compression'], rest_kwargs))
                   for i in range(1, nchunks))

        dsk[(name, 0)] = (_read_csv, fn, 0, chunkbytes, kwargs['compression'],
                                     first_kwargs)

        result = DataFrame(dsk, name, columns, divisions)

    if categorize or index:
        categories, quantiles = categories_and_quantiles(fn, args, kwargs,
                                                         index, categorize,
                                                         chunkbytes=chunkbytes)

    if categorize:
        func = partial(categorize_block, categories=categories)
        result = result.map_partitions(func, columns=columns)

    if index:
        result = set_partition(result, index, quantiles)

    return result
