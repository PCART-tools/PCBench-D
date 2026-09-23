    def autoscale(self, A):
        """
        Set *vmin*, *vmax* to min, max of *A*.
        """
        A = np.asanyarray(A)
        self.vmin = A.min()
        self.vmax = A.max()
