class LogFormatterMathtext(LogFormatter):
    """
    Format values for log axis using ``exponent = log_base(value)``.
    """

    def _non_decade_format(self, sign_string, base, fx, usetex):
        """Return string for non-decade locations."""
        return r'$\mathdefault{%s%s^{%.2f}}$' % (sign_string, base, fx)

    def __call__(self, x, pos=None):
        # docstring inherited
        usetex = mpl.rcParams['text.usetex']
        min_exp = mpl.rcParams['axes.formatter.min_exponent']

        if x == 0:  # Symlog
            return r'$\mathdefault{0}$'

        sign_string = '-' if x < 0 else ''
        x = abs(x)
        b = self._base

        # only label the decades
        fx = math.log(x) / math.log(b)
        is_x_decade = _is_close_to_int(fx)
        exponent = round(fx) if is_x_decade else np.floor(fx)
        coeff = round(b ** (fx - exponent))
        if is_x_decade:
            fx = round(fx)

        if self.labelOnlyBase and not is_x_decade:
            return ''
        if self._sublabels is not None and coeff not in self._sublabels:
            return ''

        # use string formatting of the base if it is not an integer
        if b % 1 == 0.0:
            base = '%d' % b
        else:
            base = '%s' % b

        if abs(fx) < min_exp:
            return r'$\mathdefault{%s%g}$' % (sign_string, x)
        elif not is_x_decade:
            return self._non_decade_format(sign_string, base, fx, usetex)
        else:
            return r'$\mathdefault{%s%s^{%d}}$' % (sign_string, base, fx)
