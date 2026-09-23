    def _set_codes(
        self, codes, level=None, copy=False, validate=True, verify_integrity=False
    ):
        if validate and level is None and len(codes) != self.nlevels:
            raise ValueError("Length of codes must match number of levels")
        if validate and level is not None and len(codes) != len(level):
            raise ValueError("Length of codes must match length of levels.")

        if level is None:
            new_codes = FrozenList(
                _ensure_frozen(level_codes, lev, copy=copy)._shallow_copy()
                for lev, level_codes in zip(self.levels, codes)
            )
        else:
            level = [self._get_level_number(l) for l in level]
            new_codes = list(self._codes)
            for lev_idx, level_codes in zip(level, codes):
                lev = self.levels[lev_idx]
                new_codes[lev_idx] = _ensure_frozen(
                    level_codes, lev, copy=copy
                )._shallow_copy()
            new_codes = FrozenList(new_codes)

        if verify_integrity:
            new_codes = self._verify_integrity(codes=new_codes)

        self._codes = new_codes

        self._tuples = None
        self._reset_cache()
