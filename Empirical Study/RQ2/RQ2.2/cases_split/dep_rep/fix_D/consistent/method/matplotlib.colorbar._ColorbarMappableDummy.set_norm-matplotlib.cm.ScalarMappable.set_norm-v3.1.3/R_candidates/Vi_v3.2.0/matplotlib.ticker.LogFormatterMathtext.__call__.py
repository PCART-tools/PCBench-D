    def __call__(self, x, pos=None):
        """
        Return the format for tick value *x*.

        The position *pos* is ignored.
        """
        usetex = rcParams['text.usetex']
        min_exp = rcParams['axes.formatter.min_exponent']

        if x == 0:  # Symlog
            if usetex:
                return '$0$'
            else:
                return '$%s$' % _mathdefault('0')

        sign_string = '-' if x < 0 else ''
        x = abs(x)
        b = self._base

        # only label the decades
        fx = math.log(x) / math.log(b)
        is_x_decade = is_close_to_int(fx)
        exponent = round(fx) if is_x_decade else np.floor(fx)
        coeff = round(x / b ** exponent)
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

        if np.abs(fx) < min_exp:
            if usetex:
                return r'${0}{1:g}$'.format(sign_string, x)
            else:
                return '${0}$'.format(_mathdefault(
                    '{0}{1:g}'.format(sign_string, x)))
        elif not is_x_decade:
            return self._non_decade_format(sign_string, base, fx, usetex)
        elif usetex:
            return r'$%s%s^{%d}$' % (sign_string, base, fx)
        else:
            return '$%s$' % _mathdefault('%s%s^{%d}' % (sign_string, base, fx))
