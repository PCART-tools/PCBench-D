    def _ixs(self, i: int, axis: int = 0) -> Series:
        """
        Parameters
        ----------
        i : int
        axis : int

        Returns
        -------
        Series
        """
        # irow
        if axis == 0:
            new_mgr = self._mgr.fast_xs(i)

            # if we are a copy, mark as such
            copy = isinstance(new_mgr.array, np.ndarray) and new_mgr.array.base is None
            result = self._constructor_sliced(new_mgr, name=self.index[i]).__finalize__(
                self
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
