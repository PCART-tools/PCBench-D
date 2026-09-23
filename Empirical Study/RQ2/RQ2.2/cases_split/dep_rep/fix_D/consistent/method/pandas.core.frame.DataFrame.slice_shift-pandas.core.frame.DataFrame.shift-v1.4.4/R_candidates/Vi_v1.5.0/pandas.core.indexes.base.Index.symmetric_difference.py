    def symmetric_difference(self, other, result_name=None, sort=None):
        """
        Compute the symmetric difference of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        result_name : str
        sort : False or None, default None
            Whether to sort the resulting index. By default, the
            values are attempted to be sorted, but any TypeError from
            incomparable elements is caught by pandas.

            * None : Attempt to sort the result, but catch any TypeErrors
              from comparing incomparable elements.
            * False : Do not sort the result.

        Returns
        -------
        symmetric_difference : Index

        Notes
        -----
        ``symmetric_difference`` contains elements that appear in either
        ``idx1`` or ``idx2`` but not both. Equivalent to the Index created by
        ``idx1.difference(idx2) | idx2.difference(idx1)`` with duplicates
        dropped.

        Examples
        --------
        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([2, 3, 4, 5])
        >>> idx1.symmetric_difference(idx2)
        Int64Index([1, 5], dtype='int64')
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_name_update = self._convert_can_do_setop(other)
        if result_name is None:
            result_name = result_name_update

        if not is_dtype_equal(self.dtype, other.dtype):
            self._deprecate_dti_setop(other, "symmetric_difference")

        if not self._should_compare(other):
            return self.union(other, sort=sort).rename(result_name)

        elif not is_dtype_equal(self.dtype, other.dtype):
            dtype = self._find_common_type_compat(other)
            this = self.astype(dtype, copy=False)
            that = other.astype(dtype, copy=False)
            return this.symmetric_difference(that, sort=sort).rename(result_name)

        this = self.unique()
        other = other.unique()
        indexer = this.get_indexer_for(other)

        # {this} minus {other}
        common_indexer = indexer.take((indexer != -1).nonzero()[0])
        left_indexer = np.setdiff1d(
            np.arange(this.size), common_indexer, assume_unique=True
        )
        left_diff = this._values.take(left_indexer)

        # {other} minus {this}
        right_indexer = (indexer == -1).nonzero()[0]
        right_diff = other._values.take(right_indexer)

        res_values = concat_compat([left_diff, right_diff])
        res_values = _maybe_try_sort(res_values, sort)

        # pass dtype so we retain object dtype
        result = Index(res_values, name=result_name, dtype=res_values.dtype)

        if self._is_multi:
            self = cast("MultiIndex", self)
            if len(result) == 0:
                # On equal symmetric_difference MultiIndexes the difference is empty.
                # Therefore, an empty MultiIndex is returned GH#13490
                return type(self)(
                    levels=[[] for _ in range(self.nlevels)],
                    codes=[[] for _ in range(self.nlevels)],
                    names=result.name,
                )
            return type(self).from_tuples(result, names=result.name)

        return result
