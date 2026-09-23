    def _summary(self, name=None):
        """
        Return a summarized representation.

        Parameters
        ----------
        name : str
            Name to use in the summary representation.

        Returns
        -------
        str
            Summarized representation of the index.
        """
        formatter = self._formatter_func
        if len(self) > 0:
            index_summary = f", {formatter(self[0])} to {formatter(self[-1])}"
        else:
            index_summary = ""

        if name is None:
            name = type(self).__name__
        result = f"{name}: {len(self)} entries{index_summary}"
        if self.freq:
            result += f"\nFreq: {self.freqstr}"

        # display as values, not quoted
        result = result.replace("'", "")
        return result
