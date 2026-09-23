    def closest(self, x, y):
        """Return index and pixel distance to closest index."""
        pts = np.transpose((self.x, self.y))
        # Transform data coordinates to pixel coordinates.
        pts = self.ax.transData.transform(pts)
        diff = pts - ((x, y))
        if diff.ndim == 2:
            dist = np.sqrt(np.sum(diff ** 2, axis=1))
            return np.argmin(dist), np.min(dist)
        else:
            return 0, np.sqrt(np.sum(diff ** 2))
