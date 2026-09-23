    def set_label(self, s):
        """
        Set the label to *s* for auto legend.

        Parameters
        ----------
        s : object
            Any object other than None gets converted to its `str`.
        """
        if s is not None:
            self._label = str(s)
        else:
            self._label = None
        self.pchanged()
