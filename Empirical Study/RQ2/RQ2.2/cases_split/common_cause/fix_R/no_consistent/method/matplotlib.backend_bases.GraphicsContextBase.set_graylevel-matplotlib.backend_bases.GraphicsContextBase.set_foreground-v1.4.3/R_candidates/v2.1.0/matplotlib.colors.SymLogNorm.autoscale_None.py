    def autoscale_None(self, A):
        """autoscale only None-valued vmin or vmax."""
        if self.vmin is not None and self.vmax is not None:
            pass
        A = np.asanyarray(A)
        if self.vmin is None and A.size:
            self.vmin = A.min()
        if self.vmax is None and A.size:
            self.vmax = A.max()
        self._transform_vmin_vmax()
