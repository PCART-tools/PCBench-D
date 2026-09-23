    def _wrap_reindex_result(self, target, indexer, preserve_names: bool):
        if not isinstance(target, MultiIndex):
            if indexer is None:
                target = self
            elif (indexer >= 0).all():
                target = self.take(indexer)
            else:
                try:
                    target = MultiIndex.from_tuples(target)
                except TypeError:
                    # not all tuples, see test_constructor_dict_multiindex_reindex_flat
                    return target

        target = self._maybe_preserve_names(target, preserve_names)
        return target
