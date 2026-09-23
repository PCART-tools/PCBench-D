    @classmethod
    def _from_arrays(cls, arrays, columns, index, dtype=None):
        mgr = _arrays_to_mgr(arrays, columns, index, columns, dtype=dtype)
        return cls(mgr)
