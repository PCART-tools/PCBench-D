    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred within the image.
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)
        # TODO: make sure this is consistent with patch and patch
        # collection on nonlinear transformed coordinates.
        # TODO: consider returning image coordinates (shouldn't
        # be too difficult given that the image is rectilinear
        x, y = mouseevent.xdata, mouseevent.ydata
        xmin, xmax, ymin, ymax = self.get_extent()
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin

        if x is not None and y is not None:
            inside = (xmin <= x <= xmax) and (ymin <= y <= ymax)
        else:
            inside = False

        return inside, {}
