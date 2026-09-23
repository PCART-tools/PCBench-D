    def inverted(self):
        # docstring inherited
        return PolarAxes.InvertedPolarTransform(
            self._axis, self._use_rmin,
            apply_theta_transforms=self._apply_theta_transforms
        )
