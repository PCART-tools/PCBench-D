    def searchsorted(self, v, side='left', sorter=None):
        """
        Find indices where elements of v should be inserted
        in a to maintain order.

        For full documentation, see `numpy.searchsorted`

        See Also
        --------
        numpy.searchsorted : equivalent function
        """

        # we are much more performant if the searched
        # indexer is the same type as the array
        # this doesn't matter for int64, but DOES
        # matter for smaller int dtypes
        # https://github.com/numpy/numpy/issues/5370
        try:
            v = self.dtype.type(v)
        except:
            pass
        return super(FrozenNDArray, self).searchsorted(
            v, side=side, sorter=sorter)
