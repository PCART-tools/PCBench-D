class maybe_buffered_partd(object):
    """If serialized, will return non-buffered partd. Otherwise returns a
    buffered partd"""
    def __init__(self, buffer=True, tempdir=None):
        self.tempdir = tempdir or config.get('temporary_directory', None)
        self.buffer = buffer

    def __reduce__(self):
        if self.tempdir:
            return (maybe_buffered_partd, (False, self.tempdir))
        else:
            return (maybe_buffered_partd, (False,))

    def __call__(self, *args, **kwargs):
        import partd
        if self.tempdir:
            file = partd.File(dir=self.tempdir)
        else:
            file = partd.File()
        if self.buffer:
            return partd.PandasBlocks(partd.Buffer(partd.Dict(), file))
        else:
            return partd.PandasBlocks(file)
