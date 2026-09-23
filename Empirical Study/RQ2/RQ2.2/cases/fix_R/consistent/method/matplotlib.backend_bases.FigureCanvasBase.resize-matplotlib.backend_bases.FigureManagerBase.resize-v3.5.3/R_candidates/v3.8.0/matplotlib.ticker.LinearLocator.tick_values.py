    def tick_values(self, vmin, vmax):
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=0.05)

        if (vmin, vmax) in self.presets:
            return self.presets[(vmin, vmax)]

        if self.numticks == 0:
            return []
        ticklocs = np.linspace(vmin, vmax, self.numticks)

        return self.raise_if_exceeds(ticklocs)
