    def set_rotation_mode(self, m):
        """
        Set text rotation mode.

        Parameters
        ----------
        m : {None, 'default', 'anchor'}
            If ``None`` or ``"default"``, the text will be first rotated, then
            aligned according to their horizontal and vertical alignments.  If
            ``"anchor"``, then alignment occurs before rotation.
        """
        if m is None or m in ["anchor", "default"]:
            self._rotation_mode = m
        else:
            raise ValueError("Unknown rotation_mode : %s" % repr(m))
        self.stale = True
