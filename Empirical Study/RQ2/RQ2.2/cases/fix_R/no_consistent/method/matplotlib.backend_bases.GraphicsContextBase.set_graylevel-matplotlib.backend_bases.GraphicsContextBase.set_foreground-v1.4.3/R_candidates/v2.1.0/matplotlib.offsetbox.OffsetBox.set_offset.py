    def set_offset(self, xy):
        """
        Set the offset

        accepts x, y, tuple, or a callable object.
        """
        self._offset = xy
        self.stale = True
