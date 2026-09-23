    @Appender(_index_shared_docs["intersection"])
    def intersection(self, other, sort=False):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other = ensure_index(other)

        if self.equals(other):
            return self._get_reconciled_name_object(other)

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype("O")
            other = other.astype("O")
            return this.intersection(other, sort=sort)

        # TODO(EA): setops-refactor, clean all this up
        if is_period_dtype(self):
            lvals = self._ndarray_values
        else:
            lvals = self._values
        if is_period_dtype(other):
            rvals = other._ndarray_values
        else:
            rvals = other._values

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._inner_indexer(lvals, rvals)[0]
                return self._wrap_setop_result(other, result)
            except TypeError:
                pass

        try:
            indexer = Index(rvals).get_indexer(lvals)
            indexer = indexer.take((indexer != -1).nonzero()[0])
        except Exception:
            # duplicates
            indexer = algos.unique1d(Index(rvals).get_indexer_non_unique(lvals)[0])
            indexer = indexer[indexer != -1]

        taken = other.take(indexer)

        if sort is None:
            taken = sorting.safe_sort(taken.values)
            if self.name != other.name:
                name = None
            else:
                name = self.name
            return self._shallow_copy(taken, name=name)

        if self.name != other.name:
            taken.name = None

        return taken
