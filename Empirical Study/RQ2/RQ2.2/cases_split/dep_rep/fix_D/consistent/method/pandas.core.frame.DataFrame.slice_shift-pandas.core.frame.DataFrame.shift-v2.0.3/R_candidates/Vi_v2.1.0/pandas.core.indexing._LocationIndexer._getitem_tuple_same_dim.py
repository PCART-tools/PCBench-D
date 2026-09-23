    @final
    def _getitem_tuple_same_dim(self, tup: tuple):
        """
        Index with indexers that should return an object of the same dimension
        as self.obj.

        This is only called after a failed call to _getitem_lowerdim.
        """
        retval = self.obj
        # Selecting columns before rows is signficiantly faster
        start_val = (self.ndim - len(tup)) + 1
        for i, key in enumerate(reversed(tup)):
            i = self.ndim - i - start_val
            if com.is_null_slice(key):
                continue

            retval = getattr(retval, self.name)._getitem_axis(key, axis=i)
            # We should never have retval.ndim < self.ndim, as that should
            #  be handled by the _getitem_lowerdim call above.
            assert retval.ndim == self.ndim

        if retval is self.obj:
            # if all axes were a null slice (`df.loc[:, :]`), ensure we still
            # return a new object (https://github.com/pandas-dev/pandas/pull/49469)
            retval = retval.copy(deep=False)

        return retval
