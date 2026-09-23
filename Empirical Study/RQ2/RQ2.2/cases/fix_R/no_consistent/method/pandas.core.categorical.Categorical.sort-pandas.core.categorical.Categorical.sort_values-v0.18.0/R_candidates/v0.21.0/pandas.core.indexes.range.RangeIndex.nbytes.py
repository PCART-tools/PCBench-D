    @cache_readonly
    def nbytes(self):
        """
        Return the number of bytes in the underlying data
        On implementations where this is undetermined (PyPy)
        assume 24 bytes for each value
        """
        return sum([getsizeof(getattr(self, v), 24) for v in
                    ['_start', '_stop', '_step']])
