def read_bytes(path, s3=None, delimiter=None, not_zero=False, blocksize=2**27,
               sample=True, compression=None, **kwargs):
    """ Convert location in S3 to a list of delayed values

    Parameters
    ----------
    path: string
        location in S3
    s3: S3FileSystem
    delimiter: bytes
        An optional delimiter, like ``b'\n'`` on which to split blocks of bytes
    not_zero: force seek of start-of-file delimiter, discarding header
    blocksize: int (=128MB)
        Chunk size
    sample: bool, int
        Whether or not to return a sample from the first 10k bytes
    compression: string or None
        String like 'gzip' or 'xz'.  Must support efficient random access.
    **kwargs: dict
        Extra keywords to send to boto3 session (anon, key, secret...) if
        ``s3`` is None.

    Returns
    -------
    10kB sample header and list of ``dask.Delayed`` objects or list of lists of
    delayed objects if ``path`` is a globstring.
    """
    bucket = kwargs.pop('host', '')
    s3_path = bucket + path
    if s3 is None:
        s3 = _get_s3(**kwargs)

    if '*' in path:
        filenames = sorted(s3.glob(s3_path))
        if not filenames:
            raise IOError("No such files: '%s'" % s3_path)
        sample, first = read_bytes(filenames[0], s3, delimiter, not_zero,
                                   blocksize, sample=True,
                                   compression=compression)
        rest = [read_bytes(f, s3, delimiter, not_zero, blocksize,
                       sample=False, compression=compression)[1]
                for f in filenames[1:]]
        return sample, [first] + rest
    else:
        if blocksize is None:
            offsets = [0]
        else:
            size = getsize(s3_path, compression, s3)
            offsets = list(range(0, size, blocksize))
            if not_zero:
                offsets[0] = 1

        info = s3.ls(s3_path, detail=True)[0]

        token = tokenize(info['ETag'], delimiter, blocksize, not_zero, compression)

        s3_storage_options = s3.get_delegated_s3pars()

        logger.debug("Read %d blocks of binary bytes from %s", len(offsets), s3_path)

        delayed_read_block_from_s3 = delayed(read_block_from_s3)
        values = [delayed_read_block_from_s3(s3_path, offset, blocksize,
                    delimiter=delimiter, compression=compression,
                    dask_key_name='read-block-s3-%s-%d' % (token, offset),
                    **s3_storage_options)
                    for offset in offsets]

        if sample:
            if isinstance(sample, int) and not isinstance(sample, bool):
                nbytes = sample
            else:
                nbytes = 10000
            sample = read_block_from_s3(s3_path, 0, nbytes, s3,
                                        delimiter, compression, **kwargs)

        return sample, values
