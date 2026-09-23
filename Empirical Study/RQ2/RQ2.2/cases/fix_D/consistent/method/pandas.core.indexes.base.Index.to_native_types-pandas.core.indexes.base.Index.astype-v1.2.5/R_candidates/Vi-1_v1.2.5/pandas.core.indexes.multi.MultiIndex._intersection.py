    def _intersection(self, other, sort=False):
        other, result_names = self._convert_can_do_setop(other)

        if not self._is_comparable_dtype(other.dtype):
            # The intersection is empty
            return self[:0].rename(result_names)

        lvals = self._values
        rvals = other._values

        uniq_tuples = None  # flag whether _inner_indexer was successful
        if self.is_monotonic and other.is_monotonic:
            try:
                inner_tuples = self._inner_indexer(lvals, rvals)[0]
                sort = False  # inner_tuples is already sorted
            except TypeError:
                pass
            else:
                uniq_tuples = algos.unique(inner_tuples)

        if uniq_tuples is None:
            other_uniq = set(rvals)
            seen = set()
            # pandas\core\indexes\multi.py:3503: error: "add" of "set" does not
            # return a value  [func-returns-value]
            uniq_tuples = [
                x
                for x in lvals
                if x in other_uniq
                and not (x in seen or seen.add(x))  # type: ignore[func-returns-value]
            ]

        if sort is None:
            uniq_tuples = sorted(uniq_tuples)

        if len(uniq_tuples) == 0:
            return MultiIndex(
                levels=self.levels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )
        else:
            return MultiIndex.from_arrays(
                zip(*uniq_tuples), sortorder=0, names=result_names
            )
