def make_reader(reader, reader_name, file_type):
    def read(urlpath, blocksize=AUTO_BLOCKSIZE, collection=True,
             lineterminator=None, compression=None, sample=256000,
             enforce=False, storage_options=None, **kwargs):
        return read_pandas(reader, urlpath, blocksize=blocksize,
                           collection=collection,
                           lineterminator=lineterminator,
                           compression=compression, sample=sample,
                           enforce=enforce, storage_options=storage_options,
                           **kwargs)
    read.__doc__ = READ_DOC_TEMPLATE.format(reader=reader_name,
                                            file_type=file_type)
    read.__name__ = reader_name
    return read
