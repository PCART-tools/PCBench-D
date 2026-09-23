    def view_limits(self, dmin, dmax):
        """
        Set the view limits to the nearest multiples of base that
        contain the data
        """
        if rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = self._base.le(dmin)
            vmax = self._base.ge(dmax)
            if vmin == vmax:
                vmin -= 1
                vmax += 1
        else:
            vmin = dmin
            vmax = dmax

        return mtransforms.nonsingular(vmin, vmax)
