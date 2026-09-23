    def transform_non_affine(self, tr):
        xy = np.empty(tr.shape, float)

        t = tr[:, 0:1]
        r = tr[:, 1:2]
        x = xy[:, 0:1]
        y = xy[:, 1:2]

        # PolarAxes does not use the theta transforms here, but apply them for
        # backwards-compatibility if not being used by it.
        if self._apply_theta_transforms and self._axis is not None:
            t *= self._axis.get_theta_direction()
            t += self._axis.get_theta_offset()

        if self._use_rmin and self._axis is not None:
            r = r - self._axis.get_rorigin()
        mask = r < 0
        x[:] = np.where(mask, np.nan, r * np.cos(t))
        y[:] = np.where(mask, np.nan, r * np.sin(t))

        return xy
