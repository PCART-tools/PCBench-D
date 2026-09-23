    def get_cursor_data(self, event):
        """
        Return the image value at the event position or *None* if the event is
        outside the image.

        See Also
        --------
        matplotlib.artist.Artist.get_cursor_data
        """
        xmin, xmax, ymin, ymax = self.get_extent()
        if self.origin == 'upper':
            ymin, ymax = ymax, ymin
        arr = self.get_array()
        data_extent = Bbox([[ymin, xmin], [ymax, xmax]])
        array_extent = Bbox([[0, 0], arr.shape[:2]])
        trans = BboxTransform(boxin=data_extent, boxout=array_extent)
        point = trans.transform([event.ydata, event.xdata])
        if any(np.isnan(point)):
            return None
        i, j = point.astype(int)
        # Clip the coordinates at array bounds
        if not (0 <= i < arr.shape[0]) or not (0 <= j < arr.shape[1]):
            return None
        else:
            return arr[i, j]
