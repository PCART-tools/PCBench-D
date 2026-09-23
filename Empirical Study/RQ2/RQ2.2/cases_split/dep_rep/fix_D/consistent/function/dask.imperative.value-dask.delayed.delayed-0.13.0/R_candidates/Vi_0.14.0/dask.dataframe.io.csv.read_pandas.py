def read_pandas(reader, urlpath, blocksize=AUTO_BLOCKSIZE, collection=True,
                lineterminator=None, compression=None, sample=256000,
                enforce=False, storage_options=None, **kwargs):
    reader_name = reader.__name__
    if lineterminator is not None and len(lineterminator) == 1:
        kwargs['lineterminator'] = lineterminator
    else:
        lineterminator = '\n'
    if 'index' in kwargs or 'index_col' in kwargs:
        raise ValueError("Keyword 'index' not supported "
                         "dd.{0}(...).set_index('my-index') "
                         "instead".format(reader_name))
    for kw in ['iterator', 'chunksize']:
        if kw in kwargs:
            raise ValueError("{0} not supported for "
                             "dd.{1}".format(kw, reader_name))
    if kwargs.get('nrows', None):
        raise ValueError("The 'nrows' keyword is not supported by "
                         "`dd.{0}`. To achieve the same behavior, it's "
                         "recommended to use `dd.{0}(...)."
                         "head(n=nrows)`".format(reader_name))
    if isinstance(kwargs.get('skiprows'), list):
        raise TypeError("List of skiprows not supported for "
                        "dd.{0}".format(reader_name))
    if isinstance(kwargs.get('header'), list):
        raise TypeError("List of header rows not supported for "
                        "dd.{0}".format(reader_name))

    if blocksize and compression not in seekable_files:
        warn("Warning %s compression does not support breaking apart files\n"
             "Please ensure that each individual file can fit in memory and\n"
             "use the keyword ``blocksize=None to remove this message``\n"
             "Setting ``blocksize=None``" % compression)
        blocksize = None
    if compression not in seekable_files and compression not in cfiles:
        raise NotImplementedError("Compression format %s not installed" %
                                  compression)

    b_lineterminator = lineterminator.encode()
    sample, values = read_bytes(urlpath, delimiter=b_lineterminator,
                                blocksize=blocksize,
                                sample=sample,
                                compression=compression,
                                **(storage_options or {}))

    if not isinstance(values[0], (tuple, list)):
        values = [values]

    if kwargs.get('header', 'infer') is None:
        header = b''
    else:
        header = sample.split(b_lineterminator)[0] + b_lineterminator

    head = reader(BytesIO(sample), **kwargs)

    return text_blocks_to_pandas(reader, values, header, head, kwargs,
                                 collection=collection, enforce=enforce)
