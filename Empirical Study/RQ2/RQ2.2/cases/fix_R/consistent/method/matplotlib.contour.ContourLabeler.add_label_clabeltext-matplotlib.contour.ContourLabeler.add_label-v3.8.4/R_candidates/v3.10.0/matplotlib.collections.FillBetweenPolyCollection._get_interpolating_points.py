    @classmethod
    def _get_interpolating_points(cls, t, f1, f2, idx):
        """Calculate interpolating points."""
        im1 = max(idx - 1, 0)
        t_values = t[im1:idx+1]
        diff_values = f1[im1:idx+1] - f2[im1:idx+1]
        f1_values = f1[im1:idx+1]

        if len(diff_values) == 2:
            if np.ma.is_masked(diff_values[1]):
                return t[im1], f1[im1]
            elif np.ma.is_masked(diff_values[0]):
                return t[idx], f1[idx]

        diff_root_t = cls._get_diff_root(0, diff_values, t_values)
        diff_root_f = cls._get_diff_root(diff_root_t, t_values, f1_values)
        return diff_root_t, diff_root_f
