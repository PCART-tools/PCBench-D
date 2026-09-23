    @deprecate_kwarg(old_arg_name="v", new_arg_name="value")
    def searchsorted(self, value, side="left", sorter=None):
        """
        Find indices to insert `value` so as to maintain order.

        For full documentation, see `numpy.searchsorted`

        See Also
        --------
        numpy.searchsorted : Equivalent function.
        """

        # We are much more performant if the searched
        # indexer is the same type as the array.
        #
        # This doesn't matter for int64, but DOES
        # matter for smaller int dtypes.
        #
        # xref: https://github.com/numpy/numpy/issues/5370
        try:
            value = self.dtype.type(value)
        except ValueError:
            pass

        return super().searchsorted(value, side=side, sorter=sorter)
