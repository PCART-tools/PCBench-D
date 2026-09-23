    def contains(self, mouseevent):
        """Test whether the mouse event occurred within the image."""
        if (self._different_canvas(mouseevent)
                # This doesn't work for figimage.
                or not self.axes.contains(mouseevent)[0]):
            return False, {}
        # TODO: make sure this is consistent with patch and patch
        # collection on nonlinear transformed coordinates.
        # TODO: consider returning image coordinates (shouldn't
        # be too difficult given that the image is rectilinear
        trans = self.get_transform().inverted()
        x, y = trans.transform([mouseevent.x, mouseevent.y])
        xmin, xmax, ymin, ymax = self.get_extent()
        # This checks xmin <= x <= xmax *or* xmax <= x <= xmin.
        inside = (x is not None and (x - xmin) * (x - xmax) <= 0
                  and y is not None and (y - ymin) * (y - ymax) <= 0)
        return inside, {}
