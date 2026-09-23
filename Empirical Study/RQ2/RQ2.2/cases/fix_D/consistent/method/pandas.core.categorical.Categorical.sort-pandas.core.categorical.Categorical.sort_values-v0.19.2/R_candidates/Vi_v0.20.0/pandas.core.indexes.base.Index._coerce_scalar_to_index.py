    def _coerce_scalar_to_index(self, item):
        """
        we need to coerce a scalar to a compat for our index type

        Parameters
        ----------
        item : scalar item to coerce
        """
        dtype = self.dtype

        if self._is_numeric_dtype and isnull(item):
            # We can't coerce to the numeric dtype of "self" (unless
            # it's float) if there are NaN values in our output.
            dtype = None

        return Index([item], dtype=dtype, **self._get_attributes_dict())
