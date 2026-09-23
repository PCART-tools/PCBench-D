    def _set_levels(
        self, levels, level=None, copy=False, validate=True, verify_integrity=False
    ):
        # This is NOT part of the levels property because it should be
        # externally not allowed to set levels. User beware if you change
        # _levels directly
        if validate and len(levels) == 0:
            raise ValueError("Must set non-zero number of levels.")
        if validate and level is None and len(levels) != self.nlevels:
            raise ValueError("Length of levels must match number of levels.")
        if validate and level is not None and len(levels) != len(level):
            raise ValueError("Length of levels must match length of level.")

        if level is None:
            new_levels = FrozenList(
                ensure_index(lev, copy=copy)._shallow_copy() for lev in levels
            )
        else:
            level = [self._get_level_number(l) for l in level]
            new_levels = list(self._levels)
            for l, v in zip(level, levels):
                new_levels[l] = ensure_index(v, copy=copy)._shallow_copy()
            new_levels = FrozenList(new_levels)

        if verify_integrity:
            new_codes = self._verify_integrity(levels=new_levels)
            self._codes = new_codes

        names = self.names
        self._levels = new_levels
        if any(names):
            self._set_names(names)

        self._tuples = None
        self._reset_cache()
