    def _verify_integrity(self, codes=None, levels=None):
        """

        Parameters
        ----------
        codes : optional list
            Codes to check for validity. Defaults to current codes.
        levels : optional list
            Levels to check for validity. Defaults to current levels.

        Raises
        ------
        ValueError
            If length of levels and codes don't match, if the codes for any
            level would exceed level bounds, or there are any duplicate levels.

        Returns
        -------
        codes : new codes where code value = -1 if it corresponds to a
        NaN level.
        """
        # NOTE: Currently does not check, among other things, that cached
        # nlevels matches nor that sortorder matches actually sortorder.
        codes = codes or self.codes
        levels = levels or self.levels

        if len(levels) != len(codes):
            raise ValueError(
                "Length of levels and codes must match. NOTE:"
                " this index is in an inconsistent state."
            )
        codes_length = len(codes[0])
        for i, (level, level_codes) in enumerate(zip(levels, codes)):
            if len(level_codes) != codes_length:
                raise ValueError(
                    "Unequal code lengths: %s" % ([len(code_) for code_ in codes])
                )
            if len(level_codes) and level_codes.max() >= len(level):
                msg = (
                    "On level {level}, code max ({max_code}) >= length of "
                    "level ({level_len}). NOTE: this index is in an "
                    "inconsistent state".format(
                        level=i, max_code=level_codes.max(), level_len=len(level)
                    )
                )
                raise ValueError(msg)
            if len(level_codes) and level_codes.min() < -1:
                raise ValueError(
                    "On level {level}, code value ({code})"
                    " < -1".format(level=i, code=level_codes.min())
                )
            if not level.is_unique:
                raise ValueError(
                    "Level values must be unique: {values} on "
                    "level {level}".format(values=[value for value in level], level=i)
                )

        codes = [
            self._validate_codes(level, code) for level, code in zip(levels, codes)
        ]
        new_codes = FrozenList(codes)
        return new_codes
