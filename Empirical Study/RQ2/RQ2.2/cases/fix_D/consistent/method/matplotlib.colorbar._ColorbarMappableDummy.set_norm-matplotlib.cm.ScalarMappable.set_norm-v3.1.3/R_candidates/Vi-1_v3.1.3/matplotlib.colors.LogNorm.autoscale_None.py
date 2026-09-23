    def autoscale_None(self, A):
        # docstring inherited.
        super().autoscale_None(np.ma.masked_less_equal(A, 0, copy=False))
