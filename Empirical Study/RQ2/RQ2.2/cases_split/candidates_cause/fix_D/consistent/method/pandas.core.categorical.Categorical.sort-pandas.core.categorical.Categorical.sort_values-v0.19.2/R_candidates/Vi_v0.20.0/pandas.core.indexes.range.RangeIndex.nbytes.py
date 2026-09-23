    @cache_readonly
    def nbytes(self):
        """ return the number of bytes in the underlying data """
        return sum([getsizeof(getattr(self, v)) for v in
                    ['_start', '_stop', '_step']])
