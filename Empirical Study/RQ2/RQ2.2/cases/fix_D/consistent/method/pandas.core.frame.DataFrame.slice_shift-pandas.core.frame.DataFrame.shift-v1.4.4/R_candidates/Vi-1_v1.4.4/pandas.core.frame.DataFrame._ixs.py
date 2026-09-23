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
            new_values = self._mgr.fast_xs(i)

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

            col_mgr = self._mgr.iget(i)
            result = self._box_col_values(col_mgr, i)

            # this is a cached value, mark it so
            result._set_as_cached(label, self)
            return result
