def open(filename, mode='rb', compression=None, **kwargs):
    if compression == 'infer':
        compression = infer_compression(filename)
    return opens.get(compression, io.open)(filename, mode, **kwargs)
