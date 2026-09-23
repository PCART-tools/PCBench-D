    def _wrap_reindex_result(self, target, indexer, preserve_names: bool):
        target = self._maybe_preserve_names(target, preserve_names)
        return target
