    def autoscale(self, A):
        """
        Set *vmin*, *vmax* to min, max of *A*.
        """
        self.vmin = np.ma.min(A)
        if self.vmin < 0:
            self.vmin = 0
            warnings.warn("Power-law scaling on negative values is "
                          "ill-defined, clamping to 0.")
        self.vmax = np.ma.max(A)
