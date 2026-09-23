    @property
    def _data(self):
        # dask accesses ._data directlys
        warnings.warn(
            f"{type(self).__name__}._data is a deprecated and will be removed "
            "in a future version, use ._pa_array instead",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self._pa_array
