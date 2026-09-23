    def format_eng(self, num):
        """
        Formats a number in engineering notation, appending a letter
        representing the power of 1000 of the original number.
        Some examples:

        >>> format_eng(0)       # for self.places = 0
        '0'

        >>> format_eng(1000000) # for self.places = 1
        '1.0 M'

        >>> format_eng("-1e-6") # for self.places = 2
        u'-1.00 \N{GREEK SMALL LETTER MU}'

        `num` may be a numeric value or a string that can be converted
        to a numeric value with ``float(num)``.
        """
        if isinstance(num, six.string_types):
            warnings.warn(
                "Passing a string as *num* argument is deprecated since"
                "Matplotlib 2.1, and is expected to be removed in 2.3.",
                mplDeprecation)

        dnum = float(num)
        sign = 1
        fmt = "g" if self.places is None else ".{:d}f".format(self.places)

        if dnum < 0:
            sign = -1
            dnum = -dnum

        if dnum != 0:
            pow10 = int(math.floor(math.log10(dnum) / 3) * 3)
        else:
            pow10 = 0
            # Force dnum to zero, to avoid inconsistencies like
            # format_eng(-0) = "0" and format_eng(0.0) = "0"
            # but format_eng(-0.0) = "-0.0"
            dnum = 0.0

        pow10 = np.clip(pow10, min(self.ENG_PREFIXES), max(self.ENG_PREFIXES))

        mant = sign * dnum / (10.0 ** pow10)
        # Taking care of the cases like 999.9..., which
        # may be rounded to 1000 instead of 1 k.  Beware
        # of the corner case of values that are beyond
        # the range of SI prefixes (i.e. > 'Y').
        _fmant = float("{mant:{fmt}}".format(mant=mant, fmt=fmt))
        if _fmant >= 1000 and pow10 != max(self.ENG_PREFIXES):
            mant /= 1000
            pow10 += 3

        prefix = self.ENG_PREFIXES[int(pow10)]

        formatted = "{mant:{fmt}}{sep}{prefix}".format(
            mant=mant, sep=self.sep, prefix=prefix, fmt=fmt)

        return formatted
