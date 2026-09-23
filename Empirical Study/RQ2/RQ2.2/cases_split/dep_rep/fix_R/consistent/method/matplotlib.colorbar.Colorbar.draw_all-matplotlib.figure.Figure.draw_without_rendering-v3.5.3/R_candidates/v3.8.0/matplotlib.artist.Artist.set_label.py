    def set_label(self, s):
        """
        Set a label that will be displayed in the legend.

        Parameters
        ----------
        s : object
            *s* will be converted to a string by calling `str`.
        """
        label = str(s) if s is not None else None
        if label != self._label:
            self._label = label
            self.pchanged()
            self.stale = True
