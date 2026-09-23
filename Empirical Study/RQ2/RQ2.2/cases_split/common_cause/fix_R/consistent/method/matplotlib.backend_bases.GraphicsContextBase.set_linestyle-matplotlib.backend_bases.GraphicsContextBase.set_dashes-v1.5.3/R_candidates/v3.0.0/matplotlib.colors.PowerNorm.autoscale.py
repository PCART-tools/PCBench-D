    def autoscale(self, A):
        """
        Set *vmin*, *vmax* to min, max of *A*.
        """
        self.vmin = np.ma.min(A)
        self.vmax = np.ma.max(A)
