    def _transform_vmin_vmax(self):
        """Calculate vmin and vmax in the transformed system."""
        vmin, vmax = self.vmin, self.vmax
        arr = np.array([vmax, vmin]).astype(float)
        self._upper, self._lower = self._transform(arr)
