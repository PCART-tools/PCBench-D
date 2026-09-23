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
        """
        # NOTE: Currently does not check, among other things, that cached
        # nlevels matches nor that sortorder matches actually sortorder.
        codes = codes or self.codes
        levels = levels or self.levels

        if len(levels) != len(codes):
            raise ValueError("Length of levels and codes must match. NOTE:"
                             " this index is in an inconsistent state.")
        codes_length = len(self.codes[0])
        for i, (level, level_codes) in enumerate(zip(levels, codes)):
            if len(level_codes) != codes_length:
                raise ValueError("Unequal code lengths: %s" %
                                 ([len(code_) for code_ in codes]))
            if len(level_codes) and level_codes.max() >= len(level):
                raise ValueError("On level %d, code max (%d) >= length of"
                                 " level  (%d). NOTE: this index is in an"
                                 " inconsistent state" % (i, level_codes.max(),
                                                          len(level)))
            if not level.is_unique:
                raise ValueError("Level values must be unique: {values} on "
                                 "level {level}".format(
                                     values=[value for value in level],
                                     level=i))
