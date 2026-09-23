    def _verify_integrity(
        self,
        codes: list | None = None,
        levels: list | None = None,
        levels_to_verify: list[int] | range | None = None,
    ):
        """
        Parameters
        ----------
        codes : optional list
            Codes to check for validity. Defaults to current codes.
        levels : optional list
            Levels to check for validity. Defaults to current levels.
        levels_to_validate: optional list
            Specifies the levels to verify.

        Raises
        ------
        ValueError
            If length of levels and codes don't match, if the codes for any
            level would exceed level bounds, or there are any duplicate levels.

        Returns
        -------
        new codes where code value = -1 if it corresponds to a
        NaN level.
        """
        # NOTE: Currently does not check, among other things, that cached
        # nlevels matches nor that sortorder matches actually sortorder.
        codes = codes or self.codes
        levels = levels or self.levels
        if levels_to_verify is None:
            levels_to_verify = range(len(levels))

        if len(levels) != len(codes):
            raise ValueError(
                "Length of levels and codes must match. NOTE: "
                "this index is in an inconsistent state."
            )
        codes_length = len(codes[0])
        for i in levels_to_verify:
            level = levels[i]
            level_codes = codes[i]

            if len(level_codes) != codes_length:
                raise ValueError(
                    f"Unequal code lengths: {[len(code_) for code_ in codes]}"
                )
            if len(level_codes) and level_codes.max() >= len(level):
                raise ValueError(
                    f"On level {i}, code max ({level_codes.max()}) >= length of "
                    f"level ({len(level)}). NOTE: this index is in an "
                    "inconsistent state"
                )
            if len(level_codes) and level_codes.min() < -1:
                raise ValueError(f"On level {i}, code value ({level_codes.min()}) < -1")
            if not level.is_unique:
                raise ValueError(
                    f"Level values must be unique: {list(level)} on level {i}"
                )
        if self.sortorder is not None:
            if self.sortorder > _lexsort_depth(self.codes, self.nlevels):
                raise ValueError(
                    "Value for sortorder must be inferior or equal to actual "
                    f"lexsort_depth: sortorder {self.sortorder} "
                    f"with lexsort_depth {_lexsort_depth(self.codes, self.nlevels)}"
                )

        result_codes = []
        for i in range(len(levels)):
            if i in levels_to_verify:
                result_codes.append(self._validate_codes(levels[i], codes[i]))
            else:
                result_codes.append(codes[i])

        new_codes = FrozenList(result_codes)
        return new_codes
