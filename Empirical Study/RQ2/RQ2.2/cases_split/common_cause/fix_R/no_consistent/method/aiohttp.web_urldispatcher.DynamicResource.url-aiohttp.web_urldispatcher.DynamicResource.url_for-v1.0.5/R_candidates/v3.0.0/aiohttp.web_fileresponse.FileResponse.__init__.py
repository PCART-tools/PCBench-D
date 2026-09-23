    def __init__(self, path, chunk_size=256*1024, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(path, str):
            path = pathlib.Path(path)

        self._path = path
        self._chunk_size = chunk_size
