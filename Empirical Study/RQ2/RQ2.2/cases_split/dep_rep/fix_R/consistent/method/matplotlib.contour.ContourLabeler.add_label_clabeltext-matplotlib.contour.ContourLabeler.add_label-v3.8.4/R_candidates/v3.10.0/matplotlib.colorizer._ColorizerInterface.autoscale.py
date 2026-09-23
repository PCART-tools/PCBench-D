    def autoscale(self):
        """
        Autoscale the scalar limits on the norm instance using the
        current array
        """
        self._colorizer.autoscale(self._A)
