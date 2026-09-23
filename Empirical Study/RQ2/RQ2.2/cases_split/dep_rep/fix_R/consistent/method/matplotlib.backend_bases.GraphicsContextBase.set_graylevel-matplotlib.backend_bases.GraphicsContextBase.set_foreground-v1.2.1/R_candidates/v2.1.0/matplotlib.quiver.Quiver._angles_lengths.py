    def _angles_lengths(self, U, V, eps=1):
        xy = self.ax.transData.transform(self.XY)
        uv = np.hstack((U[:, np.newaxis], V[:, np.newaxis]))
        xyp = self.ax.transData.transform(self.XY + eps * uv)
        dxy = xyp - xy
        angles = np.arctan2(dxy[:, 1], dxy[:, 0])
        lengths = np.hypot(*dxy.T) / eps
        return angles, lengths
