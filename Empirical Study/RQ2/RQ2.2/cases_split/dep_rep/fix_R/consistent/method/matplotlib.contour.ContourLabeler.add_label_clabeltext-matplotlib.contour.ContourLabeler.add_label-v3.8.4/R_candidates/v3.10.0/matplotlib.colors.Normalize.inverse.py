    def inverse(self, value):
        """
        Maps the normalized value (i.e., index in the colormap) back to image
        data value.

        Parameters
        ----------
        value
            Normalized value.
        """
        if not self.scaled():
            raise ValueError("Not invertible until both vmin and vmax are set")
        (vmin,), _ = self.process_value(self.vmin)
        (vmax,), _ = self.process_value(self.vmax)

        if np.iterable(value):
            val = np.ma.asarray(value)
            return vmin + val * (vmax - vmin)
        else:
            return vmin + value * (vmax - vmin)
