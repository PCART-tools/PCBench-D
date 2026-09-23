    def point_at_t(self, t):
        """Return the point (x, y) at parameter *t*."""
        tt = ((1 - t) ** self._orders)[::-1] * t ** self._orders
        _x = np.dot(tt, self._px)
        _y = np.dot(tt, self._py)
        return _x, _y
