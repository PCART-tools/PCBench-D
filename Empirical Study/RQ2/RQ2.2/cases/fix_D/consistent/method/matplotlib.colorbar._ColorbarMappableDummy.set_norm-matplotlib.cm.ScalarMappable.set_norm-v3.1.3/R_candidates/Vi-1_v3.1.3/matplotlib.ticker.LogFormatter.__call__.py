    def __call__(self, x, pos=None):
        """
        Return the format for tick val *x*.
        """
        if x == 0.0:  # Symlog
            return '0'

        x = abs(x)
        b = self._base
        # only label the decades
        fx = math.log(x) / math.log(b)
        is_x_decade = is_close_to_int(fx)
        exponent = np.round(fx) if is_x_decade else np.floor(fx)
        coeff = np.round(x / b ** exponent)

        if self.labelOnlyBase and not is_x_decade:
            return ''
        if self._sublabels is not None and coeff not in self._sublabels:
            return ''

        vmin, vmax = self.axis.get_view_interval()
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)
        s = self._num_to_string(x, vmin, vmax)
        return self.fix_minus(s)
