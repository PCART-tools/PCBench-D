    @cache_readonly
    def is_monotonic_increasing(self) -> bool:
        """
        return if the index is monotonic increasing (only equal or
        increasing) values.
        """

        if all(x.is_monotonic for x in self.levels):
            # If each level is sorted, we can operate on the codes directly. GH27495
            return libalgos.is_lexsorted(
                [x.astype("int64", copy=False) for x in self.codes]
            )

        # reversed() because lexsort() wants the most significant key last.
        values = [
            self._get_level_values(i).values for i in reversed(range(len(self.levels)))
        ]
        try:
            sort_order = np.lexsort(values)
            return Index(sort_order).is_monotonic
        except TypeError:

            # we have mixed types and np.lexsort is not happy
            return Index(self.values).is_monotonic
