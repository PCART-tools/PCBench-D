    def view_limits(self, dmin, dmax):
        """
        Set the view limits to the nearest multiples of base that
        contain the data.
        """
        if mpl.rcParams['axes.autolimit_mode'] == 'round_numbers':
            vmin = self._edge.le(dmin) * self._edge.step
            vmax = self._edge.ge(dmax) * self._edge.step
            if vmin == vmax:
                vmin -= 1
                vmax += 1
        else:
            vmin = dmin
            vmax = dmax

        return mtransforms.nonsingular(vmin, vmax)
