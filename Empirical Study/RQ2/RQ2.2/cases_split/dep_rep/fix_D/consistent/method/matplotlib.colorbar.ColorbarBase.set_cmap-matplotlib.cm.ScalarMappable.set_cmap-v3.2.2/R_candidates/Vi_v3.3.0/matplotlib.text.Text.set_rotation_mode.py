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
        cbook._check_in_list(["anchor", "default", None], rotation_mode=m)
        self._rotation_mode = m
        self.stale = True
