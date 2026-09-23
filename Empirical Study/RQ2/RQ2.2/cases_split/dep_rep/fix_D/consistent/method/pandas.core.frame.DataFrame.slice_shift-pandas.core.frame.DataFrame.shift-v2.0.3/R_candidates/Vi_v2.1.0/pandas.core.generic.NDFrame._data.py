    @final
    @property
    def _data(self):
        # GH#33054 retained because some downstream packages uses this,
        #  e.g. fastparquet
        # GH#33333
        warnings.warn(
            f"{type(self).__name__}._data is deprecated and will be removed in "
            "a future version. Use public APIs instead.",
            DeprecationWarning,
            stacklevel=find_stack_level(),
        )
        return self._mgr
