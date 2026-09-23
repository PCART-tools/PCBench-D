def _gen_open(f):
    if isinstance(f, int):  # file descriptor
        return io.open(f, "rb", closefd=False)
    elif not isinstance(f, six.string_types):
        raise TypeError("expected {str, int, file-like}, got %s" % type(f))

    _, ext = os.path.splitext(f)
    if ext == ".gz":
        import gzip
        return gzip.open(f, "rb")
    elif ext == ".bz2":
        from bz2 import BZ2File
        return BZ2File(f, "rb")
    else:
        return open(f, "rb")
