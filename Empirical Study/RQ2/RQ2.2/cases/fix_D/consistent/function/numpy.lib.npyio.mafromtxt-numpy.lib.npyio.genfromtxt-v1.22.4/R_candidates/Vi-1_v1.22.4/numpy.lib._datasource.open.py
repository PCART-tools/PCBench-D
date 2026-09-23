def open(path, mode='r', destpath=os.curdir, encoding=None, newline=None):
    """
    Open `path` with `mode` and return the file object.

    If ``path`` is an URL, it will be downloaded, stored in the
    `DataSource` `destpath` directory and opened from there.

    Parameters
    ----------
    path : str
        Local file path or URL to open.
    mode : str, optional
        Mode to open `path`. Mode 'r' for reading, 'w' for writing, 'a' to
        append. Available modes depend on the type of object specified by
        path.  Default is 'r'.
    destpath : str, optional
        Path to the directory where the source file gets downloaded to for
        use.  If `destpath` is None, a temporary directory will be created.
        The default path is the current directory.
    encoding : {None, str}, optional
        Open text file with given encoding. The default encoding will be
        what `io.open` uses.
    newline : {None, str}, optional
        Newline to use when reading text file.

    Returns
    -------
    out : file object
        The opened file.

    Notes
    -----
    This is a convenience function that instantiates a `DataSource` and
    returns the file object from ``DataSource.open(path)``.

    """

    ds = DataSource(destpath)
    return ds.open(path, mode, encoding=encoding, newline=newline)
