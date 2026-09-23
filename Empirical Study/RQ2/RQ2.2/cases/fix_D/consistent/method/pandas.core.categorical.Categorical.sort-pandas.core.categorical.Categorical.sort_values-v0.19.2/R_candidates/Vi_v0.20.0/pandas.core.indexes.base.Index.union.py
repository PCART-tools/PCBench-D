    def union(self, other):
        """
        Form the union of two Index objects and sorts if possible.

        Parameters
        ----------
        other : Index or array-like

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
        other = _ensure_index(other)

        if len(other) == 0 or self.equals(other):
            return self._get_consensus_name(other)

        if len(self) == 0:
            return other._get_consensus_name(self)

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype('O')
            other = other.astype('O')
            return this.union(other)

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._outer_indexer(self._values, other._values)[0]
            except TypeError:
                # incomparable objects
                result = list(self._values)

                # worth making this faster? a very unusual case
                value_set = set(self._values)
                result.extend([x for x in other._values if x not in value_set])
        else:
            indexer = self.get_indexer(other)
            indexer, = (indexer == -1).nonzero()

            if len(indexer) > 0:
                other_diff = algos.take_nd(other._values, indexer,
                                           allow_fill=False)
                result = _concat._concat_compat((self._values, other_diff))

                try:
                    self._values[0] < other_diff[0]
                except TypeError as e:
                    warnings.warn("%s, sort order is undefined for "
                                  "incomparable objects" % e, RuntimeWarning,
                                  stacklevel=3)
                else:
                    types = frozenset((self.inferred_type,
                                       other.inferred_type))
                    if not types & _unsortable_types:
                        result.sort()

            else:
                result = self._values

                try:
                    result = np.sort(result)
                except TypeError as e:
                    warnings.warn("%s, sort order is undefined for "
                                  "incomparable objects" % e, RuntimeWarning,
                                  stacklevel=3)

        # for subclasses
        return self._wrap_union_result(other, result)
