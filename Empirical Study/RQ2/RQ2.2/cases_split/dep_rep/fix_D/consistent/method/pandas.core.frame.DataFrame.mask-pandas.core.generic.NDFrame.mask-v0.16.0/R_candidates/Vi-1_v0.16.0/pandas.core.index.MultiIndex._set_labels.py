    def _set_labels(self, labels, level=None, copy=False, validate=True,
                    verify_integrity=False):

        if validate and level is None and len(labels) != self.nlevels:
            raise ValueError("Length of labels must match number of levels")
        if validate and level is not None and len(labels) != len(level):
            raise ValueError('Length of labels must match length of levels.')

        if level is None:
            new_labels = FrozenList(_ensure_frozen(lab, lev, copy=copy)._shallow_copy()
                                    for lev, lab in zip(self.levels, labels))
        else:
            level = [self._get_level_number(l) for l in level]
            new_labels = list(self._labels)
            for l, lev, lab in zip(level, self.levels, labels):
                new_labels[l] = _ensure_frozen(lab, lev, copy=copy)._shallow_copy()
            new_labels = FrozenList(new_labels)

        self._labels = new_labels
        self._tuples = None
        self._reset_cache()

        if verify_integrity:
            self._verify_integrity()
