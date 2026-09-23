    def intersection(self, other):
        """
        Form the intersection of two Index objects. Sortedness of the result is
        not guaranteed

        Parameters
        ----------
        other : Index or array-like

        Returns
        -------
        intersection : Index
        """
        if not hasattr(other, '__iter__'):
            raise TypeError('Input must be iterable!')

        self._assert_can_do_setop(other)

        other = _ensure_index(other)

        if self.equals(other):
            return self

        if not is_dtype_equal(self.dtype,other.dtype):
            this = self.astype('O')
            other = other.astype('O')
            return this.intersection(other)

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._inner_indexer(self.values, other.values)[0]
                return self._wrap_union_result(other, result)
            except TypeError:
                pass

        try:
            indexer = self.get_indexer(other.values)
            indexer = indexer.take((indexer != -1).nonzero()[0])
        except:
            # duplicates
            indexer = self.get_indexer_non_unique(other.values)[0].unique()
            indexer = indexer[indexer != -1]

        taken = self.take(indexer)
        if self.name != other.name:
            taken.name = None
        return taken
