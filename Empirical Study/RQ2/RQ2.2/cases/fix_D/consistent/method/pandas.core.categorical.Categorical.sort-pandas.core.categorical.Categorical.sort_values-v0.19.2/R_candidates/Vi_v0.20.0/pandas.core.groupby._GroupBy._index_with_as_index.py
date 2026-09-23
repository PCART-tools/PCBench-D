    def _index_with_as_index(self, b):
        """
        Take boolean mask of index to be returned from apply, if as_index=True

        """
        # TODO perf, it feels like this should already be somewhere...
        from itertools import chain
        original = self._selected_obj.index
        gp = self.grouper
        levels = chain((gp.levels[i][gp.labels[i][b]]
                        for i in range(len(gp.groupings))),
                       (original._get_level_values(i)[b]
                        for i in range(original.nlevels)))
        new = MultiIndex.from_arrays(list(levels))
        new.names = gp.names + original.names
        return new
