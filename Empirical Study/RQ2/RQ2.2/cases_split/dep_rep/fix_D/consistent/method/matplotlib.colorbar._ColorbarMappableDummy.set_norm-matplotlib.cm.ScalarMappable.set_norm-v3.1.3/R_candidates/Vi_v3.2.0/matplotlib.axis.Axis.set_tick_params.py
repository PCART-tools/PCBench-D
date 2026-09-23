    def set_tick_params(self, which='major', reset=False, **kw):
        """
        Set appearance parameters for ticks, ticklabels, and gridlines.

        For documentation of keyword arguments, see
        :meth:`matplotlib.axes.Axes.tick_params`.
        """
        dicts = []
        if which == 'major' or which == 'both':
            dicts.append(self._major_tick_kw)
        if which == 'minor' or which == 'both':
            dicts.append(self._minor_tick_kw)
        kwtrans = self._translate_tick_kw(kw)

        # this stashes the parameter changes so any new ticks will
        # automatically get them
        for d in dicts:
            if reset:
                d.clear()
            d.update(kwtrans)

        if reset:
            self.reset_ticks()
        else:
            # apply the new kwargs to the existing ticks
            if which == 'major' or which == 'both':
                for tick in self.majorTicks:
                    tick._apply_params(**kwtrans)
            if which == 'minor' or which == 'both':
                for tick in self.minorTicks:
                    tick._apply_params(**kwtrans)
            # special-case label color to also apply to the offset
            # text
            if 'labelcolor' in kwtrans:
                self.offsetText.set_color(kwtrans['labelcolor'])

        self.stale = True
