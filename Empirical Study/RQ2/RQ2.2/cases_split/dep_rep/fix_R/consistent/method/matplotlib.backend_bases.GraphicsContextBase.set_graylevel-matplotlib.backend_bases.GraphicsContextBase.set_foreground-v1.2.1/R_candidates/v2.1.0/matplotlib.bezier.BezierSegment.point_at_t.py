    def point_at_t(self, t):
        "evaluate a point at t"
        one_minus_t_powers = np.power(1. - t, self._orders)[::-1]
        t_powers = np.power(t, self._orders)

        tt = one_minus_t_powers * t_powers
        _x = sum(tt * self._px)
        _y = sum(tt * self._py)

        return _x, _y
