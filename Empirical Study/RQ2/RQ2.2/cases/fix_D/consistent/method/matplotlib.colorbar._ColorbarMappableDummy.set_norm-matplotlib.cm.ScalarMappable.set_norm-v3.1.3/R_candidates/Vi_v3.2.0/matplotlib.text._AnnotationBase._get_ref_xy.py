    def _get_ref_xy(self, renderer):
        """
        return x, y (in display coordinate) that is to be used for a reference
        of any offset coordinate
        """
        def is_offset(s):
            return isinstance(s, str) and s.split()[0] == "offset"

        if isinstance(self.xycoords, tuple):
            if any(map(is_offset, self.xycoords)):
                raise ValueError("xycoords should not be an offset coordinate")
        elif is_offset(self.xycoords):
            raise ValueError("xycoords should not be an offset coordinate")
        x, y = self.xy
        return self._get_xy(renderer, x, y, self.xycoords)
