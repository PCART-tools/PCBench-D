    def _make_verts_for_region(self, t, f1, f2, idx0, idx1):
        """
        Make ``verts`` for a contiguous region between ``idx0`` and ``idx1``, taking
        into account ``step`` and ``interpolate``.
        """
        t_slice = t[idx0:idx1]
        f1_slice = f1[idx0:idx1]
        f2_slice = f2[idx0:idx1]
        if self._step is not None:
            step_func = cbook.STEP_LOOKUP_MAP["steps-" + self._step]
            t_slice, f1_slice, f2_slice = step_func(t_slice, f1_slice, f2_slice)

        if self._interpolate:
            start = self._get_interpolating_points(t, f1, f2, idx0)
            end = self._get_interpolating_points(t, f1, f2, idx1)
        else:
            # Handle scalar f2 (e.g. 0): the fill should go all
            # the way down to 0 even if none of the dep1 sample points do.
            start = t_slice[0], f2_slice[0]
            end = t_slice[-1], f2_slice[-1]

        pts = np.concatenate((
            np.asarray([start]),
            np.stack((t_slice, f1_slice), axis=-1),
            np.asarray([end]),
            np.stack((t_slice, f2_slice), axis=-1)[::-1]))

        return self._fix_pts_xy_order(pts)
