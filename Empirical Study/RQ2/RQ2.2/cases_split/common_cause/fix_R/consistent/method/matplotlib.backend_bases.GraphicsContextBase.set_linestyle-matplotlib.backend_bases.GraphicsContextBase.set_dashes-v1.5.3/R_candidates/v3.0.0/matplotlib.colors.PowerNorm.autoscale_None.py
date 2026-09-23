    def autoscale_None(self, A):
        """autoscale only None-valued vmin or vmax."""
        A = np.asanyarray(A)
        if self.vmin is None and A.size:
            self.vmin = A.min()
        if self.vmax is None and A.size:
            self.vmax = A.max()
