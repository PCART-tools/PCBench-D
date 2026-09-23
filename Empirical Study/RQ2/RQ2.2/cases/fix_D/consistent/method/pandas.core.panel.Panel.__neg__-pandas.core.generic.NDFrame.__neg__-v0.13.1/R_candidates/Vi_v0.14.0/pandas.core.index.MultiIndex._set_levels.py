    def _set_levels(self, levels, copy=False, validate=True,
                    verify_integrity=False):
        # This is NOT part of the levels property because it should be
        # externally not allowed to set levels. User beware if you change
        # _levels directly
        if validate and len(levels) == 0:
            raise ValueError('Must set non-zero number of levels.')
        if validate and len(levels) != len(self._labels):
            raise ValueError('Length of levels must match length of labels.')
        levels = FrozenList(_ensure_index(lev, copy=copy)._shallow_copy()
                            for lev in levels)
        names = self.names
        self._levels = levels
        if any(names):
            self._set_names(names)

        self._tuples = None
        self._reset_cache()

        if verify_integrity:
            self._verify_integrity()
