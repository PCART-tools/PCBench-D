    @Appender(_index_shared_docs['get_indexer_non_unique'] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = _ensure_index(target)
        pself, ptarget = self._maybe_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer_non_unique(ptarget)

        if self.is_all_dates:
            self = Index(self.asi8)
            tgt_values = target.asi8
        else:
            tgt_values = target._values

        indexer, missing = self._engine.get_indexer_non_unique(tgt_values)
        return _ensure_platform_int(indexer), missing
