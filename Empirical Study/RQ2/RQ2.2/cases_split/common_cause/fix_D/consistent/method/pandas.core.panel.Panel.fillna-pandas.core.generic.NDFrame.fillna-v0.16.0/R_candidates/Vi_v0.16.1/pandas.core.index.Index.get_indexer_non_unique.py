    def get_indexer_non_unique(self, target):
        """ return an indexer suitable for taking from a non unique index
            return the labels in the same order as the target, and
            return a missing indexer into the target (missing are marked as -1
            in the indexer); target must be an iterable """
        target = _ensure_index(target)
        pself, ptarget = self._possibly_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer_non_unique(ptarget)

        if self.is_all_dates:
            self = Index(self.asi8)
            tgt_values = target.asi8
        else:
            tgt_values = target.values

        indexer, missing = self._engine.get_indexer_non_unique(tgt_values)
        return Index(indexer), missing
