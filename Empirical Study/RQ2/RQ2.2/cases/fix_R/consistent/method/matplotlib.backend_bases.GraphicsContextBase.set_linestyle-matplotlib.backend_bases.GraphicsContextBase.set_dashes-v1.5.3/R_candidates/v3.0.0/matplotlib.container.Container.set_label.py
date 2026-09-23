    def set_label(self, s):
        """
        Set the label to *s* for auto legend.

        Parameters
        ----------
        s : string or anything printable with '%s' conversion.
        """
        if s is not None:
            self._label = '%s' % (s, )
        else:
            self._label = None
        self.pchanged()
