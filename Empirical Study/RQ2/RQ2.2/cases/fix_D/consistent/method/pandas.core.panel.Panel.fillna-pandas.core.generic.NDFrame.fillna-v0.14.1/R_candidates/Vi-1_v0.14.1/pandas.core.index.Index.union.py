    def union(self, other):
        """
        Form the union of two Index objects and sorts if possible

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        union : Index
        """
        if not hasattr(other, '__iter__'):
            raise TypeError('Input must be iterable.')

        if len(other) == 0 or self.equals(other):
            return self

        if len(self) == 0:
            return _ensure_index(other)

        self._assert_can_do_setop(other)

        if self.dtype != other.dtype:
            this = self.astype('O')
            other = other.astype('O')
            return this.union(other)

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._outer_indexer(self, other.values)[0]
            except TypeError:
                # incomparable objects
                result = list(self.values)

                # worth making this faster? a very unusual case
                value_set = set(self.values)
                result.extend([x for x in other.values if x not in value_set])
        else:
            indexer = self.get_indexer(other)
            indexer, = (indexer == -1).nonzero()

            if len(indexer) > 0:
                other_diff = com.take_nd(other.values, indexer,
                                         allow_fill=False)
                result = com._concat_compat((self.values, other_diff))

                try:
                    self.values[0] < other_diff[0]
                except TypeError as e:
                    warnings.warn("%s, sort order is undefined for "
                                  "incomparable objects" % e, RuntimeWarning)
                else:
                    types = frozenset((self.inferred_type,
                                       other.inferred_type))
                    if not types & _unsortable_types:
                        result.sort()

            else:
                result = self.values

                try:
                    result = np.sort(result)
                except TypeError as e:
                    warnings.warn("%s, sort order is undefined for "
                                  "incomparable objects" % e, RuntimeWarning)

        # for subclasses
        return self._wrap_union_result(other, result)
