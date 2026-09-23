    def set_data(self, pts, y=None):
        """Set x and y positions of handles."""
        if y is not None:
            x = pts
            pts = np.array([x, y])
        self._markers.set_data(pts)
