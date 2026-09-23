    def _set_labels(self, labels, copy=False, validate=True,
                    verify_integrity=False):
        if validate and len(labels) != self.nlevels:
            raise ValueError("Length of labels must match length of levels")
        self._labels = FrozenList(
            _ensure_frozen(labs, copy=copy)._shallow_copy() for labs in labels)
        self._tuples = None
        self._reset_cache()

        if verify_integrity:
            self._verify_integrity()
