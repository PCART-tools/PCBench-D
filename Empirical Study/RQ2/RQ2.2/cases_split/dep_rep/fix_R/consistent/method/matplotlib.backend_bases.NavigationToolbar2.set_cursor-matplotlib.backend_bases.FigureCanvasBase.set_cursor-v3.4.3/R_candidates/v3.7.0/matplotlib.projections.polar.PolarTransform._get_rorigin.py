    def _get_rorigin(self):
        # Get lower r limit after being scaled by the radial scale transform
        return self._scale_transform.transform(
            (0, self._axis.get_rorigin()))[1]
