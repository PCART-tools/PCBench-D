    def autoscale(self, A):
        # docstring inherited.
        super().autoscale(np.ma.array(A, mask=(A <= 0)))
