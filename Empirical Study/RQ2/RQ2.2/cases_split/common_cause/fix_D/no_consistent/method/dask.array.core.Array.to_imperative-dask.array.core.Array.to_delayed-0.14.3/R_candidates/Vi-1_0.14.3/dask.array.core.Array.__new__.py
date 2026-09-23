    def __new__(cls, dask, name, chunks, dtype, shape=None):
        self = super(Array, cls).__new__(cls)
        assert isinstance(dask, Mapping)
        if not isinstance(dask, ShareDict):
            s = ShareDict()
            s.update_with_key(dask, key=name)
            dask = s
        self.dask = dask
        self.name = name
        self._chunks = normalize_chunks(chunks, shape)
        if self._chunks is None:
            raise ValueError(chunks_none_error_message)
        if dtype is None:
            raise ValueError("You must specify the dtype of the array")
        self.dtype = np.dtype(dtype)

        for plugin in _globals.get('array_plugins', ()):
            result = plugin(self)
            if result is not None:
                self = result

        return self
