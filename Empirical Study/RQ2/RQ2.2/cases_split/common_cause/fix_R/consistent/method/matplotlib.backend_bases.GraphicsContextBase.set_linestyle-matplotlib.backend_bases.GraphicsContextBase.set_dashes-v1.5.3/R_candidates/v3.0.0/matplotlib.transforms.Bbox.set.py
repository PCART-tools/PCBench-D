    def set(self, other):
        """
        Set this bounding box from the "frozen" bounds of another
        :class:`Bbox`.
        """
        if np.any(self._points != other.get_points()):
            self._points = other.get_points()
            self.invalidate()
