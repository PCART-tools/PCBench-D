    def autoscale_None(self, A):
        """If vmin or vmax are not set, use the min/max of *A* to set them."""
        A = np.asanyarray(A)

        if isinstance(A, np.ma.MaskedArray):
            # we need to make the distinction between an array, False, np.bool_(False)
            if A.mask is False or not A.mask.shape:
                A = A.data

        if self.vmin is None and A.size:
            self.vmin = A.min()
        if self.vmax is None and A.size:
            self.vmax = A.max()
