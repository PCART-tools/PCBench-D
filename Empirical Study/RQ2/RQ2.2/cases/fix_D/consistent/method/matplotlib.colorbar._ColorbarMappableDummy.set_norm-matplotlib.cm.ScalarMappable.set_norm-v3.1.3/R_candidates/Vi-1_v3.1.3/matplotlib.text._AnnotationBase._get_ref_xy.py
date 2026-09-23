    def _get_ref_xy(self, renderer):
        """
        return x, y (in display coordinate) that is to be used for a reference
        of any offset coordinate
        """
        def is_offset(s):
            return isinstance(s, str) and s.split()[0] == "offset"

        if isinstance(self.xycoords, tuple):
            s1, s2 = self.xycoords
            if is_offset(s1) or is_offset(s2):
                raise ValueError("xycoords should not be an offset coordinate")
            x, y = self.xy
            x1, y1 = self._get_xy(renderer, x, y, s1)
            x2, y2 = self._get_xy(renderer, x, y, s2)
            return x1, y2
        elif is_offset(self.xycoords):
            raise ValueError("xycoords should not be an offset coordinate")
        else:
            x, y = self.xy
            return self._get_xy(renderer, x, y, self.xycoords)
