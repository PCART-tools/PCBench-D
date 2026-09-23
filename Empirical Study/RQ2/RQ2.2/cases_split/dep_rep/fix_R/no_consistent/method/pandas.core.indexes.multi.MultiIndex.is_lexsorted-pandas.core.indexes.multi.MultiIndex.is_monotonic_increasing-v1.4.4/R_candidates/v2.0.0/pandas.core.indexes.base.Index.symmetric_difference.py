    def symmetric_difference(self, other, result_name=None, sort=None):
        """
        Compute the symmetric difference of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        result_name : str
        sort : bool or None, default None
            Whether to sort the resulting index. By default, the
            values are attempted to be sorted, but any TypeError from
            incomparable elements is caught by pandas.

            * None : Attempt to sort the result, but catch any TypeErrors
              from comparing incomparable elements.
            * False : Do not sort the result.
            * True : Sort the result (which may raise TypeError).

        Returns
        -------
        Index

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
        Index([1, 5], dtype='int64')
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_name_update = self._convert_can_do_setop(other)
        if result_name is None:
            result_name = result_name_update

        if not is_dtype_equal(self.dtype, other.dtype):
            self, other = self._dti_setop_align_tzs(other, "symmetric_difference")

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
        left_diff = this.take(left_indexer)

        # {other} minus {this}
        right_indexer = (indexer == -1).nonzero()[0]
        right_diff = other.take(right_indexer)

        res_values = left_diff.append(right_diff)
        result = _maybe_try_sort(res_values, sort)

        if not self._is_multi:
            return Index(result, name=result_name, dtype=res_values.dtype)
        else:
            left_diff = cast("MultiIndex", left_diff)
            if len(result) == 0:
                # result might be an Index, if other was an Index
                return left_diff.remove_unused_levels().set_names(result_name)
            return result.set_names(result_name)
