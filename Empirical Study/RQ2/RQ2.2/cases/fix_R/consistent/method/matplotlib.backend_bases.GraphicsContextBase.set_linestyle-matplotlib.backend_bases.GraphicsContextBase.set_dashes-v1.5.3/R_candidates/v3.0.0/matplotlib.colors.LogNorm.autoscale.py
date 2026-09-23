    def autoscale(self, A):
        """
        Set *vmin*, *vmax* to min, max of *A*.
        """
        A = np.ma.masked_less_equal(A, 0, copy=False)
        self.vmin = np.ma.min(A)
        self.vmax = np.ma.max(A)
