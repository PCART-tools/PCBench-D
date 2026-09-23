    @docstring.interpd
    def set_joinstyle(self, s):
        """
        Set the `.JoinStyle`.

        Parameters
        ----------
        s : `.JoinStyle` or %(JoinStyle)s
        """
        js = JoinStyle(s)
        self._joinstyle = js
        self.stale = True
