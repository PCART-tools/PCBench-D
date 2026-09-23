    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred within the image.
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        # 1) This doesn't work for figimage; but figimage also needs a fix
        #    below (as the check cannot use x/ydata and extents).
        # 2) As long as the check below uses x/ydata, we need to test axes
        #    identity instead of `self.axes.contains(event)` because even if
        #    axes overlap, x/ydata is only valid for event.inaxes anyways.
        if self.axes is not mouseevent.inaxes:
            return False, {}
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
