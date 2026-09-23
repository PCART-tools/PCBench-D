    @contextmanager  # noqa: T484
    def TemporaryDirectoryName(suffix=None):
        with tempfile.TemporaryDirectory(suffix=suffix) as d:
            yield d
