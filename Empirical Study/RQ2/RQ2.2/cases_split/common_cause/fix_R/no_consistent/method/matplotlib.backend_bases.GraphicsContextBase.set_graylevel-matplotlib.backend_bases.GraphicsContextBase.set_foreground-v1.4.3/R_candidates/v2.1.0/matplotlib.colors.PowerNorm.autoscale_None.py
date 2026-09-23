    def autoscale_None(self, A):
        """autoscale only None-valued vmin or vmax."""
        A = np.asanyarray(A)
        if self.vmin is None and A.size:
            self.vmin = A.min()
            if self.vmin < 0:
                self.vmin = 0
                warnings.warn("Power-law scaling on negative values is "
                              "ill-defined, clamping to 0.")
        if self.vmax is None and A.size:
            self.vmax = A.max()
