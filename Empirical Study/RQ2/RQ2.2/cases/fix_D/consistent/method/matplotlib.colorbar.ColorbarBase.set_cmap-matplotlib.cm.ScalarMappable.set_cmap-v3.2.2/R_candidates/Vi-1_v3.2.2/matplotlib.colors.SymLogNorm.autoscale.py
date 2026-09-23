    def autoscale(self, A):
        # docstring inherited.
        super().autoscale(A)
        self._transform_vmin_vmax()
