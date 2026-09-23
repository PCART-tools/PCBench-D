    def _set_codes(
        self,
        codes,
        *,
        level=None,
        copy: bool = False,
        validate: bool = True,
        verify_integrity: bool = False,
    ) -> None:
        if validate:
            if level is None and len(codes) != self.nlevels:
                raise ValueError("Length of codes must match number of levels")
            if level is not None and len(codes) != len(level):
                raise ValueError("Length of codes must match length of levels.")

        if level is None:
            new_codes = FrozenList(
                _coerce_indexer_frozen(level_codes, lev, copy=copy).view()
                for lev, level_codes in zip(self._levels, codes)
            )
        else:
            level_numbers = [self._get_level_number(lev) for lev in level]
            new_codes_list = list(self._codes)
            for lev_num, level_codes in zip(level_numbers, codes):
                lev = self.levels[lev_num]
                new_codes_list[lev_num] = _coerce_indexer_frozen(
                    level_codes, lev, copy=copy
                )
            new_codes = FrozenList(new_codes_list)

        if verify_integrity:
            new_codes = self._verify_integrity(codes=new_codes)

        self._codes = new_codes

        self._reset_cache()
