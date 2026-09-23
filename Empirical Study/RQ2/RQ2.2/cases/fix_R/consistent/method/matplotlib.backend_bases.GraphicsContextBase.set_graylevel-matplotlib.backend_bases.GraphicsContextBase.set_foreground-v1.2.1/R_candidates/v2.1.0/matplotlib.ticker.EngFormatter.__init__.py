    def __init__(self, unit="", places=None, sep=" "):
        """
        Parameters
        ----------
        unit : str (default: "")
            Unit symbol to use, suitable for use with single-letter
            representations of powers of 1000. For example, 'Hz' or 'm'.

        places : int (default: None)
            Precision with which to display the number, specified in
            digits after the decimal point (there will be between one
            and three digits before the decimal point). If it is None,
            the formatting falls back to the floating point format '%g',
            which displays up to 6 *significant* digits, i.e. the equivalent
            value for *places* varies between 0 and 5 (inclusive).

        sep : str (default: " ")
            Separator used between the value and the prefix/unit. For
            example, one get '3.14 mV' if ``sep`` is " " (default) and
            '3.14mV' if ``sep`` is "". Besides the default behavior, some
            other useful options may be:

            * ``sep=""`` to append directly the prefix/unit to the value;
            * ``sep="\\N{THIN SPACE}"`` (``U+2009``);
            * ``sep="\\N{NARROW NO-BREAK SPACE}"`` (``U+202F``);
            * ``sep="\\N{NO-BREAK SPACE}"`` (``U+00A0``).
        """
        self.unit = unit
        self.places = places
        self.sep = sep
