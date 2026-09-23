class OpenFile(object):
    """
    File-like object to be used in a context

    These instances are safe to serialize, as the low-level file object
    is not created until invoked using `with`.

    Parameters
    ----------
    fs : FileSystem
        The file system to use for opening the file. Should match the interface
        of ``dask.bytes.local.LocalFileSystem``.
    path : str
        Location to open
    mode : str like 'rb', optional
        Mode of the opened file
    compression : str or None, optional
        Compression to apply
    encoding : str or None, optional
        The encoding to use if opened in text mode.
    errors : str or None, optional
        How to handle encoding errors if opened in text mode.
    """
    def __init__(self, fs, path, mode='rb', compression=None, encoding=None,
                 errors=None):
        self.fs = fs
        self.path = path
        self.mode = mode
        self.compression = get_compression(path, compression)
        self.encoding = encoding
        self.errors = errors
        self.fobjects = []

    def __reduce__(self):
        return (OpenFile, (self.fs, self.path, self.mode, self.compression,
                           self.encoding, self.errors))

    def __enter__(self):
        mode = self.mode.replace('t', '').replace('b', '') + 'b'

        f = SeekableFile(self.fs.open(self.path, mode=mode))

        fobjects = [f]

        if self.compression is not None:
            compress = merge(seekable_files, compress_files)[self.compression]
            f = compress(f, mode=mode)
            fobjects.append(f)

        if 't' in self.mode:
            f = io.TextIOWrapper(f, encoding=self.encoding,
                                 errors=self.errors)
            fobjects.append(f)

        self.fobjects = fobjects
        return f

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Close all encapsulated file objects"""
        for f in reversed(self.fobjects):
            f.close()
        self.fobjects = []
