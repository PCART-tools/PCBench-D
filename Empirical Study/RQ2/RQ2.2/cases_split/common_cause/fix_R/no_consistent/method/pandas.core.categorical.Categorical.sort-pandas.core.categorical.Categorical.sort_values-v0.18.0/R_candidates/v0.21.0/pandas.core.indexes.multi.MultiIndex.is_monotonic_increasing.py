    @cache_readonly
    def is_monotonic_increasing(self):
        """
        return if the index is monotonic increasing (only equal or
        increasing) values.
        """

        # reversed() because lexsort() wants the most significant key last.
        values = [self._get_level_values(i).values
                  for i in reversed(range(len(self.levels)))]
        try:
            sort_order = np.lexsort(values)
            return Index(sort_order).is_monotonic
        except TypeError:

            # we have mixed types and np.lexsort is not happy
            return Index(self.values).is_monotonic
