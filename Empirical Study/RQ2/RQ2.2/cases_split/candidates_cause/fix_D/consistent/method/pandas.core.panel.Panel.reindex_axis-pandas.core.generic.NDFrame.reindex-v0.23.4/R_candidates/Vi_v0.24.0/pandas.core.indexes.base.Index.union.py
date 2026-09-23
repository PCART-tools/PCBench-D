    def union(self, other, sort=True):
        """
        Form the union of two Index objects.

        Parameters
        ----------
        other : Index or array-like
        sort : bool, default True
            Sort the resulting index if possible

            .. versionadded:: 0.24.0

        Returns
        -------
        union : Index

        Examples
        --------

        >>> idx1 = pd.Index([1, 2, 3, 4])
        >>> idx2 = pd.Index([3, 4, 5, 6])
        >>> idx1.union(idx2)
        Int64Index([1, 2, 3, 4, 5, 6], dtype='int64')
        """
        self._assert_can_do_setop(other)
        other = ensure_index(other)

        if len(other) == 0 or self.equals(other):
            return self._get_reconciled_name_object(other)

        if len(self) == 0:
            return other._get_reconciled_name_object(self)

        # TODO: is_dtype_union_equal is a hack around
        # 1. buggy set ops with duplicates (GH #13432)
        # 2. CategoricalIndex lacking setops (GH #10186)
        # Once those are fixed, this workaround can be removed
        if not is_dtype_union_equal(self.dtype, other.dtype):
            this = self.astype('O')
            other = other.astype('O')
            return this.union(other, sort=sort)

        # TODO(EA): setops-refactor, clean all this up
        if is_period_dtype(self) or is_datetime64tz_dtype(self):
            lvals = self._ndarray_values
        else:
            lvals = self._values
        if is_period_dtype(other) or is_datetime64tz_dtype(other):
            rvals = other._ndarray_values
        else:
            rvals = other._values

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._outer_indexer(lvals, rvals)[0]
            except TypeError:
                # incomparable objects
                result = list(lvals)

                # worth making this faster? a very unusual case
                value_set = set(lvals)
                result.extend([x for x in rvals if x not in value_set])
        else:
            indexer = self.get_indexer(other)
            indexer, = (indexer == -1).nonzero()

            if len(indexer) > 0:
                other_diff = algos.take_nd(rvals, indexer,
                                           allow_fill=False)
                result = _concat._concat_compat((lvals, other_diff))

            else:
                result = lvals

            if sort:
                try:
                    result = sorting.safe_sort(result)
                except TypeError as e:
                    warnings.warn("{}, sort order is undefined for "
                                  "incomparable objects".format(e),
                                  RuntimeWarning, stacklevel=3)

        # for subclasses
        return self._wrap_setop_result(other, result)
