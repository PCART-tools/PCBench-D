    def __unicode__(self):
        """
        Return a string representation for a particular DataFrame

        Invoked by unicode(df) in py2 only. Yields a Unicode String in both
        py2/py3.
        """
        width, height = get_terminal_size()
        max_rows = (height if get_option("display.max_rows") == 0
                    else get_option("display.max_rows"))
        if len(self.index) > (max_rows or 1000):
            result = self._tidy_repr(min(30, max_rows - 4))
        elif len(self.index) > 0:
            result = self._get_repr(print_header=True,
                                    length=len(self) > 50,
                                    name=True,
                                    dtype=True)
        elif self.name is None:
            result = u('Series([], dtype: %s)') % (self.dtype)
        else:
            result = u('Series([], name: %s, dtype: %s)') % (self.name,
                                                             self.dtype)
        return result
