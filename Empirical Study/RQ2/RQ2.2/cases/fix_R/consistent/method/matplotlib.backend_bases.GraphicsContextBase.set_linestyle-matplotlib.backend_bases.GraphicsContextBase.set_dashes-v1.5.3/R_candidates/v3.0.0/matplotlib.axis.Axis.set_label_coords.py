    def set_label_coords(self, x, y, transform=None):
        """
        Set the coordinates of the label.  By default, the x
        coordinate of the y label is determined by the tick label
        bounding boxes, but this can lead to poor alignment of
        multiple ylabels if there are multiple axes.  Ditto for the y
        coordinate of the x label.

        You can also specify the coordinate system of the label with
        the transform.  If None, the default coordinate system will be
        the axes coordinate system (0,0) is (left,bottom), (0.5, 0.5)
        is middle, etc

        """

        self._autolabelpos = False
        if transform is None:
            transform = self.axes.transAxes

        self.label.set_transform(transform)
        self.label.set_position((x, y))
        self.stale = True
