    def _ixs(self, i: int, axis: int = 0):
        """
        Parameters
        ----------
        i : int
        axis : int

        Notes
        -----
        If slice passed, the resulting data will be a view.
        """
        # irow
        if axis == 0:
            label = self.index[i]
            new_values = self._data.fast_xs(i)
            if is_scalar(new_values):
                return new_values

            # if we are a copy, mark as such
            copy = isinstance(new_values, np.ndarray) and new_values.base is None
            result = self._constructor_sliced(
                new_values,
                index=self.columns,
                name=self.index[i],
                dtype=new_values.dtype,
            )
            result._set_is_copy(self, copy=copy)
            return result

        # icol
        else:
            label = self.columns[i]

            # if the values returned are not the same length
            # as the index (iow a not found value), iget returns
            # a 0-len ndarray. This is effectively catching
            # a numpy error (as numpy should really raise)
            values = self._data.iget(i)

            if len(self.index) and not len(values):
                values = np.array([np.nan] * len(self.index), dtype=object)
            result = self._box_col_values(values, label)

            # this is a cached value, mark it so
            result._set_as_cached(label, self)

            return result
