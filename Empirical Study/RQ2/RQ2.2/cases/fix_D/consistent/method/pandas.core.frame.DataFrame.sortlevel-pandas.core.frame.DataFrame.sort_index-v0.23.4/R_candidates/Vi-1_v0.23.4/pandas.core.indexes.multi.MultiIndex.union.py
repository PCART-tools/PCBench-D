    def union(self, other):
        """
        Form the union of two MultiIndex objects, sorting if possible

        Parameters
        ----------
        other : MultiIndex or array / Index of tuples

        Returns
        -------
        Index

        >>> index.union(index2)
        """
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if len(other) == 0 or self.equals(other):
            return self

        uniq_tuples = lib.fast_unique_multiple([self._ndarray_values,
                                                other._ndarray_values])
        return MultiIndex.from_arrays(lzip(*uniq_tuples), sortorder=0,
                                      names=result_names)
