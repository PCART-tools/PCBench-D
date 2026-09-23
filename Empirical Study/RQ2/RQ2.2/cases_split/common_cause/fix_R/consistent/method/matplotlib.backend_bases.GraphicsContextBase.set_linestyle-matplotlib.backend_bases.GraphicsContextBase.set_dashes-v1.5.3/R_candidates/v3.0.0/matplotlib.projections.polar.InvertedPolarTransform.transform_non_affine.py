    def transform_non_affine(self, xy):
        x = xy[:, 0:1]
        y = xy[:, 1:]
        r = np.sqrt(x*x + y*y)
        with np.errstate(invalid='ignore'):
            # At x=y=r=0 this will raise an
            # invalid value warning when doing 0/0
            # Divide by zero warnings are only raised when
            # the numerator is different from 0. That
            # should not happen here.
            theta = np.arccos(x / r)
        theta = np.where(y < 0, 2 * np.pi - theta, theta)

        # PolarAxes does not use the theta transforms here, but apply them for
        # backwards-compatibility if not being used by it.
        if self._apply_theta_transforms and self._axis is not None:
            theta -= self._axis.get_theta_offset()
            theta *= self._axis.get_theta_direction()
            theta %= 2 * np.pi

        if self._use_rmin and self._axis is not None:
            r += self._axis.get_rorigin()

        return np.concatenate((theta, r), 1)
