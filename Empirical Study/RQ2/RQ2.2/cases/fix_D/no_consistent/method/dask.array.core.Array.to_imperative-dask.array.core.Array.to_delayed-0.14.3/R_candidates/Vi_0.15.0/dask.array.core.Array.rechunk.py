    def rechunk(self, chunks, threshold=None, block_size_limit=None):
        """ See da.rechunk for docstring """
        from . import rechunk   # avoid circular import
        return rechunk(self, chunks, threshold, block_size_limit)
