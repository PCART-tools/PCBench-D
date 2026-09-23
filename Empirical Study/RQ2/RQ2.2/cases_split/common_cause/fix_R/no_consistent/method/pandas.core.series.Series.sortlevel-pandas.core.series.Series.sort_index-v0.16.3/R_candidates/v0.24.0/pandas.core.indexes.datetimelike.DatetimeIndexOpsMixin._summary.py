    def _summary(self, name=None):
        """
        Return a summarized representation.

        Parameters
        ----------
        name : str
            name to use in the summary representation

        Returns
        -------
        String with a summarized representation of the index
        """
        formatter = self._formatter_func
        if len(self) > 0:
            index_summary = ', %s to %s' % (formatter(self[0]),
                                            formatter(self[-1]))
        else:
            index_summary = ''

        if name is None:
            name = type(self).__name__
        result = '%s: %s entries%s' % (printing.pprint_thing(name),
                                       len(self), index_summary)
        if self.freq:
            result += '\nFreq: %s' % self.freqstr

        # display as values, not quoted
        result = result.replace("'", "")
        return result
