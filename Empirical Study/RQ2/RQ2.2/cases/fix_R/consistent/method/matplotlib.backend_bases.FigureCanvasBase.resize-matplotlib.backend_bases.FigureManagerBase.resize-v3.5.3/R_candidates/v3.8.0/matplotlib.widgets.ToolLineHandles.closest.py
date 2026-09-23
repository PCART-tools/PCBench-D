    def closest(self, x, y):
        """
        Return index and pixel distance to closest handle.

        Parameters
        ----------
        x, y : float
            x, y position from which the distance will be calculated to
            determinate the closest handle

        Returns
        -------
        index, distance : index of the handle and its distance from
            position x, y
        """
        if self.direction == 'horizontal':
            p_pts = np.array([
                self.ax.transData.transform((p, 0))[0] for p in self.positions
                ])
            dist = abs(p_pts - x)
        else:
            p_pts = np.array([
                self.ax.transData.transform((0, p))[1] for p in self.positions
                ])
            dist = abs(p_pts - y)
        index = np.argmin(dist)
        return index, dist[index]
