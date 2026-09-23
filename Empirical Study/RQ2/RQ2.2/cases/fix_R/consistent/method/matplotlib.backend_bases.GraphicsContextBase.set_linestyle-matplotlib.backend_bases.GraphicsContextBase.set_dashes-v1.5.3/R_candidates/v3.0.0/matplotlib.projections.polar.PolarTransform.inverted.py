    def inverted(self):
        return PolarAxes.InvertedPolarTransform(self._axis, self._use_rmin,
                                                self._apply_theta_transforms)
