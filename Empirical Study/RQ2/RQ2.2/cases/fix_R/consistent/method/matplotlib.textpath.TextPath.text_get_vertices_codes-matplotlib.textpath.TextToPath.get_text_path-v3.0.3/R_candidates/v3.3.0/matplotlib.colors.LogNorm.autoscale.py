    def autoscale(self, A):
        # docstring inherited.
        super().autoscale(np.ma.masked_less_equal(A, 0, copy=False))
