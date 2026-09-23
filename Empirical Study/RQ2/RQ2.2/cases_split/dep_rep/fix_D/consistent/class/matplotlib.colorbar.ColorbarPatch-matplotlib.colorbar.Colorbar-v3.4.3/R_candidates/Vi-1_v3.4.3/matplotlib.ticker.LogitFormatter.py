class LogitFormatter(Formatter):
    """
    Probability formatter (using Math text).
    """

    def __init__(
        self,
        *,
        use_overline=False,
        one_half=r"\frac{1}{2}",
        minor=False,
        minor_threshold=25,
        minor_number=6,
    ):
        r"""
        Parameters
        ----------
        use_overline : bool, default: False
            If x > 1/2, with x = 1-v, indicate if x should be displayed as
            $\overline{v}$. The default is to display $1-v$.

        one_half : str, default: r"\frac{1}{2}"
            The string used to represent 1/2.

        minor : bool, default: False
            Indicate if the formatter is formatting minor ticks or not.
            Basically minor ticks are not labelled, except when only few ticks
            are provided, ticks with most space with neighbor ticks are
            labelled. See other parameters to change the default behavior.

        minor_threshold : int, default: 25
            Maximum number of locs for labelling some minor ticks. This
            parameter have no effect if minor is False.

        minor_number : int, default: 6
            Number of ticks which are labelled when the number of ticks is
            below the threshold.
        """
        self._use_overline = use_overline
        self._one_half = one_half
        self._minor = minor
        self._labelled = set()
        self._minor_threshold = minor_threshold
        self._minor_number = minor_number

    def use_overline(self, use_overline):
        r"""
        Switch display mode with overline for labelling p>1/2.

        Parameters
        ----------
        use_overline : bool, default: False
            If x > 1/2, with x = 1-v, indicate if x should be displayed as
            $\overline{v}$. The default is to display $1-v$.
        """
        self._use_overline = use_overline

    def set_one_half(self, one_half):
        r"""
        Set the way one half is displayed.

        one_half : str, default: r"\frac{1}{2}"
            The string used to represent 1/2.
        """
        self._one_half = one_half

    def set_minor_threshold(self, minor_threshold):
        """
        Set the threshold for labelling minors ticks.

        Parameters
        ----------
        minor_threshold : int
            Maximum number of locations for labelling some minor ticks. This
            parameter have no effect if minor is False.
        """
        self._minor_threshold = minor_threshold

    def set_minor_number(self, minor_number):
        """
        Set the number of minor ticks to label when some minor ticks are
        labelled.

        Parameters
        ----------
        minor_number : int
            Number of ticks which are labelled when the number of ticks is
            below the threshold.
        """
        self._minor_number = minor_number

    def set_locs(self, locs):
        self.locs = np.array(locs)
        self._labelled.clear()

        if not self._minor:
            return None
        if all(
            is_decade(x, rtol=1e-7)
            or is_decade(1 - x, rtol=1e-7)
            or (is_close_to_int(2 * x) and int(np.round(2 * x)) == 1)
            for x in locs
        ):
            # minor ticks are subsample from ideal, so no label
            return None
        if len(locs) < self._minor_threshold:
            if len(locs) < self._minor_number:
                self._labelled.update(locs)
            else:
                # we do not have a lot of minor ticks, so only few decades are
                # displayed, then we choose some (spaced) minor ticks to label.
                # Only minor ticks are known, we assume it is sufficient to
                # choice which ticks are displayed.
                # For each ticks we compute the distance between the ticks and
                # the previous, and between the ticks and the next one. Ticks
                # with smallest minimum are chosen. As tiebreak, the ticks
                # with smallest sum is chosen.
                diff = np.diff(-np.log(1 / self.locs - 1))
                space_pessimistic = np.minimum(
                    np.concatenate(((np.inf,), diff)),
                    np.concatenate((diff, (np.inf,))),
                )
                space_sum = (
                    np.concatenate(((0,), diff))
                    + np.concatenate((diff, (0,)))
                )
                good_minor = sorted(
                    range(len(self.locs)),
                    key=lambda i: (space_pessimistic[i], space_sum[i]),
                )[-self._minor_number:]
                self._labelled.update(locs[i] for i in good_minor)

    def _format_value(self, x, locs, sci_notation=True):
        if sci_notation:
            exponent = math.floor(np.log10(x))
            min_precision = 0
        else:
            exponent = 0
            min_precision = 1
        value = x * 10 ** (-exponent)
        if len(locs) < 2:
            precision = min_precision
        else:
            diff = np.sort(np.abs(locs - x))[1]
            precision = -np.log10(diff) + exponent
            precision = (
                int(np.round(precision))
                if is_close_to_int(precision)
                else math.ceil(precision)
            )
            if precision < min_precision:
                precision = min_precision
        mantissa = r"%.*f" % (precision, value)
        if not sci_notation:
            return mantissa
        s = r"%s\cdot10^{%d}" % (mantissa, exponent)
        return s

    def _one_minus(self, s):
        if self._use_overline:
            return r"\overline{%s}" % s
        else:
            return "1-{}".format(s)

    def __call__(self, x, pos=None):
        if self._minor and x not in self._labelled:
            return ""
        if x <= 0 or x >= 1:
            return ""
        if is_close_to_int(2 * x) and round(2 * x) == 1:
            s = self._one_half
        elif x < 0.5 and is_decade(x, rtol=1e-7):
            exponent = round(np.log10(x))
            s = "10^{%d}" % exponent
        elif x > 0.5 and is_decade(1 - x, rtol=1e-7):
            exponent = round(np.log10(1 - x))
            s = self._one_minus("10^{%d}" % exponent)
        elif x < 0.1:
            s = self._format_value(x, self.locs)
        elif x > 0.9:
            s = self._one_minus(self._format_value(1-x, 1-self.locs))
        else:
            s = self._format_value(x, self.locs, sci_notation=False)
        return r"$\mathdefault{%s}$" % s

    def format_data_short(self, value):
        # docstring inherited
        # Thresholds chosen to use scientific notation iff exponent <= -2.
        if value < 0.1:
            return "{:e}".format(value)
        if value < 0.9:
            return "{:f}".format(value)
        return "1-{:e}".format(1 - value)
