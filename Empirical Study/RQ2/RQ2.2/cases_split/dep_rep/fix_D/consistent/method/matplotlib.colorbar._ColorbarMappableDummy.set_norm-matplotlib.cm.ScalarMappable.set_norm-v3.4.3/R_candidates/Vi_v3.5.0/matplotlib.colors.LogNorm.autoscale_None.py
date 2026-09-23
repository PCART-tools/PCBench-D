    def autoscale_None(self, A):
        # docstring inherited.
        super().autoscale_None(np.ma.array(A, mask=(A <= 0)))
