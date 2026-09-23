def read_bytes(path, delimiter=None, not_zero=False, blocksize=2**27,
        sample=True, compression=None):
    """ See dask.bytes.core.read_bytes for docstring """
    if '*' in path:
        filenames = list(map(os.path.abspath, sorted(glob(path))))
        sample, first = read_bytes(filenames[0], delimiter, not_zero,
                                   blocksize, sample=True,
                                   compression=compression)
        rest = [read_bytes(f, delimiter, not_zero, blocksize, sample=False,
                           compression=compression)[1]
                for f in filenames[1:]]
        return sample, [first] + rest
    else:
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        if blocksize is None:
            offsets = [0]
        else:
            size = getsize(path, compression)

            offsets = list(range(0, size, blocksize))
            if not_zero:
                offsets[0] = 1

        token = tokenize(path, delimiter, blocksize, not_zero, compression,
                         os.path.getmtime(path))

        logger.debug("Read %d blocks of binary bytes from %s", len(offsets), path)
        f = delayed(read_block_from_file)

        values = [f(path, offset, blocksize, delimiter, compression,
                    dask_key_name='read-file-block-%s-%d' % (token, offset))
                  for offset in offsets]

        if sample:
            if sample is not True:
                nbytes = sample
            else:
                nbytes = 10000
            sample = read_block_from_file(path, 0, nbytes, None, compression)

        return sample, values
