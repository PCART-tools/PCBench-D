    def set_label(self, s):
        """
        Set the label to *s* for auto legend.

        Parameters
        ----------
        s : object
            *s* will be converted to a string by calling `str`.
        """
        if s is not None:
            self._label = str(s)
        else:
            self._label = None
        self.pchanged()
        self.stale = True
