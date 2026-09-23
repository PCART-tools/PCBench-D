    def set_xy(self, xy):
        """
        Set the vertices of the polygon

        Parameters
        ----------
        xy : numpy array or iterable of pairs
            The coordinates of the vertices as a Nx2
            ndarray or iterable of pairs.
        """
        xy = np.asarray(xy)
        if self._closed:
            if len(xy) and (xy[0] != xy[-1]).any():
                xy = np.concatenate([xy, [xy[0]]])
        else:
            if len(xy) > 2 and (xy[0] == xy[-1]).all():
                xy = xy[:-1]
        self._path = Path(xy, closed=self._closed)
        self.stale = True
