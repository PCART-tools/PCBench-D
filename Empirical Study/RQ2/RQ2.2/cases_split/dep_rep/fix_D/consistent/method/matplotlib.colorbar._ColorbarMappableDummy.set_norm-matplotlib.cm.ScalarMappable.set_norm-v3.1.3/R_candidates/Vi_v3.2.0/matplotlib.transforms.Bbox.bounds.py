    @BboxBase.bounds.setter
    def bounds(self, bounds):
        l, b, w, h = bounds
        points = np.array([[l, b], [l + w, b + h]], float)
        if np.any(self._points != points):
            self._points = points
            self.invalidate()
