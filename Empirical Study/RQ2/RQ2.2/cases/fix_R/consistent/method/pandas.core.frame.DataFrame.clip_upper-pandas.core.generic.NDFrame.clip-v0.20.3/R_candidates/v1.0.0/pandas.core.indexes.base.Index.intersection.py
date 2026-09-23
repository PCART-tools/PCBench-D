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
        lvals = self._values
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
        except (InvalidIndexError, IncompatibleFrequency):
            # InvalidIndexError raised by get_indexer if non-unique
            # IncompatibleFrequency raised by PeriodIndex.get_indexer
            indexer = algos.unique1d(Index(rvals).get_indexer_non_unique(lvals)[0])
            indexer = indexer[indexer != -1]

        taken = other.take(indexer)
        res_name = get_op_result_name(self, other)

        if sort is None:
            taken = algos.safe_sort(taken.values)
            return self._shallow_copy(taken, name=res_name)

        taken.name = res_name
        return taken
