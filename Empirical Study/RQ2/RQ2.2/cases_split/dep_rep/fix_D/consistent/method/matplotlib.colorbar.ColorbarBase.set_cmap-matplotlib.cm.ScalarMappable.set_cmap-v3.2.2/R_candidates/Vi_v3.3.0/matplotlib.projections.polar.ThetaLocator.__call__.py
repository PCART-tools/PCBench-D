    def __call__(self):
        lim = self.axis.get_view_interval()
        if _is_full_circle_deg(lim[0], lim[1]):
            return np.arange(8) * 2 * np.pi / 8
        else:
            return np.deg2rad(self.base())
