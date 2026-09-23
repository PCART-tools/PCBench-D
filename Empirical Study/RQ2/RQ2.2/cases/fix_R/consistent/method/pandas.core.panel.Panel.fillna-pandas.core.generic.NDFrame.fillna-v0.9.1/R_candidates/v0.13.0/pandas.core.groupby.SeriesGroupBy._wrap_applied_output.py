    def _wrap_applied_output(self, keys, values, not_indexed_same=False):
        if len(keys) == 0:
            return Series([])

        def _get_index():
            if self.grouper.nkeys > 1:
                index = MultiIndex.from_tuples(keys, names=self.grouper.names)
            else:
                index = Index(keys, name=self.grouper.names[0])
            return index

        if isinstance(values[0], dict):
            # GH #823
            index = _get_index()
            return DataFrame(values, index=index).stack()

        if isinstance(values[0], (Series, dict)):
            return self._concat_objects(keys, values,
                                        not_indexed_same=not_indexed_same)
        elif isinstance(values[0], DataFrame):
            # possible that Series -> DataFrame by applied function
            return self._concat_objects(keys, values,
                                        not_indexed_same=not_indexed_same)
        else:
            return Series(values, index=_get_index())
