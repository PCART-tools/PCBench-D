    def set_rotation_mode(self, m):
        """
        set text rotation mode. If "anchor", the un-rotated text
        will first aligned according to their *ha* and
        *va*, and then will be rotated with the alignement
        reference point as a origin. If None (default), the text will be
        rotated first then will be aligned.
        """
        if m is None or m in ["anchor", "default"]:
            self._rotation_mode = m
        else:
            raise ValueError("Unknown rotation_mode : %s" % repr(m))
        self.stale = True
