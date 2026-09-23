    def inverted(self):
        return PolarAxes.PolarTransform(self._axis, self._use_rmin,
                                        self._apply_theta_transforms)
