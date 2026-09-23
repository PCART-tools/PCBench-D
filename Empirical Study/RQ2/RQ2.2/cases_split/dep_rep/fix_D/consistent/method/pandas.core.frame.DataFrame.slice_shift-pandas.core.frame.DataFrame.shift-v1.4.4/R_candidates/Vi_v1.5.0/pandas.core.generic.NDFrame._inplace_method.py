    @final
    def _inplace_method(self, other, op):
        """
        Wrap arithmetic method to operate inplace.
        """
        result = op(self, other)

        if (
            self.ndim == 1
            and result._indexed_same(self)
            and is_dtype_equal(result.dtype, self.dtype)
        ):
            # GH#36498 this inplace op can _actually_ be inplace.
            self._values[:] = result._values
            return self

        # Delete cacher
        self._reset_cacher()

        # this makes sure that we are aligned like the input
        # we are updating inplace so we want to ignore is_copy
        self._update_inplace(
            result.reindex_like(self, copy=False), verify_is_copy=False
        )
        return self
