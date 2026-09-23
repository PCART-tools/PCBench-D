    def _get_ref_xy(self, renderer):
        """
        return x, y (in display coordinate) that is to be used for a reference
        of any offset coordinate
        """

        if isinstance(self.xycoords, tuple):
            s1, s2 = self.xycoords
            if ((isinstance(s1, six.string_types)
                 and s1.split()[0] == "offset")
                    or (isinstance(s2, six.string_types)
                        and s2.split()[0] == "offset")):
                raise ValueError("xycoords should not be an offset coordinate")
            x, y = self.xy
            x1, y1 = self._get_xy(renderer, x, y, s1)
            x2, y2 = self._get_xy(renderer, x, y, s2)
            return x1, y2
        elif (isinstance(self.xycoords, six.string_types) and
              self.xycoords.split()[0] == "offset"):
            raise ValueError("xycoords should not be an offset coordinate")
        else:
            x, y = self.xy
            return self._get_xy(renderer, x, y, self.xycoords)
