    def _union(self, other, sort):
        """
        Specific union logic should go here. In subclasses, union behavior
        should be overwritten here rather than in `self.union`.

        Parameters
        ----------
        other : Index or array-like
        sort : False or None, default False
            Whether to sort the resulting index.

            * False : do not sort the result.
            * None : sort the result, except when `self` and `other` are equal
              or when the values cannot be compared.

        Returns
        -------
        Index
        """

        if not len(other) or self.equals(other):
            return self._get_reconciled_name_object(other)

        if not len(self):
            return other._get_reconciled_name_object(self)

        # TODO(EA): setops-refactor, clean all this up
        if is_period_dtype(self) or is_datetime64tz_dtype(self):
            lvals = self._ndarray_values
        else:
            lvals = self._values
        if is_period_dtype(other) or is_datetime64tz_dtype(other):
            rvals = other._ndarray_values
        else:
            rvals = other._values

        if sort is None and self.is_monotonic and other.is_monotonic:
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
                other_diff = algos.take_nd(rvals, indexer, allow_fill=False)
                result = _concat._concat_compat((lvals, other_diff))

            else:
                result = lvals

            if sort is None:
                try:
                    result = sorting.safe_sort(result)
                except TypeError as e:
                    warnings.warn(
                        "{}, sort order is undefined for "
                        "incomparable objects".format(e),
                        RuntimeWarning,
                        stacklevel=3,
                    )

        # for subclasses
        return self._wrap_setop_result(other, result)
