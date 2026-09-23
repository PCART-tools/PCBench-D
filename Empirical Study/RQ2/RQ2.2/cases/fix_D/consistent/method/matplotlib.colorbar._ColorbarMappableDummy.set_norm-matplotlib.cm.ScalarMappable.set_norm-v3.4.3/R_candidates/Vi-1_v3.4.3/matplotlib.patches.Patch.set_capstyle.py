    @docstring.interpd
    def set_capstyle(self, s):
        """
        Set the `.CapStyle`.

        Parameters
        ----------
        s : `.CapStyle` or %(CapStyle)s
        """
        cs = CapStyle(s)
        self._capstyle = cs
        self.stale = True
