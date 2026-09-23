    def view_limits(self, dmin, dmax):
        if self._symmetric:
            dmax = max(abs(dmin), abs(dmax))
            dmin = -dmax

        dmin, dmax = mtransforms.nonsingular(
            dmin, dmax, expander=1e-12, tiny=1e-13)

        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            return self._raw_ticks(dmin, dmax)[[0, -1]]
        else:
            return dmin, dmax
