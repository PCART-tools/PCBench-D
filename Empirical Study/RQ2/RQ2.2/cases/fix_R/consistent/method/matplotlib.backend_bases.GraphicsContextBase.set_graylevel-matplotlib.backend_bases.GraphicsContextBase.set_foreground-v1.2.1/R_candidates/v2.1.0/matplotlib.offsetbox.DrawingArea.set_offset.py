    def set_offset(self, xy):
        """
        set offset of the container.

        Accept : tuple of x,y cooridnate in disokay units.
        """
        self._offset = xy

        self.offset_transform.clear()
        self.offset_transform.translate(xy[0], xy[1])
        self.stale = True
