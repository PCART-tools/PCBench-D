    def autoscale_None(self, A):
        """If vmin or vmax are not set, use the min/max of *A* to set them."""
        A = np.asanyarray(A)
        if self.vmin is None and A.size:
            self.vmin = A.min()
        if self.vmax is None and A.size:
            self.vmax = A.max()
