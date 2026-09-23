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
        data_extent = Bbox([[xmin, ymin], [xmax, ymax]])
        array_extent = Bbox([[0, 0], [arr.shape[1], arr.shape[0]]])
        trans = self.get_transform().inverted()
        trans += BboxTransform(boxin=data_extent, boxout=array_extent)
        point = trans.transform([event.x, event.y])
        if any(np.isnan(point)):
            return None
        j, i = point.astype(int)
        # Clip the coordinates at array bounds
        if not (0 <= i < arr.shape[0]) or not (0 <= j < arr.shape[1]):
            return None
        else:
            return arr[i, j]
