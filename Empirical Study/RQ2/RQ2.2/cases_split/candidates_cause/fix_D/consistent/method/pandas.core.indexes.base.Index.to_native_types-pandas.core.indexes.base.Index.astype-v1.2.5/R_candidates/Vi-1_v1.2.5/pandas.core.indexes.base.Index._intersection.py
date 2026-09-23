    def _intersection(self, other, sort=False):
        """
        intersection specialized to the case with matching dtypes.
        """
        # TODO(EA): setops-refactor, clean all this up
        lvals = self._values
        rvals = other._values

        if self.is_monotonic and other.is_monotonic:
            try:
                result = self._inner_indexer(lvals, rvals)[0]
            except TypeError:
                pass
            else:
                return algos.unique1d(result)

        try:
            indexer = Index(rvals).get_indexer(lvals)
            indexer = indexer.take((indexer != -1).nonzero()[0])
        except (InvalidIndexError, IncompatibleFrequency):
            # InvalidIndexError raised by get_indexer if non-unique
            # IncompatibleFrequency raised by PeriodIndex.get_indexer
            indexer = algos.unique1d(Index(rvals).get_indexer_non_unique(lvals)[0])
            indexer = indexer[indexer != -1]

        result = other.take(indexer).unique()._values

        if sort is None:
            result = algos.safe_sort(result)

        # Intersection has to be unique
        assert Index(result).is_unique

        return result
