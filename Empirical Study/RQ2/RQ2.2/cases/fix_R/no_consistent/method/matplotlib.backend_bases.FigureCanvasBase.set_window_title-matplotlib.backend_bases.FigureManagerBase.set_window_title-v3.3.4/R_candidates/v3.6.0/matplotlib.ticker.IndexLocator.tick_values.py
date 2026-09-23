    def tick_values(self, vmin, vmax):
        return self.raise_if_exceeds(
            np.arange(vmin + self.offset, vmax + 1, self._base))
