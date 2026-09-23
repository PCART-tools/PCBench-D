    def union(self, other, sort=None):
        """
        Form the union of two MultiIndex objects

        Parameters
        ----------
        other : MultiIndex or array / Index of tuples
        sort : False or None, default None
            Whether to sort the resulting Index.

            * None : Sort the result, except when

              1. `self` and `other` are equal.
              2. `self` has length 0.
              3. Some values in `self` or `other` cannot be compared.
                 A RuntimeWarning is issued in this case.

            * False : do not sort the result.

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default value from ``True`` to ``None``
               (without change in behaviour).

        Returns
        -------
        Index

        >>> index.union(index2)
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if len(other) == 0 or self.equals(other):
            return self

        # TODO: Index.union returns other when `len(self)` is 0.

        uniq_tuples = lib.fast_unique_multiple(
            [self._ndarray_values, other._ndarray_values], sort=sort
        )

        return MultiIndex.from_arrays(
            zip(*uniq_tuples), sortorder=0, names=result_names
        )
