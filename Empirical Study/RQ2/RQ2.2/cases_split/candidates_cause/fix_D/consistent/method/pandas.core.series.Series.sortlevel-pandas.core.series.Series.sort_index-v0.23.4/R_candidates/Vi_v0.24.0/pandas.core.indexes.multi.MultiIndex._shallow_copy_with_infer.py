    def _shallow_copy_with_infer(self, values, **kwargs):
        # On equal MultiIndexes the difference is empty.
        # Therefore, an empty MultiIndex is returned GH13490
        if len(values) == 0:
            return MultiIndex(levels=[[] for _ in range(self.nlevels)],
                              codes=[[] for _ in range(self.nlevels)],
                              **kwargs)
        return self._shallow_copy(values, **kwargs)
