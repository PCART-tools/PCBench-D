    def format_data(self, value):
        """
        Format a number in engineering notation, appending a letter
        representing the power of 1000 of the original number.
        Some examples:

        >>> format_data(0)        # for self.places = 0
        '0'

        >>> format_data(1000000)  # for self.places = 1
        '1.0 M'

        >>> format_data(-1e-6)  # for self.places = 2
        '-1.00 \N{MICRO SIGN}'
        """
        sign = 1
        fmt = "g" if self.places is None else f".{self.places:d}f"

        if value < 0:
            sign = -1
            value = -value

        if value != 0:
            pow10 = int(math.floor(math.log10(value) / 3) * 3)
        else:
            pow10 = 0
            # Force value to zero, to avoid inconsistencies like
            # format_eng(-0) = "0" and format_eng(0.0) = "0"
            # but format_eng(-0.0) = "-0.0"
            value = 0.0

        pow10 = np.clip(pow10, min(self.ENG_PREFIXES), max(self.ENG_PREFIXES))

        mant = sign * value / (10.0 ** pow10)
        # Taking care of the cases like 999.9..., which may be rounded to 1000
        # instead of 1 k.  Beware of the corner case of values that are beyond
        # the range of SI prefixes (i.e. > 'Y').
        if (abs(float(format(mant, fmt))) >= 1000
                and pow10 < max(self.ENG_PREFIXES)):
            mant /= 1000
            pow10 += 3

        unit_prefix = self.ENG_PREFIXES[int(pow10)]
        if self.unit or unit_prefix:
            suffix = f"{self.sep}{unit_prefix}{self.unit}"
        else:
            suffix = ""
        if self._usetex or self._useMathText:
            return f"${mant:{fmt}}${suffix}"
        else:
            return f"{mant:{fmt}}{suffix}"
